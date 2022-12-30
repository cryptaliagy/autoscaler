"""A module for the github client."""

import httpx

from autoscaler.config import Settings
from autoscaler.models import (
    RegistrationTokenResponse,
)


class GithubClient:
    """A client for interacting with the Github API."""

    __client: httpx.AsyncClient | None

    def __init__(self, settings: Settings | None = None) -> None:
        """
        Create a new GithubClient.

        If settings are passed into the constructor, initialize the httpx
        client. Otherwise, the client will be initialized when the
        initialize method is called.

        Args:
            settings: The settings to use for the client.
        """
        self.__client = None

        if settings is not None:
            self.initialize(settings)

    @property
    def _client(self) -> httpx.AsyncClient:
        """Get the httpx client."""
        if self.__client is None:
            raise ValueError("Client has not been initialized")

        return self.__client

    def initialize(self, settings: Settings) -> None:
        """Initialize the client."""
        self.__client = httpx.AsyncClient(
            headers={
                "Authorization": f"token {settings.github_pat}",
                "Accept": "application/vnd.github.v3+json",
            },
            base_url="https://api.github.com",
        )

    async def create_runner_token(self, owner: str, repo: str | None = None) -> str:
        """Create a new runner token for a repo.

        Args:
            owner: The owner of the repo.
            repo: The name of the repo, or None if the token is for an org.

        Returns:
            A registration token for a new runner.
        """
        if repo is None:
            suffix = f"/orgs/{owner}/actions/runners/registration-token"
        else:
            suffix = f"/repos/{owner}/{repo}/actions/runners/registration-token"

        res = await self._client.post(suffix)

        if res.status_code >= 300:
            raise ValueError("Something went wrong in the API call")

        return RegistrationTokenResponse.parse_raw(res.content).token

    async def close(self) -> None:
        """Close the client."""
        await self._client.aclose()

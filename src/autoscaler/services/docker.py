"""A module for interacting with the docker client."""

import docker  # pyright: reportMissingTypeStubs=false

from docker.errors import BuildError

from docker.models.containers import Container
from docker.models.images import Image

from loguru import logger

from autoscaler.config import (
    Settings,
    RunnerSettings,
)

from typing import (
    cast,
    Any,
)


class DockerClient:
    """A class for interacting with the docker client."""

    _client: docker.DockerClient
    image: Image
    settings: RunnerSettings
    is_enabled: bool

    def __init__(
        self,
        *,
        client: docker.DockerClient | None = None,
        settings: Settings | None = None,
    ):
        """
        Initialise the client.

        Args:
            client: The docker client to use. If None, a client will be
                created using the default settings.
            settings: The settings to use for the client.
        """
        self._client = (
            client or docker.from_env()
        )  # pyright: reportUnknownMemberType=false,reportUnknownVariableType=false

        if settings is not None:
            self.initialize(settings)

    def initialize(self, settings: Settings) -> None:
        """
        Initialize the client.

        Args:
            settings: The settings to use for the client.
        """
        self.is_enabled = settings.docker.enabled
        self.settings = settings.runner

        if not self.is_enabled:
            logger.debug("Docker client disabled")
            return

        if settings.docker.build_image:
            logger.debug(
                "Building runner image "
                f"{settings.docker.runner_image}:{settings.docker.runner_tag}"
                f" from {settings.docker.runner_dockerfile} in "
                f"{settings.docker.build_path}"
            )
            self.build_image(
                path=settings.docker.build_path,
                dockerfile=settings.docker.runner_dockerfile,
                image=settings.docker.runner_image,
                tag=settings.docker.runner_tag,
                no_cache=settings.docker.no_cache,
            )
        else:
            logger.debug(
                "Pulling runner image "
                f"{settings.docker.runner_image}:{settings.docker.runner_tag}"
            )
            self.pull_image(
                image=settings.docker.runner_image,
                tag=settings.docker.runner_tag,
            )

        logger.debug("Docker client initialized")
        logger.debug(f"Runner image ID: {self.image.id}")
        logger.debug(f"Runner image tags: {self.image.tags}")

    async def close(self) -> None:
        """Close the client."""
        self._client.close()

    def pull_image(self, *, image: str, tag: str = "latest") -> None:
        """
        Pull an image.

        Args:
            image: The name of the image.

        Raises:
            `docker.errors.APIError`: If the image could not be pulled.
        """
        self.image = cast(
            Image,
            self._client.images.pull(image, tag=tag),
        )

    def build_image(
        self,
        *,
        path: str,
        dockerfile: str,
        image: str,
        tag: str = "latest",
        no_cache: bool = False,
    ) -> None:
        """
        Build an image.

        Args:
            dockerfile: The path to the dockerfile.
            image: The name of the image.

        Returns:
            The image that was built.
        """
        try:
            self.image, logs = cast(
                tuple[Image, Any],
                self._client.images.build(
                    path=path,
                    dockerfile=dockerfile,
                    tag=f"{image}:{tag}",
                    nocache=no_cache,
                ),
            )
            for log in logs:
                logger.debug(log.get("stream", "").strip())
        except BuildError as error:
            for log in error.build_log:
                logger.error(log)  # pyright: reportUnknownArgumentType=false

            raise

    def list_runners(self) -> list[Container]:
        """
        List the runners.

        Returns:
            A list of the runners.
        """
        containers = cast(list[Container], self._client.containers.list())

        return [
            container
            for container in containers
            if cast(Image, container.image).id == self.image.id
        ]

    def start_runner(self, *, url: str, token: str) -> None:
        """
        Start a new runner.

        Args:
            url: The URL of the runner.
            token: The registration token for the runner.

        Returns:
            The container that was started.
        """
        container = cast(
            Container,
            self._client.containers.run(
                self.image,
                remove=True,
                detach=True,
                environment={
                    "URL": url,
                    "TOKEN": token,
                },
                volumes=["/var/run/docker.sock:/var/run/docker.sock"],
            ),
        )

        logger.debug(f"Started runner {container.name}")
        logger.debug(f"CID: {container.id}")
        logger.debug(f"Logs: {container.logs()}")

    def count_runners(self) -> int:
        """
        Count the number of runners.

        Returns:
            The number of runners.
        """
        return len(self.list_runners())

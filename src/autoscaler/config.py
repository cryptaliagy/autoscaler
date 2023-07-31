"""
A module containing settings for the app.

While this module defines some defaults, all settings
can be overridden by setting environment variables with
the same name as the setting.
"""

from pydantic_settings import (
    BaseSettings,
)


class DockerSettings(BaseSettings):
    """Settings for the docker client."""

    build_image: bool = True
    build_path: str = "."
    runner_dockerfile: str = "./devstack/runner.dockerfile"
    runner_image: str = "runner"
    runner_tag: str = "latest"
    no_cache: bool = False
    enabled: bool = True

    class Config:  # pyright: ignore
        """Pydantic config."""

        env_prefix = "DOCKER_"


class RunnerSettings(BaseSettings):
    """
    Settings for the runner.

    Attributes:
        max_scale_up: The maximum number of runners to scale up
            at once.
        scale_polling_interval: The interval, in seconds, at which
            to poll for number of runners.
        autoscale_timeout: The timeout, in seconds, after which
            the autoscaler will stop trying to scale up runners.
            This is set to 23 hours by default, as Github will drop
            any job that takes longer than 24 hours to be picked up
            by a runner.
    """

    max_runners: int = 5
    scale_polling_interval: int = 60
    autoscale_timeout: int = 60 * 60 * 23
    base_url: str = "https://github.com"

    class Config:  # pyright: ignore
        """Pydantic config."""

        env_prefix = "RUNNER_"


class Settings(BaseSettings):
    """
    Settings for the app.

    Any settings that are not set will be automatically
    read from the environment by Pydantic. Any settings can also
    be overridden by setting environment variables with the same
    name as the setting.

    Attributes:
        env: The environment that the app is running in.
        debug: Whether the app is running in debug mode.
        secret_token: The secret token to use for authenticating
            requests to the app.
        github_pat: The Github personal access token to use for
            authenticating with the Github API.
        docker: Settings for the docker client.
        runner: Settings for the runner.
    """

    env: str = "dev"
    debug: bool = False
    secret_token: str = "secret"
    github_pat: str = "secret"
    docker: DockerSettings = DockerSettings()
    runner: RunnerSettings = RunnerSettings()

    @property
    def openapi_url(self) -> str:  # pragma: no cover
        """
        Get the URL to the OpenAPI docs.

        This allows the docs to be disabled in production.
        """
        if self.env == "dev":
            return "/openapi.json"
        return ""

    class Config:  # pyright: ignore
        """
        Configurations for the settings.

        Attributes:
            env_file: The file to read environment variables from,
                if it exists.
        """

        env_file = ".env"
        env_prefix = "AUTOSCALER_"

"""A module for external services."""


from autoscaler.services.github import GithubClient
from autoscaler.services.docker import DockerClient
from autoscaler.services.protocols import Service, RunnerProvider

__all__ = [
    "docker",
    "github",
    "get_services",
    "Service",
    "RunnerProvider",
]

docker = DockerClient()
github = GithubClient()


def get_services() -> list[Service]:
    """Return a list of services."""
    return [docker, github]

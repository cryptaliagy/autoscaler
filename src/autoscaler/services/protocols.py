"""Protocols for services."""

from autoscaler.config import (
    Settings,
    RunnerSettings,
)

from typing import Protocol


class Service(Protocol):
    """A protocol for services."""

    def initialize(self, settings: Settings) -> None:
        """Initialize the service."""
        ...

    async def close(self) -> None:
        """Close the service."""
        ...


class RunnerProvider(Protocol):
    """A protocol for runner providers."""

    settings: RunnerSettings

    def start_runner(self, *, url: str, token: str) -> None:
        """Start a runner."""
        ...

    def count_runners(self) -> int:
        """Count the number of runners."""
        ...

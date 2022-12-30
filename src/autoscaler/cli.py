"""A module for running CLI commands related to the autoscaler."""

import asyncio

import typer

from autoscaler.services import (
    github,
    docker,
)
from autoscaler.config import Settings

github.initialize(Settings())
docker.initialize(Settings())

cli = typer.Typer()


gh = typer.Typer()

dkr = typer.Typer()


@gh.command("create-token")
def create_token(owner: str = typer.Option(None), repo: str = "") -> None:
    """Create a new Github Runner token."""
    token = asyncio.new_event_loop().run_until_complete(
        github.create_runner_token(owner, repo)
    )

    typer.echo(token)


@dkr.command("create-runner")
def create_runner(owner: str = typer.Option(None), repo: str = "") -> None:
    """Create a new Github Runner."""
    token = asyncio.new_event_loop().run_until_complete(
        github.create_runner_token(owner, repo)
    )

    docker.start_runner(url=f"https://github.com/{owner}/{repo}", token=token)


cli.add_typer(gh, name="gh")
cli.add_typer(dkr, name="dkr")

if __name__ == "__main__":
    cli()

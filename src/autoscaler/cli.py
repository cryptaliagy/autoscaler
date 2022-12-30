"""A module for running CLI commands related to the autoscaler."""

import asyncio

import typer

from autoscaler.services import github
from autoscaler.config import Settings

github.initialize(Settings())

cli = typer.Typer()


gh = typer.Typer()


@gh.command("create-token")
def create_token(owner: str = typer.Option(None), repo: str = "") -> None:
    """Create a new Github Runner token."""
    token = asyncio.new_event_loop().run_until_complete(
        github.create_runner_token(owner, repo)
    )

    typer.echo(token)


cli.add_typer(gh, name="gh")

if __name__ == "__main__":
    cli()

"""A module for background tasks."""

import asyncio

from autoscaler.services import (
    github,
    RunnerProvider,
)

from loguru import logger


async def start_runner(
    *,
    runner_provider: RunnerProvider,
    owner: str,
    repo: str | None,
) -> None:
    """
    Start a runner.

    Args:
        runner_provider: The runner provider to use.
        owner: The owner of the repo.
        repo: The name of the repo.
        token: The registration token for the runner.
    """
    count = 0

    while count < runner_provider.settings.autoscale_timeout:
        if runner_provider.count_runners() < runner_provider.settings.max_runners:
            break

        logger.info("Runner limit reached, waiting for runners to terminate")

        count += runner_provider.settings.scale_polling_interval

        await asyncio.sleep(runner_provider.settings.scale_polling_interval)

    if count >= runner_provider.settings.autoscale_timeout:
        logger.error("Timed out waiting for runners to terminate")

        return

    token = await github.create_runner_token(owner, repo)

    if repo is None:
        logger.info(f"Starting runner for org: {owner}")
        url = f"{runner_provider.settings.base_url}/${owner}"
    else:
        logger.info(f"Starting runner for repo: {owner}/{repo}")
        url = f"{runner_provider.settings.base_url}/${owner}/${repo}"

    runner_provider.start_runner(url=url, token=token)

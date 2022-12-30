"""
The main module for the autoscaler app.

This module contains the app factory for the autoscaler app, and
acts as the main entry point for the app.
"""

import sys

from fastapi import (
    FastAPI,
    Depends,
)
from loguru import logger

from autoscaler.config import Settings
from autoscaler.dependencies import (
    access_log,
    get_settings,
)
from autoscaler.services import (
    get_services,
)

from autoscaler.routes import router


def create_app(
    settings: Settings | None = None,
) -> FastAPI:
    """
    Create the autoscaler app.

    Application factory for the autoscaler app. This allows the app to be
    configured differently for different environments, e.g. testing.
    This factory also sets up the logging for the app.

    Args:
        settings: The settings to use for the app.

    Returns:
        The app.
    """
    active_settings = settings or get_settings()

    app = FastAPI(
        openapi_url=active_settings.openapi_url,
        dependencies=[Depends(access_log)],
    )

    app.include_router(router)

    @app.on_event(
        "startup"
    )  # pyright: reportUnknownMemberType=false,reportUntypedFunctionDecorator=false
    async def _() -> None:
        log_level = "DEBUG" if active_settings.debug else "INFO"
        logger.remove(0)
        logger.add(
            sys.stderr,
            level=log_level,
            format="<yellow>{time:YYYY-MM-DD HH:mm:ss}</yellow> |"
            # + " [<green>{process}</green>] |"
            + " <level>{level:6s}</level> |"
            + " <cyan>{name}:{function}:{line}</cyan> - {message}",
            colorize=True,
        )

        logger.info("Starting app")

        logger.info("Loading services")
        for service in get_services():
            logger.info(f"Starting {service.__class__.__name__}")
            service.initialize(active_settings)

        logger.info("Services loaded")

    @app.on_event(
        "shutdown"
    )  # pyright: reportUnknownMemberType=false,reportUntypedFunctionDecorator=false
    async def _() -> None:
        logger.info("Shutting down app")
        for service in get_services():
            logger.info(f"Closing {service.__class__.__name__}")
            await service.close()

    return app

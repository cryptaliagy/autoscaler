"""
A module to define dependencies for the app.

Dependencies are used to inject objects into routes. This allows
the routes to be as simple as possible, and allows for the
injection of objects that are used by multiple routes.
"""


from functools import lru_cache

from fastapi import (
    Request,
    Header,
    HTTPException,
    Depends,
)

from loguru import logger
from cryptography.hazmat.primitives import (
    hashes,
    hmac,
)

from autoscaler.config import Settings


@lru_cache()
def get_settings() -> Settings:  # pragma: no cover
    """
    Get the settings for the app.

    This is cached so that the settings are only created once.
    Dependency is used to inject the settings into routes that
    need them.

    Returns:
        The default app settings.
    """
    # Need to initialize this way to prevent pylance from complaining about
    # the Settings class not being given values for things that get
    # pulled from the environment.
    # https://docs.pydantic.dev/visual_studio_code/#basesettings-and-ignoring-pylancepyright-errors
    return Settings.parse_obj({})


async def access_log(request: Request) -> None:
    """
    Log the request to the access log.

    This dependency is used by the app to log all requests to the
    access log.

    Args:
        request: The request to log. This is injected by FastAPI.
    """
    logger.info(
        f"{request.method} {request.url.path} "
        + f"{request.url.query} {request.headers.get('User-Agent')}"
    )


async def check_hmac(
    request: Request,
    x_hub_signature_256: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> None:
    """
    Check the HMAC signature for the request.

    This dependency is used by the app to check the HMAC signature
    for the request. If the signature is invalid, the request is
    rejected.

    Args:
        request: The request to check. This is injected by FastAPI.
        x_hub_signature_256: The HMAC signature for the request.
            This is injected by FastAPI.
        settings: The settings for the app. This is injected by
            FastAPI.
    """
    if x_hub_signature_256 is None:
        logger.error("No HMAC signature provided!")
        raise HTTPException(status_code=400, detail="No HMAC signature provided!")

    if len(x_hub_signature_256) < 8:
        logger.error("Invalid HMAC signature provided!")
        raise HTTPException(status_code=400, detail="Invalid HMAC signature provided!")

    # Github uses HMAC-based auth using a pre-provided secret key
    key = settings.secret_token.encode()

    signature = hmac.HMAC(key, hashes.SHA256())
    data = await request.body()

    signature.update(data)

    try:
        signature.verify(x_hub_signature_256[7:].encode())
    except Exception as e:
        logger.error(f"Failed HMAC authentication: {e}")
        raise HTTPException(status_code=400, detail="Invalid HMAC signature provided!")

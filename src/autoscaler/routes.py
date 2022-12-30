"""
A module for the routes of the app.

All routes are defined using FastAPI's APIRouter. The routes are
then mounted on the app in autoscaler/__init__.py. This is done so
that they can be defined independently of the app.
"""

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
)

from autoscaler.dependencies import (
    check_hmac,
)
from autoscaler.models import (
    StatusResponse,
    WorkflowJobAction,
    WorkflowJobWebhookPayload,
)
from autoscaler.tasks import (
    start_runner,
)
from autoscaler.services import (
    docker,
)


router = APIRouter()


@router.get(
    "/heartbeat",
    response_model=StatusResponse,
    summary="Check the status of the app",
    description="A route for checking the status of the app.",
)
async def heartbeat() -> StatusResponse:
    """
    Return a status response to indicate that the service is up and running.

    Returns:
        A status response message
    """
    return StatusResponse(msg="Service is up and running")


@router.post(
    "/webhook/repo/docker",
    summary="Handle a webhook from Github",
    description="A route for handling webhooks from Github.",
    response_model=StatusResponse,
    dependencies=[Depends(check_hmac)],
)
async def webhook(
    payload: WorkflowJobWebhookPayload,
    tasks: BackgroundTasks,
) -> StatusResponse:
    """
    Handle a webhook from Github.

    Args:
        payload: The payload of the webhook.
        tasks: A background tasks object.

    Returns:
        A status response message.
    """
    if payload.action == WorkflowJobAction.QUEUED:
        tasks.add_task(
            start_runner,
            runner_provider=docker,
            owner=payload.repository.owner.login,
            repo=payload.repository.name,
        )
    return StatusResponse(msg="Webhook received")


@router.post(
    "/webhook/org/docker",
    summary="Handle an org webhook from Github",
    description="A route for handling org webhooks from Github.",
    response_model=StatusResponse,
    dependencies=[Depends(check_hmac)],
)
async def org_webhook(
    payload: WorkflowJobWebhookPayload,
    tasks: BackgroundTasks,
) -> StatusResponse:
    """
    Handle an org webhook from Github.

    Args:
        payload: The payload of the webhook.
        tasks: A background tasks object.

    Returns:
        A status response message.
    """
    if payload.organization is None:
        raise HTTPException(detail="No organization in payload", status_code=400)

    if payload.action == WorkflowJobAction.QUEUED:
        tasks.add_task(
            start_runner,
            runner_provider=docker,
            owner=payload.organization.login,
            repo=None,
        )
    return StatusResponse(msg="Webhook received")

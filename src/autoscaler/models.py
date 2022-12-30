"""
A module for the models of the autoscaler app.

All models are defined using Pydantic's BaseModel. This allows for
validation of the data that is passed to the app, and allows for
serialization of the data that is returned from the app.
"""

from enum import Enum

from pydantic import (
    BaseModel,
)


class WorkflowJobAction(str, Enum):
    """The action that triggered the workflow job webhook."""

    CREATED = "created"
    QUEUED = "queued"
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"


class StatusResponse(BaseModel):
    """
    A generic status response model.

    Attributes:
        msg: The status message.
        status: A short status code.
    """

    status: str = "ok"
    msg: str


class RegistrationTokenResponse(BaseModel):
    """
    A model for the registration token response.

    The expected response from the Github API when requesting a
    registration token for creating a new self-hosted runner.

    Attributes:
        token: The registration token.
        expires_at: The time at which the token expires.
    """

    token: str
    expires_at: str


class RepositoryOwner(BaseModel):
    """
    A model for the repository owner.

    Attributes:
        id: The id of the owner.
        login: The login of the owner.
    """

    id: int
    login: str


class Repository(BaseModel):
    """
    A model for the repository.

    Attributes:
        id: The id of the repository.
        name: The name of the repository.
        full_name: The full name of the repository.
        private: Whether the repository is private.
        owner: The owner of the repository.
    """

    id: int
    name: str
    full_name: str
    private: bool
    owner: RepositoryOwner


class WorkflowJobWebhookPayload(BaseModel):
    """
    A model for the workflow job webhook payload.

    Attributes:
        action: The action that triggered the webhook.
        workflow_job: The workflow job that triggered the webhook.
    """

    action: WorkflowJobAction
    repository: Repository
    organization: RepositoryOwner | None

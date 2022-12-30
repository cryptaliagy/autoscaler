# Github Actions Autoscaler

This project is currently a proof-of-concept Github Actions autoscaling service. It can receive a webhook from Github (using SHA-256 HMAC for authentication) and spin up a github runner to accept the queued job.

## Quickstart

Ensure you have `docker`, `docker-compose`, `poetry`, and `just` installed.

1. Clone the repository
1. Build the container with `just build`
1. Run the container with `just up`

### Without `just`

The `justfile` is provided as a convenience to make commands shorter, but it isn't fully necessary. You can replace any of the listed `just` commands above with `docker compose -f devstack/docker-compose.yaml`.:

1. Clone the repository
1. Build the container with `docker compose -f devstack/docker-compose.yaml build`
1. Run the container with `docker compose -f devstack/docker-compose.yaml up`

### Without Docker

Ensure you have `poetry` installed.

1. Clone the repository
1. Install dependencies with `poetry install`
   OPTIONAL: install only the runtime dependencies: `poetry install --without=dev`
1. Run the `gunicorn` server: `poetry run gunicorn -b 0.0.0.0:5000 -k uvicorn.workers.UvicornWorker 'autoscaler:create_app()'`

### Minimal Quickstart

> You should at _least_ use this in a virtual environment, but I'm not your mom.

1. Clone the repository
1. Install the project: `pip install -e .`
1. Run `uvicorn` server: `python -m autoscaler`

## Configuration

All fields in the `Settings` object can be set via environment variables, allowing various forms of customization. For example, the runner image name can be configured using the `DOCKER_RUNNER_IMAGE` variable.

To see what settings are available, check the [config file](src/autoscaler/config.py). Note that prefixes must be used (as in the `DOCKER_RUNNER_IMAGE` example) when setting the environment variables.

### Setting The Secret Token

For HMAC authentication, a secret token **must** be created and provided to both the autoscaler and Github webhooks. One way such a token can be generated is by using the `openssl` CLI:

```bash
openssl rand -base64 32
```

When creating the webhook, copy+paste this value. All repositories/orgs that the autoscaler will connect to **must** contain the **same** secret.

### Github PAT

Both classic PATs as well as the new fine-grained PATs can be used to provision the runner registration tokens. Classic PATs require the `repo` scope for repository-based webhooks and `mannage_runners:org` for organization-based webhooks.

Fine-grained PATs have been tested with read/write access repository access to `administration` and `actions` scopes.

### Configuring The Webhooks

Note, Github must have a way to connect to your API (such as [`ngrok`](https://ngrok.com/)) for the autoscaler to respond to the github events.

### Repository

Under Repository -> Settings -> Webhooks, create a new webhook. Set the secret token for the webhook, and enable the `workflow_job` hook (and nothing else).

### Organization

Under Organization -> Settings -> Webhooks, create a new webhook. Set the secret token for the webhook, and enable the `workflow_job` hook (and nothing else).

## Should I use this?

No.

While I'm currently working to see if I can make this a properly functioning service, this is very much an in-development piece of work and is likely riddled with security problems that come from setting up infrastructure to run arbitrary code.

For a production-ready Github Actions autoscaler, look at the [Github documentation](https://docs.github.com/en/actions/hosting-your-own-runners/autoscaling-with-self-hosted-runners)

## Known Limitations

- Using the Docker-based webhooks does not allow the use of "container" directives in workflow files. This would require the autoscaler to spin up VMs instead.

## Technology

This project uses [`fastapi`](https://fastapi.tiangolo.com/) as the framework, [`pydantic`](https://docs.pydantic.dev/) for declaring models and configs, and [`loguru`] for logging.

The runners that are spun up are created using Docker and the [`docker` python library](https://github.com/docker/docker-py). The autoscaler uses `docker` and [`gunicorn`](https://gunicorn.org/) for the web server.

Dependency management is handled with [`poetry`](https://python-poetry.org/)

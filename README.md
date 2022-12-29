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

## Should I use this?

No.

While I'm currently working to see if I can make this a properly functioning service, this is very much an in-development piece of work and is likely riddled with security problems that come from setting up infrastructure to run arbitrary code.

For a production-ready Github Actions autoscaler, look at the [Github documentation](https://docs.github.com/en/actions/hosting-your-own-runners/autoscaling-with-self-hosted-runners)

## Technology

This project uses [`fastapi`](https://fastapi.tiangolo.com/) as the framework, [`pydantic`](https://docs.pydantic.dev/) for declaring models and configs, and [`loguru`] for logging.

The runners that are spun up are created using Docker and the [`docker` python library](https://github.com/docker/docker-py). The autoscaler uses `docker` and [`gunicorn`](https://gunicorn.org/) for the web server.

Dependency management is handled with [`poetry`](https://python-poetry.org/)

FROM python:3.10-alpine as dev

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN poetry install --without=dev --no-root

COPY . .

RUN poetry install --without=dev

CMD sh -c "poetry run gunicorn -w 1 --threads 1 -b 0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker 'autoscaler:create_app()' --reload -t 0"

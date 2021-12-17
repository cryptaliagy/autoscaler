FROM python:3.9-slim-buster

WORKDIR /app

COPY devstack/get-docker.sh /app

RUN sh ./get-docker.sh

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

RUN pip install -e .

CMD ["./run.sh"]

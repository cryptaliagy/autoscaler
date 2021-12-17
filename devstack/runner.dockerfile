FROM python:3.9-slim-buster

WORKDIR /runner

RUN apt-get update

RUN apt-get install build-essential -y

RUN pip install docker-compose

COPY devstack/get-docker.sh /runner

RUN sh ./get-docker.sh

RUN curl -O -L https://github.com/actions/runner/releases/download/v2.285.1/actions-runner-linux-x64-2.285.1.tar.gz

RUN tar xzf ./actions-runner-linux-x64-2.285.1.tar.gz

RUN ./bin/installdependencies.sh

COPY runner.sh /runner

RUN useradd -m runner

RUN chown -R runner /runner

USER runner

CMD ["./runner.sh"]

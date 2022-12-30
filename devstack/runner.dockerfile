FROM debian:11-slim

WORKDIR /runner

RUN apt-get update && apt-get install -y curl tar

RUN curl -fsSL https://get.docker.com | sh

RUN curl -O -L https://github.com/actions/runner/releases/download/v2.300.2/actions-runner-linux-x64-2.300.2.tar.gz

RUN tar xzf ./actions-runner-linux-x64-2.*.tar.gz && ./bin/installdependencies.sh

COPY runner.sh /runner

RUN useradd -m runner && usermod -aG docker runner && chown -R runner /runner

USER runner

CMD ["./runner.sh"]

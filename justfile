set positional-arguments
service := "autoscaler"
container_shell := "/bin/sh"
compose_cmd := "docker compose -f devstack/docker-compose.yaml"

alias bd := build
# Build the service(s).
build *args:
	{{ compose_cmd }} build {{ args }}

# Starts the service(s).
up *args:
	{{ compose_cmd }} up {{ args }}

# Runs the specified command from the service container
run *args:
	{{ compose_cmd }} run --rm {{ service }} {{ args }}

alias bash := sh
# Connects to a running service container, if it is currently running
sh:
	{{ compose_cmd }} exec {{ service }} {{ container_shell }}

# Runs all tests in their respective containers
test:
	TARGET=test just bd
	just run /app/config/test.sh

# Removes all docker objects and volumes (for THIS project)
down *args:
	{{ compose_cmd }} down {{ args }}
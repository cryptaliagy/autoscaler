#!/bin/bash
export PATH="/home/runner/.local/bin":$PATH
echo "Connecting to the Github runner"
./config.sh --unattended --url https://github.com/$USER/$REPO --token $TOKEN --ephemeral
./run.sh

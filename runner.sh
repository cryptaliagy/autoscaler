#!/bin/bash

echo "Connecting to the Github runner"
./config.sh --unattended --url https://github.com/$USER/$REPO --token $TOKEN --ephemeral
./run.sh

#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PORT=5000
PID=$(lsof -ti:$PORT)

if [ -z "$PID" ]; then
    echo -e "\nNo process found running on port $PORT"
else
    kill -9 $PID
    echo -e "\nKilled process $PID on port $PORT"
fi

cd "$PROJECT_ROOT/docker"
docker compose down

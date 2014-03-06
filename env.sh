#!/bin/bash

ROOT_PATH="$(cd "$(dirname "$BASH_SOURCE")"; pwd)"

export PYTHONPATH="$ROOT_PATH:$PROJECT_ROOT:$PYTHONPATH"

if [[ -f "$ROOT_PATH/.venv/bin/activate" ]]; then
    . $ROOT_PATH/.venv/bin/activate
fi

#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJ_DIR="$SCRIPT_DIR/.."
SRC_DIR="$PROJ_DIR/src"
export PYTHONPATH=$SRC_DIR:$PYTHONPATH

python -m unittest discover test

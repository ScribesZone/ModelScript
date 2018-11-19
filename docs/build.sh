#!/usr/bin/env bash
source ../.venv/bin/activate
which sphinx-build
sphinx-build --version
make clean
make html

#!/bin/bash
# Simple installer that clones the repository and runs setup.sh
set -e

REPO_URL="https://github.com/youruser/pdf2txtconvert.git"
TMP_DIR="$(mktemp -d)"

cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

cd "$TMP_DIR"

echo "Cloning $REPO_URL"

git clone --depth 1 "$REPO_URL" repo
cd repo

sudo ./setup.sh --install "$@"


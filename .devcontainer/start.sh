#!/usr/bin/env bash
# Runs every time the codespace is opened: serves the site on port 8080.
# To start it by hand:  bash .devcontainer/start.sh
set -euo pipefail
cd "$(dirname "$0")/.."

if curl -s -o /dev/null http://127.0.0.1:8080/; then
  echo "The website is already running on port 8080 (see the Ports tab)."
  exit 0
fi
bundle check >/dev/null 2>&1 || bash .devcontainer/setup.sh
# production: links stay relative instead of pointing to localhost
JEKYLL_ENV=production bundle exec jekyll serve --host 0.0.0.0 --port 8080

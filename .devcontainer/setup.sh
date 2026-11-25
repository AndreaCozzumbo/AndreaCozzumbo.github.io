#!/usr/bin/env bash
# Runs once, when the codespace is created: installs what the site needs.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v convert >/dev/null; then
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends imagemagick
fi
gem list -i bundler -v 4.0.6 >/dev/null || gem install bundler -v 4.0.6 --no-document
bundle config set --local path vendor/bundle
bundle install --jobs 4 --retry 3

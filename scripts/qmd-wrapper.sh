#!/usr/bin/env bash
# qmd wrapper — strips proxy vars before calling qmd
# ipull (qmd's model downloader) bypasses npm proxy and hangs on proxy env vars
#
# Usage:  ./scripts/qmd-wrapper.sh <qmd subcommand> [args...]
# Example: ./scripts/qmd-wrapper.sh search "时间序列" --mode hybrid

exec env \
  -u http_proxy \
  -u https_proxy \
  -u HTTP_PROXY \
  -u HTTPS_PROXY \
  -u all_proxy \
  -u ALL_PROXY \
  qmd "$@"

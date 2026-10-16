#!/bin/sh
set -eu

PROXY_HOST="${PROXY_HOST:-127.0.0.1}"
PROXY_PORT="${PROXY_PORT:-2080}"

CLAUDE_BIN="${CLAUDE_BIN:-claude}"

HTTP_PROXY_URL="http://${PROXY_HOST}:${PROXY_PORT}"
SOCKS_PROXY_URL="socks5://${PROXY_HOST}:${PROXY_PORT}"

if ! command -v "$CLAUDE_BIN" >/dev/null 2>&1; then
    printf 'Ошибка: команда "%s" не найдена.\n' "$CLAUDE_BIN" >&2
    exit 127
fi

exec env \
    http_proxy="$HTTP_PROXY_URL" \
    HTTP_PROXY="$HTTP_PROXY_URL" \
    https_proxy="$HTTP_PROXY_URL" \
    HTTPS_PROXY="$HTTP_PROXY_URL" \
    all_proxy="$SOCKS_PROXY_URL" \
    ALL_PROXY="$SOCKS_PROXY_URL" \
    socks_proxy="$SOCKS_PROXY_URL" \
    SOCKS_PROXY="$SOCKS_PROXY_URL" \
    "$CLAUDE_BIN" "$@"

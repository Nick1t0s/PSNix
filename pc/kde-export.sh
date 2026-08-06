#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-KDE}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v konsave >/dev/null 2>&1; then
  echo "konsave не установлен. Установите: pipx install konsave" >&2
  exit 1
fi

konsave -s "$NAME" -f
konsave -e "$NAME" -d "$DIR" -n "$NAME" -f
echo "Снимок сохранён: $DIR/$NAME.knsv"

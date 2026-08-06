#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-KDE}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILE="$DIR/$NAME.knsv"

if ! command -v konsave >/dev/null 2>&1; then
  echo "konsave не установлен. Установите: pipx install konsave" >&2
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "Файл снимка не найден: $FILE" >&2
  exit 1
fi

konsave -r "$NAME" >/dev/null 2>&1 || true
konsave -i "$FILE"
konsave -a "$NAME"
echo "Снимок применён из: $FILE"
echo "Выйдите и войдите заново, чтобы изменения применились полностью."

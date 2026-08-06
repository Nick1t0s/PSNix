#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-KDE}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILE="$DIR/$NAME.knsv"
WALLDIR="$DIR/wallpapers"
MANIFEST="$WALLDIR/paths.txt"

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

# ---- обои: раскладываем по манифесту и чиним пути в конфигах ----
if [ -f "$MANIFEST" ]; then
  mkdir -p "$HOME/Pictures"
  while IFS=$'\t' read -r id orig; do
    [ -n "$id" ] || continue
    src="$WALLDIR/$id-$(basename "$orig")"
    if [ ! -f "$src" ]; then
      echo "Файл обоев не найден: $src" >&2
      continue
    fi
    new="$HOME/Pictures/$(basename "$orig")"
    cp -f "$src" "$new"
    new="${new//&/\\&}"
    for rc in "$HOME/.config/plasma-org.kde.plasma.desktop-appletsrc" "$HOME/.config/kscreenlockerrc"; do
      [ -f "$rc" ] && sed -i "s|$orig|$new|g" "$rc"
    done
  done < "$MANIFEST"
  echo "Обои восстановлены в ~/Pictures, пути в конфигах обновлены."
else
  echo "Манифест обоев не найден: $MANIFEST (пропускаю обои)" >&2
fi

echo "Снимок применён из: $FILE"
echo "Выйдите и войдите заново, чтобы изменения применились полностью."

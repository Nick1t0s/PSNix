#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-KDE}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WALLDIR="$DIR/wallpapers"
MANIFEST="$WALLDIR/paths.txt"

if ! command -v konsave >/dev/null 2>&1; then
  echo "konsave не установлен. Установите: pipx install konsave" >&2
  exit 1
fi

rm -rf "$WALLDIR"
mkdir -p "$WALLDIR"

declare -A seen
i=0
for rc in "$HOME/.config/plasma-org.kde.plasma.desktop-appletsrc" "$HOME/.config/kscreenlockerrc"; do
  [ -f "$rc" ] || continue
  while read -r path; do
    [ -n "$path" ] || continue
    case "$path" in file://*) path="${path#file://}" ;; esac
    [ -f "$path" ] || continue
    [ "${seen[$path]+x}" ] && continue
    seen[$path]=1
    i=$((i+1))
    cp -f "$path" "$WALLDIR/$i-$(basename "$path")"
    printf '%s\t%s\n' "$i" "$path" >> "$MANIFEST"
  done < <(grep -E '^(Image|PreviewImage)=' "$rc" | sed 's/^[^=]*=//')
done

konsave -s "$NAME" -f
konsave -e "$NAME" -d "$DIR" -n "$NAME" -f
echo "Снимок сохранён: $DIR/$NAME.knsv"
echo "Сохранено обоев: $i -> $WALLDIR"

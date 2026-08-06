#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-KDE}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILE="$DIR/$NAME.knsv"
WALLDIR="$DIR/wallpapers"
MANIFEST="$WALLDIR/paths.txt"

# ---- живая сессия Plasma? ----
LIVE=0
pgrep -x plasmashell >/dev/null 2>&1 && LIVE=1
pgrep -x kwin_wayland >/dev/null 2>&1 && LIVE=1
pgrep -x kwin_x11 >/dev/null 2>&1 && LIVE=1

if [ "$LIVE" -eq 1 ] && [ "${KDE_RESTORE_LIVE:-0}" != 1 ]; then
  echo "ОШИБКА: запущена живая сессия Plasma (plasmashell/kwin)." >&2
  echo "Применение поверх живой сессии ненадёжно: Plasma держит старый конфиг" >&2
  echo "в памяти, изменения на экране не появятся, а при выходе старый конфиг" >&2
  echo "может перезаписать свежий." >&2
  echo "" >&2
  echo "Как сделать правильно:" >&2
  echo "  1) выйдите из сессии (к экрану входа);" >&2
  echo "  2) перейдите в TTY: Ctrl+Alt+F2 (или F3-F6);" >&2
  echo "  3) войдите под своим пользователем и выполните:" >&2
  echo "     $DIR/kde-restore.sh $NAME" >&2
  echo "  4) вернитесь в графику: Ctrl+Alt+F1 и войдите." >&2
  echo "" >&2
  echo "Если всё же нужно применить прямо в живой сессии (обои/панель — сразу," >&2
  echo "виртуальные столы — только после перезапуска KWin):" >&2
  echo "  KDE_RESTORE_LIVE=1 $DIR/kde-restore.sh $NAME" >&2
  exit 1
fi

if ! command -v konsave >/dev/null 2>&1; then
  echo "konsave не установлен. Установите: pipx install konsave" >&2
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "Файл снимка не найден: $FILE" >&2
  exit 1
fi

# В живой сессии сначала корректно останавливаем plasmashell, чтобы он не
# записал обратно свой старый конфиг поверх только что применённого.
if [ "$LIVE" -eq 1 ]; then
  echo "Останавливаю plasmashell..."
  kquitapp6 plasmashell 2>/dev/null || true
  i=0
  while pgrep -x plasmashell >/dev/null 2>&1 && [ "$i" -lt 50 ]; do
    sleep 0.2
    i=$((i+1))
  done
  if pgrep -x plasmashell >/dev/null 2>&1; then
    echo "plasmashell не завершился, продолжаю..." >&2
  fi
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

# В живой сессии поднимаем plasmashell заново, чтобы он прочитал новые конфиги.
if [ "$LIVE" -eq 1 ]; then
  systemctl --user start plasma-plasmashell.service 2>/dev/null || true
  if ! pgrep -x plasmashell >/dev/null 2>&1; then
    setsid plasmashell >/dev/null 2>&1 &
    disown || true
  fi
  echo "plasmashell перезапущен — обои и панель применены сразу."
  echo "Виртуальные столы (kwinrc) подхватятся только после полного выхода/входа"
  echo "или перезапуска KWin: systemctl --user restart plasma-kwin_wayland.service."
else
  echo "Сессия Plasma не запущена — всё применится при следующем входе в систему."
fi

echo "Снимок применён из: $FILE"
echo "Выйдите и войдите заново, чтобы изменения применились полностью."

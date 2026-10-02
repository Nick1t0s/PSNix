#!/usr/bin/env bash
# Яркость мониторов из кэша (пишется brightness-change.sh по хоткеям/скроллу).
# ПОСТОЯННЫЙ ddcutil-ОПРОС ЗАПРЕЩЁН: DDC/CI по I²C на NVIDIA = микрофризы
# каждые ~5 сек (в т.ч. при записи OBS). Модуль обновляется по SIGRTMIN+7.
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/waybar-brightness"
hp=$(cat "$CACHE/HPN" 2>/dev/null); [ -n "$hp" ] || hp="?"
aus=$(cat "$CACHE/AUS" 2>/dev/null); [ -n "$aus" ] || aus="?"
icon=$(printf '\uf0eb')
printf '{"text": "%s %s%%", "tooltip": "Основной: %s%%\\nДополнительный: %s%%"}\n' "$icon" "$hp" "$hp" "$aus"

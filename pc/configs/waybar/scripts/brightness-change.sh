#!/usr/bin/env bash
# Изменение яркости мониторов через DDC/CI + запись кэша для waybar-модуля.
# ddcutil по I²C на NVIDIA вызывает микрофризы — вызывать ТОЛЬКО по нажатию
# (хоткеи hyprland.conf / скролл в waybar). Постоянный опрос запрещён:
# waybar-модуль brightness.sh читает только кэш.
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/waybar-brightness"
mkdir -p "$CACHE"
delta="${1:-+5}"
for mon in HPN AUS; do
    cur=$(cat "$CACHE/$mon" 2>/dev/null)
    if [ -z "$cur" ]; then
        cur=$(ddcutil -t -g "$mon" getvcp 10 2>/dev/null | awk '$2==10 {print $4}')
        [ -n "$cur" ] || cur=50
    fi
    new=$((cur + delta))
    ((new < 0)) && new=0
    ((new > 100)) && new=100
    ddcutil -t -g "$mon" setvcp 10 "$new" 2>/dev/null
    echo "$new" > "$CACHE/$mon"
done
pkill -SIGRTMIN+7 -x waybar 2>/dev/null

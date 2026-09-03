#!/usr/bin/env bash
# Яркость мониторов через DDC/CI: text — основной (HP), tooltip — оба
hp=$(ddcutil -t -g HPN getvcp 10 2>/dev/null | awk '$2==10 {print $4}')
aus=$(ddcutil -t -g AUS getvcp 10 2>/dev/null | awk '$2==10 {print $4}')
[ -n "$hp" ] || hp="?"
[ -n "$aus" ] || aus="?"
icon=$(printf '\uf0eb')
printf '{"text": "%s %s%%", "tooltip": "Основной: %s%%\\nДополнительный: %s%%"}\n' "$icon" "$hp" "$hp" "$aus"

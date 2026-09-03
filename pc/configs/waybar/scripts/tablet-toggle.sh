#!/usr/bin/env bash
# Переключение области планшета XP-Pen между мониторами
CFG="$HOME/.config/hypr/hyprland.conf"
REPO="/home/nik/PSNix/pc/configs/hypr/hyprland.conf"

cur=$(sed -n '/name = xppen-deco-01-v3-pen/,/^}/s/.*output *= *//p' "$CFG" | head -1)
if [ "$cur" = "HDMI-A-1" ]; then
    next="DP-3"; next_t="0"
else
    next="HDMI-A-1"; next_t="1"
fi

for f in "$CFG" "$REPO"; do
    [ -f "$f" ] || continue
    sed -i "/name = xppen-deco-01-v3-pen/,/^}/s/output *=.*/output = $next/" "$f"
    sed -i "/name = xppen-deco-01-v3-pen/,/^}/s/transform *=.*/transform = $next_t/" "$f"
done

hyprctl reload >/dev/null 2>&1
pkill -SIGRTMIN+8 -x waybar 2>/dev/null
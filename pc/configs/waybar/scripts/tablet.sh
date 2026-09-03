#!/usr/bin/env bash
# Виджет планшета: показывает, к какому монитору привязан XP-Pen
CFG="$HOME/.config/hypr/hyprland.conf"
cur=$(sed -n '/name = xppen-deco-01-v3-pen/,/^}/s/.*output *= *//p' "$CFG" | head -1)
case "$cur" in
    HDMI-A-1) label="HDMI"; tip="Планшет: вертикальный (HDMI-A-1). Клик — переключить на главный";;
    *)        label="DP";   tip="Планшет: главный (DP-3). Клик — переключить на вертикальный";;
esac
icon=$(printf '\uf1fc')
printf '{"text": "%s %s", "tooltip": "%s"}\n' "$icon" "$label" "$tip"
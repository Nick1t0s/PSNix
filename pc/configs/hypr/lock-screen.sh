#!/usr/bin/env bash
# Блокировка: гасим доп-монитор и центрируем главный; после разблокировки возвращаем всё
MAIN_LINE="DP-3,1920x1200@60,1200x720,1"
MAIN_LOCK="DP-3,1920x1200@60,0x0,1"
SEC_LINE="HDMI-A-1,1920x1200@59.95,0x0,1,transform,1"

restore() {
    # сначала уводим главный в его рабочую позицию, чтобы включаемый HDMI не перекрывался с ним
    hyprctl keyword monitor "$MAIN_LINE" >/dev/null 2>&1
    hyprctl keyword monitor "$SEC_LINE" >/dev/null 2>&1
    hyprctl dispatch dpms on >/dev/null 2>&1
    # hyprpaper не переприменяет обои после toggle мониторов — перезапускаем
    systemctl --user restart hyprpaper.service >/dev/null 2>&1
}
trap restore EXIT

pidof hyprlock >/dev/null 2>&1 && exit 0
hyprctl keyword monitor "HDMI-A-1,disable" >/dev/null 2>&1
hyprctl keyword monitor "$MAIN_LOCK" >/dev/null 2>&1
hyprlock

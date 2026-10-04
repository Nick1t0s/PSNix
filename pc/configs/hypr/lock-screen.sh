#!/usr/bin/env bash
# Блокировка: гасим доп-монитор через DPMS, после разблокировки включаем.
# Не disable: тогда HDMI пропадает из Hyprland, и если выключить DP-3 кнопкой, мониторов не остаётся —
# Hyprland заводит виртуальный FALLBACK со столом 11+ и после включения отдаёт этот стол DP-3.
# Проверка до trap: повторный вызов во время блокировки не должен включать HDMI
pidof hyprlock >/dev/null 2>&1 && exit 0

restore() {
    hyprctl dispatch dpms on >/dev/null 2>&1
    # hyprpaper не переприменяет обои после переподключения монитора — перезапускаем
    systemctl --user restart hyprpaper.service >/dev/null 2>&1
}
trap restore EXIT

hyprctl dispatch dpms off HDMI-A-1 >/dev/null 2>&1
hyprlock

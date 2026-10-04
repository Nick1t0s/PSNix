#!/usr/bin/env bash
# Меню питания через wofi: выбор действия вместо мгновенного выхода из сессии
choice=$(printf '%s\n' "Lock" "Logout" "Reboot" "Shutdown" \
    | wofi --dmenu --prompt "Power" --width 220 --height 190 --cache-file /dev/null)

case "$choice" in
    Lock)     ~/.local/bin/lock-screen ;;
    Logout)   hyprctl dispatch exit ;;
    Reboot)   systemctl reboot ;;
    Shutdown) systemctl poweroff ;;
esac

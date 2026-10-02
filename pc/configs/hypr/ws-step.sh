#!/usr/bin/env bash
# Шаг по рабочим столам внутри текущего монитора: на границе (10 <-> 11) ничего не делает.
# Использование: ws-step -1 | +1
cur=$(hyprctl activeworkspace -j | jq -r .id)
t=$((cur + $1))
if [ "$cur" -le 10 ]; then
  [ "$t" -ge 1 ] && [ "$t" -le 10 ] || exit 0
else
  [ "$t" -ge 11 ] || exit 0
fi
hyprctl dispatch workspace "$t"

#!/bin/bash

for hwmon in /sys/class/hwmon/hwmon*; do
    [ "$(cat "$hwmon/name" 2>/dev/null)" = "coretemp" ] || continue

    for label in "$hwmon"/temp*_label; do
        [ "$(cat "$label" 2>/dev/null)" = "Package id 0" ] || continue

        input="${label/_label/_input}"
        temp=$(cat "$input" 2>/dev/null)

        [ -n "$temp" ] || exit 1

        echo "$((temp / 1000))"
        exit 0
    done
done

#!/usr/bin/env bash
# LibreOffice в светлой теме Fluent (под Windows 11), остальные GTK-программы остаются в Breeze-Dark.
# Ярлыки /usr/share/applications/libreoffice-*.desktop зовут `libreoffice`, а ~/.local/bin первый в PATH.
# GTK_THEME без варианта = светлый, prefer-dark из gtk-3.0/settings.ini тогда не действует.
export GTK_THEME=Fluent-Light
exec /usr/bin/libreoffice "$@"

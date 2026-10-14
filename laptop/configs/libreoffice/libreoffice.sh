#!/usr/bin/env bash
# LibreOffice в светлой теме Fluent (под Windows 11), остальные GTK-программы остаются в Breeze-Dark.
# Ярлыки /usr/share/applications/libreoffice-*.desktop зовут `libreoffice`, а ~/.local/bin первый в PATH.
# GTK_THEME без варианта = светлый, prefer-dark из gtk-3.0/settings.ini тогда не действует.
export GTK_THEME=Fluent-Light
# gdk-pixbuf 2.44 грузит картинки через glycin 2.1.1, а тот роняет LO (abort) на иконках сайдбара Calc —
# LO получает свой gdk-pixbuf 2.42.12 без glycin (из Ubuntu 25.10, ставится по Шагу 11 доки 12).
# Без loaders.cache не подключаем: иначе системный gdk-pixbuf не найдёт SVG-загрузчик.
pixbuf=$HOME/.local/lib/libreoffice-pixbuf
if [ -e "$pixbuf/loaders.cache" ]; then
    export LD_LIBRARY_PATH="$pixbuf${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
    export GDK_PIXBUF_MODULE_FILE="$pixbuf/loaders.cache"
fi
exec /usr/bin/libreoffice "$@"

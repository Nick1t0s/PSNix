# 12 — Hyprland и Waybar (окружение)

> Wayland-композитор Hyprland, статус-бар Waybar, терминальный файл-пикер
> (yazi в диалогах) и восстановление конфигов из `laptop/configs/` и `pc/configs/` этого репозитория.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Пакеты Wayland-стека

```bash
sudo apt install -y \
  hyprland hypridle hyprlock hyprpaper waybar wofi kitty \
  xdg-desktop-portal-gtk xdg-desktop-portal-hyprland \
  brightnessctl playerctl pavucontrol wireplumber \
  grim slurp
```

- `hypridle` — idle-демон (лок через 5 минут, выключение монитора)
- `hyprlock` — экран блокировки, `hyprpaper` — обои
- `waybar` — статус-бар, `wofi` — меню приложений, `kitty` — терминал
- `brightnessctl`, `playerctl`, `wireplumber` — клавиши яркости/медиа/громкости
- `grim`, `slurp` — скриншоты (PrtScrn / Shift+PrtScrn)

---

## Шаг 2 — Копирование конфигов

Конфиги лежат в `laptop/configs/` (ноутбук) и `pc/configs/` (ПК, два экрана:
главный 1920x1200 с waybar + вертикальный 1200x1920, повёрнутый на 90°).
Ниже — копирование для текущего хоста (подставь `laptop` или `pc` вместо `$HOST`).
Существующие конфиги перед заменой бэкапятся в `*.bak` вручную:
`cp ~/.config/hypr/hyprland.conf{,.bak}`.

```bash
cp -v $HOST/configs/hypr/hyprland.conf          ~/.config/hypr/hyprland.conf
cp -v $HOST/configs/hypr/hypridle.conf          ~/.config/hypr/hypridle.conf
cp -v $HOST/configs/hypr/hyprlock.conf          ~/.config/hypr/hyprlock.conf
cp -v $HOST/configs/hypr/hyprpaper.conf         ~/.config/hypr/hyprpaper.conf
cp -v $HOST/configs/waybar/hyprland-config      ~/.config/waybar/hyprland-config
cp -v $HOST/configs/waybar/hyprland-style.css   ~/.config/waybar/hyprland-style.css
cp -v $HOST/configs/waybar/scripts/cpu-temp.sh  ~/.config/waybar/scripts/cpu-temp.sh
cp -v $HOST/configs/waybar/scripts/powermenu.sh ~/.config/waybar/scripts/powermenu.sh
mkdir -p ~/.config/wofi   # тёмная минималистичная тема wofi (у laptop пока та же, что у pc)
cp -v $HOST/configs/wofi/config                 ~/.config/wofi/config
cp -v $HOST/configs/wofi/style.css              ~/.config/wofi/style.css
chmod +x ~/.config/waybar/scripts/cpu-temp.sh ~/.config/waybar/scripts/powermenu.sh
```

`powermenu.sh` — меню питания на кнопке waybar (Lock / Logout / Reboot / Shutdown через `wofi --dmenu`)
вместо мгновенного выхода из сессии. Lock на ПК вызывает `lock-screen` (13, Часть 6), на ноуте `hyprlock`.

**Тёмная тема** (Breeze-Dark для GTK, BreezeDark для Qt/KDE-программ):

```bash
sudo apt install -y breeze-gtk-theme breeze-cursor-theme kf6-breeze-icon-theme
mkdir -p ~/.config/gtk-3.0 ~/.config/gtk-4.0
cp -v $HOST/configs/gtk-3.0/settings.ini        ~/.config/gtk-3.0/settings.ini
cp -v $HOST/configs/gtk-4.0/settings.ini        ~/.config/gtk-4.0/settings.ini
cp -v $HOST/configs/kdeglobals                  ~/.config/kdeglobals
gsettings set org.gnome.desktop.interface color-scheme prefer-dark   # GTK4/libadwaita смотрят сюда, а не в settings.ini
gsettings set org.gnome.desktop.interface gtk-theme Breeze-Dark
gsettings set org.gnome.desktop.interface icon-theme breeze
```

> На ПК имена портов мониторов (`DP-1`/`DP-2` в конфиге) проверь через
> `hyprctl monitors` и поправь при необходимости.

> Графический планшет (XP-Pen Deco 01 V3, ПК): помимо этого шага нужен override
> libwacom и waybar-скрипты виджета — см. «13 — Только для ПК», Часть 3.

---

## Шаг 3 — Waybar через systemd (авто-перезапуск)

В `hyprland.conf`: `exec-once = systemctl --user restart waybar-hyprland.service`.
Пакетный `waybar.service` замаскировать (он привязан к `graphical-session.target`
и стартует с дефолтным конфигом), вместо него — свой юнит с `Restart=on-failure`:

```bash
systemctl --user mask waybar.service
mkdir -p ~/.config/systemd/user
cp -v $HOST/configs/systemd/user/waybar-hyprland.service ~/.config/systemd/user/waybar-hyprland.service
systemctl --user daemon-reload
systemctl --user restart waybar-hyprland.service
```

Проверка: `systemctl --user status waybar-hyprland.service` (active) и `pgrep -a waybar`.

Файлы waybar: `hyprland-config` (JSON-конфиг модулей), `hyprland-style.css` (стиль),
`scripts/cpu-temp.sh` (температура CPU Package, модуль `custom/cpu-temp`, опрос раз в 5 сек).

> **Двойной hypridle**: новые Ubuntu поставляют `hypridle.service` включённым
> (глобальный пресет), а `hyprland.conf` уже запускает hypridle через `exec-once` —
> получаются два экземпляра с двойными таймерами (двойной лок/гашение экрана).
> Дистровский юнит маскируется в user-scope (перекрывает global-пресет):
>
> ```bash
> systemctl --user mask hypridle.service
> systemctl --user stop hypridle.service
> pgrep -a hypridle   # должен остаться один экземпляр
> ```
>
> `hyprpaper.service` трогать не нужно — `hyprland.conf` сознательно стартует
> именно дистровский юнит (`exec-once = systemctl --user start hyprpaper.service`).

---

## Шаг 4 — Терминальный файл-пикер (yazi в диалогах)

Файловые диалоги приложений открываются в kitty с yazi (режим выбора:
**Enter** — выбрать, **Q** — отмена) через `xdg-desktop-portal-termfilechooser`.
Сборка из исходников в `~/.local` без root:

```bash
sudo apt install -y build-essential ninja-build meson pkg-config libinih-dev libsystemd-dev scdoc
git clone --depth 1 https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser /tmp/tfc-build
cd /tmp/tfc-build && meson setup build --prefix="$HOME/.local" && ninja -C build install
```

Конфиги порталов:

```bash
mkdir -p ~/.config/xdg-desktop-portal-termfilechooser \
         ~/.config/xdg-desktop-portal \
         ~/.config/environment.d
cp -v $HOST/configs/portals/termfilechooser/config          ~/.config/xdg-desktop-portal-termfilechooser/config
cp -v $HOST/configs/portals/xdg-desktop-portal/portals.conf ~/.config/xdg-desktop-portal/portals.conf
cp -v $HOST/configs/portals/environment.d/portal.conf       ~/.config/environment.d/portal.conf
systemctl --user restart xdg-desktop-portal.service
```

Проверка:

```bash
GDK_DEBUG=portals zenity --file-selection   # должна открыться kitty с yazi
```

#### Режим «Save As»

Ключевые опции конфига: `save_mode=suggested` — диалог сохранения стартует
в папке, которую предложило приложение (у браузера это папка загрузок),
а не в `$HOME` (значение `last` при первом запуске деградирует до
`default_dir`).

Портал сам создаёт файл-плейсхолдер с предложенным именем (`create_help_file=1`
по умолчанию) и открывает его в yazi. Workflow:

- **Enter** на плейсхолдере — сохранить с предложенным именем и путём
  (браузер перезапишет плейсхолдер содержимым скачивания);
- `r` (rename) или перемещение файла — задать своё имя/папку, затем **Enter**
  на файле с новым именем;
- **Q** — отмена, плейсхолдер удалится автоматически.

Внимание: выбор существующего файла и **Enter** перезапишет его — это
нормальное поведение любого save-диалога.

Проверка save-режима:

```bash
GDK_DEBUG=portals zenity --file-selection --save --filename="$HOME/test.txt"
```

Логи бэкенда: `journalctl --user -eu xdg-desktop-portal-termfilechooser`.

### «Показать в папке» → тоже yazi (org.freedesktop.FileManager1)

```bash
sudo apt install -y libdbus-1-dev
git clone --depth 1 https://github.com/boydaihungst/org.freedesktop.FileManager1.common /tmp/fm1-build
cd /tmp/fm1-build && meson setup build --prefix="$HOME/.local" && ninja -C build install
pkill dolphin   # dolphin держит имя org.freedesktop.FileManager1, пока запущен
```

Конфиг (`$HOST/configs/portals/filemanager1/config` содержит плейсхолдер `@PREFIX@`):

```bash
mkdir -p ~/.config/org.freedesktop.FileManager1.common
sed 's|@PREFIX@|'"$HOME"'/.local|' \
  $HOST/configs/portals/filemanager1/config > ~/.config/org.freedesktop.FileManager1.common/config
```

Проверка:

```bash
busctl --user call org.freedesktop.FileManager1 /org/freedesktop/FileManager1 \
  org.freedesktop.FileManager1 ShowItems as s 1 "file://$HOME/Downloads/файл" ""
```

> Приложения, игнорирующие портал, покажут свой диалог.

---

## Шаг 5 — Firefox и браузер по умолчанию

```bash
sudo apt install firefox -y
xdg-settings set default-web-browser firefox_firefox.desktop
```

В `about:config`:

- `widget.use-xdg-desktop-portal.file-picker = 1` — файловые диалоги в yazi
- `widget.use-xdg-desktop-portal.open-uri = 1` — «Показать в папке» в yazi

> На Ubuntu Firefox — snap, id десктоп-файла именно `firefox_firefox.desktop`.

---

## Шаг 6 — Zoom: нативный диалог вместо терминального пикера

Qt+CEF-клиент Zoom уходит в терминальный пикер, поэтому ему подкладывается
user-level `.desktop` (перекрывает системный и переживает обновления):

```bash
mkdir -p ~/.local/share/applications
```

Создай `~/.local/share/applications/Zoom.desktop`:

```ini
[Desktop Entry]
Name=Zoom Workplace
Comment=Zoom Video Conference
Exec=env QT_QPA_PLATFORMTHEME=gtk3 GTK_USE_PORTAL=0 /usr/bin/zoom %U
Icon=Zoom
Terminal=false
Type=Application
Encoding=UTF-8
Categories=Network;Application;
StartupWMClass=zoom
MimeType=x-scheme-handler/zoommtg;x-scheme-handler/zoomus;x-scheme-handler/tel;x-scheme-handler/callto;x-scheme-handler/zoomphonecall;x-scheme-handler/zoomphonesms;x-scheme-handler/zoomcontactcentercall;application/x-zoom
X-KDE-Protocols=zoommtg;zoomus;tel;callto;zoomphonecall;zoomphonesms;zoomcontactcentercall;
Name[en_US]=Zoom Workplace
```

```bash
update-desktop-database ~/.local/share/applications
```

---

## Шаг 7 — Настройка вручную

1. **Шрифт** `JetBrainsMono Nerd Font` (waybar/hyprlock): распакуй архивы
   Nerd Font в `~/.local/share/fonts/` и выполни `fc-cache -f`.
2. **Обои**: hyprpaper/hyprlock указывают на
   `~/Pictures/Mikasa_Ackerman_Aesthetic_Wallpaper_4K_Attack_on_Titan_Lockscreen.jpg`
   — положи файл (есть в `laptop/wallpapers/`) или поправь пути в конфигах.
3. **waybar** `on-click` ссылается на `~/.local/bin/rofi-bluetooth` и
   `~/.local/bin/rofi-wifi` — создай эти скрипты или замени команды.

---

## Шаг 8 — VM-оверрайд (VirtualBox / VMware)

На виртуалке софтовый рендерер (`llvmpipe`) не тянет blur/shadow/animations.
Подключи лёгкий конфиг:

```bash
cp -v $HOST/configs/hypr/vm.conf ~/.config/hypr/vm.conf
echo -e "\n# VM detected\nsource = ~/.config/hypr/vm.conf" >> ~/.config/hypr/hyprland.conf
```

Он отключает эффекты, ставит масштаб 1 и `WLR_NO_HARDWARE_CURSORS=1`. Проверка:

```bash
hyprctl getoption decoration:blur:enabled
hyprctl getoption animations:enabled
```

---

## Шаг 9 — Фикс краш-цикла DrKonqi (микрофризы каждые ~10 сек)

> Симптом: система периодически заикается каждые 7–10 секунд — в играх (CS),
> при рисовании на планшете в rnote и т.п. Причина: обработчик крашей KDE
> (`drkonqi-coredump-launcher`) сам сегфолтится; его падение пишется как новый
> coredump, системный `drkonqi-coredump-processor@` снова стартует лаунчер —
> бесконечный цикл (сотни крашей в час, каждый цикл — запись дампа на диск,
> спавн systemd-юнитов и journal-записи = микрофриз).
> Проверка: `coredumpctl list | tail` — дампы `drkonqi-coredump-launcher`
> каждые 10–25 сек.

```bash
# 1. Разорвать цикл: замаскировать юзерные юниты DrKonqi
systemctl --user mask \
  drkonqi-coredump-launcher.socket \
  drkonqi-coredump-launcher@.service \
  drkonqi-coredump-pickup.service \
  drkonqi-sentry-postman.path
systemctl --user stop \
  drkonqi-coredump-launcher.socket \
  drkonqi-coredump-pickup.service \
  drkonqi-sentry-postman.path

# 2. Убрать системный обработчик (он стартует лаунчер в обход сокета)
sudo systemctl disable --now drkonqi-coredump-processor@.service

# 3. Почистить накопившиеся дампы (могут занимать гигабайты)
sudo rm -rf /var/lib/systemd/coredump/*
```

Проверка: подождать минуту, `coredumpctl list --since "-5 min"` — пусто;
фризы исчезли (проверить в игре/на планшете).

> Диалоги «Приложение упало» от KDE больше не показываются — apport
> продолжает логировать краши (`journalctl`, `/var/crash`). Реальные краши
> приложений видны через `coredumpctl list` (systemd-coredump не трогали).

---

## Шаг 10 — LibreOffice: GTK3 под Wayland и вид «как MS Office»

> Симптом: LibreOffice открывается не на том мониторе и не того размера
> (на ПК окно Writer было размером с вертикальный монитор, а окно Calc вообще за пределами экрана).
> Причины: со времён Plasma стоит только Qt/KDE-вариант интерфейса (`libreoffice-kf6/qt6`),
> который под Hyprland ведёт себя хуже всего, а в профиле запомнилась битая
> геометрия окон (`ooSetupFactoryWindowAttributes`).

```bash
sudo apt install -y libreoffice-gtk3 fonts-crosextra-carlito fonts-crosextra-caladea
```

- `libreoffice-gtk3` — GTK3-вариант интерфейса, работает под Wayland без XWayland: Hyprland сам ставит окно
  на монитор с фокусом и сам задаёт ему размер
- `fonts-crosextra-carlito` / `-caladea` — шрифты с теми же размерами, что Calibri / Cambria: документы
  из Word открываются без съехавшей вёрстки

В `hyprland.conf` уже есть (Шаг 2 их ставит):

- `env = SAL_USE_VCLPLUGIN,gtk3` — принудительно GTK3-вариант (kf6/qt6 не удалены, на них можно откатиться);
- правило `libreoffice-tile` (`match:class = ^(libreoffice-.*|soffice)$`, `tile = yes`) — окно всегда
  в тайлинге, запомненный размер не мешает.

**Тема Fluent (Windows 11) только для LibreOffice.** Остальные GTK-программы остаются в Breeze-Dark:

```bash
git clone --depth 1 https://github.com/vinceliuice/Fluent-gtk-theme /tmp/fluent-build
/tmp/fluent-build/install.sh -d ~/.themes -c light -s standard   # → ~/.themes/Fluent-Light, без sudo/sassc
install -Dm755 $HOST/configs/libreoffice/libreoffice.sh ~/.local/bin/libreoffice
```

Обёртка задаёт `GTK_THEME=Fluent-Light` и запускает `/usr/bin/libreoffice`. Она работает потому, что
`~/.local/bin` стоит первым в PATH, а все ярлыки `libreoffice-*.desktop` вызывают просто `libreoffice`.

**Профиль** `~/.config/libreoffice/4/user/registrymodifications.xcu`. Профиль появляется после первого
запуска LibreOffice. Перед правкой LibreOffice должен быть полностью закрыт (`pgrep -a soffice` пусто),
иначе при выходе он перезапишет файл:

```bash
f=~/.config/libreoffice/4/user/registrymodifications.xcu
cp -p "$f" "$f.bak"
sed -i '/ooSetupFactoryWindowAttributes/d' "$f"           # сброс битой геометрии окон
p='<item oor:path="/org.openoffice.Office.Writer/DefaultFont"><prop oor:name='
sed -i 's#^</oor:items>$#<item oor:path="/org.openoffice.Office.Common/Misc"><prop oor:name="SymbolStyle" oor:op="fuse"><value>colibre</value></prop></item>\n'\
"$p"'"Standard" oor:op="fuse"><value>Carlito</value></prop></item>\n'\
"$p"'"StandardHeight" oor:op="fuse"><value>388</value></prop></item>\n'\
"$p"'"Heading" oor:op="fuse"><value>Carlito</value></prop></item>\n'\
"$p"'"List" oor:op="fuse"><value>Carlito</value></prop></item>\n'\
"$p"'"Caption" oor:op="fuse"><value>Carlito</value></prop></item>\n'\
"$p"'"Index" oor:op="fuse"><value>Carlito</value></prop></item>\n</oor:items>#' "$f"
python3 -I -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1]); print('XML OK')" "$f"
```

- `SymbolStyle = colibre` — плоские цветные значки в стиле MS Office (вместо Breeze)
- `DefaultFont` — в Writer по умолчанию Carlito 11 pt, как Calibri 11 в Word (`StandardHeight` в 1/100 мм:
  11 pt = 388)

**Лента (вручную, через профиль не задаётся):** View → User Interface… → **Tabbed** → **Apply to All**.
Через профиль меняется только `ToolbarMode/…/Active`, а старые панели и строка меню остаются,
и интерфейс получается двойным. Команда меню переключает всё сразу.

Проверка (открыть Writer через лаунчер, а не из старого терминала):

```bash
pid=$(pgrep -x soffice.bin)
tr '\0' '\n' < /proc/$pid/environ | grep -E '^(GTK_THEME|SAL_USE_VCLPLUGIN)='   # Fluent-Light, gtk3
grep -oE 'libvclplug_[a-z0-9]+lo\.so' /proc/$pid/maps | sort -u                 # libvclplug_gtk3lo.so
hyprctl clients | grep -A22 'class: libreoffice-writer' | grep -E 'xwayland|floating|monitor'   # 0 / 0 / монитор с фокусом
```

> Откат: удалить `~/.local/bin/libreoffice` (тема), убрать `SAL_USE_VCLPLUGIN` и `libreoffice-tile`
> из `hyprland.conf` + `hyprctl reload`, профиль вернуть из `.bak`,
> ленту — View → User Interface → Standard Toolbar → Apply to All.

---

## Шаг 11 — LibreOffice падает в Calc: свой gdk-pixbuf без glycin

> Симптом: Calc внезапно закрывается, когда входишь в ячейку для редактирования (чаще всего на реестре
> регистрации). После перезапуска предлагает восстановить документ, остаётся `.~lock.*#` рядом с файлом.
> Причина: при входе в ячейку сайдбар перестраивается и грузит иконку (`gtk_image_new_from_file`).
> gdk-pixbuf 2.44 грузит картинки только через glycin 2.1.1, а glycin держит процесс-загрузчик ~30 с
> и потом гасит его. Следующая загрузка после этого паникует внутри `gly_loader_load` → `abort`.
> Проверка: `coredumpctl list soffice.bin` — SIGABRT, в `coredumpctl info <PID>` стек
> `gly_loader_load` ← `gdk_pixbuf_loader_close` ← `SidebarController::UpdateConfigurations`.

Выключить glycin в системном gdk-pixbuf переменной нельзя, а glycin 2.1.5 из `resolute-updates` по changelog
это не чинит. Поэтому только LibreOffice получает gdk-pixbuf 2.42.12 из Ubuntu 25.10 (последний без glycin).
Системные пакеты не трогаются. Сборка Debian не подходит: она слинкована с `libjpeg.so.62`, а в Ubuntu
есть только `libjpeg.so.8`.

Из корня репо:

```bash
install -Dm755 $HOST/configs/libreoffice/libreoffice.sh ~/.local/bin/libreoffice   # обёртка из Шага 10
m=http://archive.ubuntu.com/ubuntu   # когда 25.10 уберут из архива — http://old-releases.ubuntu.com/ubuntu
deb=libgdk-pixbuf-2.0-0_2.42.12+dfsg-5ubuntu0.1_amd64.deb
cd "$(mktemp -d)"

# 1. Скачать и проверить: подпись InRelease → хеш Packages.xz → хеш .deb
curl -fsSO $m/dists/questing-updates/InRelease
curl -fsSO $m/dists/questing-updates/main/binary-amd64/Packages.xz
curl -fsSO $m/pool/main/g/gdk-pixbuf/$deb
gpgv --keyring /usr/share/keyrings/ubuntu-archive-keyring.gpg InRelease          # Good signature
grep -q " $(sha256sum Packages.xz | cut -c1-64) .*main/binary-amd64/Packages.xz$" InRelease && echo "Packages OK"
xz -dc Packages.xz | grep -A6 "^Filename: .*/$deb$" | grep -q "^SHA256: $(sha256sum $deb | cut -c1-64)$" && echo "deb OK"

# 2. Распаковать без скриптов пакета в ~/.local/lib/libreoffice-pixbuf
dpkg-deb -x $deb x
p=~/.local/lib/libreoffice-pixbuf; l=x/usr/lib/x86_64-linux-gnu
mkdir -p $p/loaders
cp -a $l/libgdk_pixbuf-2.0.so.0* $l/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders $p/
cp -a $l/gdk-pixbuf-2.0/2.10.0/loaders/*.so $p/loaders/
ldd $p/libgdk_pixbuf-2.0.so.0 | grep 'not found'                                 # пусто

# 3. Кеш загрузчиков: старые + системный SVG (librsvg); PNG и JPEG встроены в саму библиотеку
LD_LIBRARY_PATH=$p $p/gdk-pixbuf-query-loaders $p/loaders/*.so \
  /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader_svg.so > $p/loaders.cache
```

- Обёртка ставит `LD_LIBRARY_PATH` и `GDK_PIXBUF_MODULE_FILE` на этот каталог, только если в нём есть
  `loaders.cache`. Без кеша LibreOffice запускается как раньше: если указать системному gdk-pixbuf пустой
  кеш, он не найдёт SVG-загрузчик.
- Совместимость проверена: всё, что `libgtk-3`, `libgdk-3`, `libvclplug_gtk3lo`, `librsvg` и SVG-загрузчик
  импортируют из gdk-pixbuf, в 2.42.12 есть (`gdk_pixbuf_get_from_surface/window` — это функции `libgdk-3`).

Проверка (LibreOffice полностью закрыть и открыть заново через лаунчер):

```bash
pid=$(pgrep -x soffice.bin)
grep -oE '/[^ ]*(gdk_pixbuf-2\.0\.so|glycin)[^ ]*' /proc/$pid/maps | sort -u   # только ~/.local/lib/libreoffice-pixbuf/…, libglycin нет
coredumpctl list soffice.bin                                                  # после нескольких минут в Calc — новых SIGABRT нет
```

> Откат: `rm -r ~/.local/lib/libreoffice-pixbuf`, обёртка без кеша сама вернётся к системному gdk-pixbuf.
> Так же проверять, починили ли glycin после обновления: убрать каталог и поработать в Calc дольше минуты.

---

## Шаг 12 — War Thunder: Waybar поверх полноэкранной игры

> Симптом: в режиме «Полноэкранный» Waybar остаётся видна поверх игры.
> Причина: игра (нативный Linux-клиент, окно через XWayland) просто растягивает обычное окно на весь
> монитор и не просит fullscreen. Для Hyprland это плавающее окно (`fullscreen: 0`), а слой `top`,
> на котором стоит Waybar, рисуется поверх всего, кроме настоящих fullscreen-окон.

В `hyprland.conf` уже есть (Шаг 2 его ставит) правило `warthunder-fullscreen` с `fullscreen = yes`.
Оно матчит окно по `initial_class` / `initial_title` = `Loading...` + `xwayland = true`. Такой class
у окна при открытии, потом игра меняет его на `War Thunder (Vulkan, 64bit)`. `fullscreen` — статичный
эффект, проверяется только при открытии, поэтому матч по текущему class не сработал бы.

Проверка (игру перезапустить из лаунчера, правило срабатывает только при открытии окна):

```bash
hyprctl clients -j | python3 -I -c 'import json,sys; [print(c["class"], c["initialClass"], c["fullscreen"]) for c in json.load(sys.stdin) if c["xwayland"]]'
# War Thunder (Vulkan, 64bit) Loading... 2
```

Если после обновления игры Waybar вернулась, посмотреть фактический `initialClass` той же командой
и поправить матчер.

> Откат: убрать блок `warthunder-fullscreen` из `hyprland.conf` (Hyprland перечитает сам или `hyprctl reload`).

---

## Горячие клавиши (основные)

- `Super+R` — меню приложений (wofi), `Super+E` — kitty + yazi
- `Super+Escape` — блокировка (hyprlock), `Ctrl+Alt+T` — терминал
  (`Ctrl+Alt+L` не занят: в PyCharm/CLion это «слово вправо», см. доку 02, Шаг 9)
- `PrtScrn` — скриншот области, `Shift+PrtScrn` — весь экран
- `Super+H/J/K/L` — фокус, `Super+Ctrl+H/J/K/L` — перемещение, `Super+Shift+H/J/K/L` — resize
- `Super+1..0` — воркспейсы, `Ctrl+Super+←/→` — переключение
- `Super+Space` — раскладка (`grp:win_space_toggle`)

---

## Ссылки

- [Hyprland Wiki](https://wiki.hypr.land/Configuring/)
- [Waybar Wiki](https://github.com/Alexays/Waybar/wiki)
- [Yazi — chooser mode](https://yazi-rs.github.io/docs/usage/chooser/)
- [xdg-desktop-portal-termfilechooser](https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser)
- [org.freedesktop.FileManager1.common](https://github.com/boydaihungst/org.freedesktop.FileManager1.common)
- [XDG Desktop Portal (ArchWiki)](https://wiki.archlinux.org/title/XDG_Desktop_Portal)

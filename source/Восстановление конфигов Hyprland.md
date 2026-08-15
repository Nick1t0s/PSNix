# Восстановление конфигов Hyprland/waybar/порталов

> Авто-копирование конфигов (`copy_configs`) и установка Wayland-стека
> (`install_wayland`) удалены из установщика. Все конфиги лежат в `configs/`
> этого репозитория — ниже, как вернуть их вручную на свежую систему.

---

## 1. Пакеты Wayland-стека

```bash
sudo apt install -y \
  hyprland hypridle hyprlock hyprpaper waybar wofi kitty \
  xdg-desktop-portal-gtk xdg-desktop-portal-hyprland \
  brightnessctl playerctl pavucontrol wireplumber \
  grim slurp
```

---

## 2. Копирование конфигов

Единый конфиг (laptop = PC, разделения на варианты нет):

```bash
cp -v configs/hypr/hyprland.conf          ~/.config/hypr/hyprland.conf
cp -v configs/hypr/hypridle.conf          ~/.config/hypr/hypridle.conf
cp -v configs/hypr/hyprlock.conf          ~/.config/hypr/hyprlock.conf
cp -v configs/hypr/hyprpaper.conf         ~/.config/hypr/hyprpaper.conf
cp -v configs/waybar/hyprland-config      ~/.config/waybar/hyprland-config
cp -v configs/waybar/hyprland-style.css   ~/.config/waybar/hyprland-style.css
cp -v configs/waybar/scripts/cpu-temp.sh  ~/.config/waybar/scripts/cpu-temp.sh
chmod +x ~/.config/waybar/scripts/cpu-temp.sh
```

Существующие конфиги перед заменой бэкапятся в `*.bak` (раньше это делал скрипт,
теперь вручную: `cp ~/.config/hypr/hyprland.conf{,.bak}`).

---

## 3. Восстановление терминального файл-пикера (yazi в диалогах)

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

cp -v configs/portals/termfilechooser/config ~/.config/xdg-desktop-portal-termfilechooser/config
cp -v configs/portals/xdg-desktop-portal/portals.conf ~/.config/xdg-desktop-portal/portals.conf
cp -v configs/portals/environment.d/portal.conf ~/.config/environment.d/portal.conf
```

Перезапуск порталов:

```bash
systemctl --user restart xdg-desktop-portal.service
```

> В `hyprland.conf` та же переменная задана как `env = GTK_USE_PORTAL,1`.

---

## 4. «Показать в папке» → yazi (org.freedesktop.FileManager1)

```bash
sudo apt install -y libdbus-1-dev
git clone --depth 1 https://github.com/boydaihungst/org.freedesktop.FileManager1.common /tmp/fm1-build
cd /tmp/fm1-build && meson setup build --prefix="$HOME/.local" && ninja -C build install
pkill dolphin   # если запущен
```

Конфиг (`configs/portals/filemanager1/config` содержит плейсхолдер `@PREFIX@`,
замените его на `$HOME/.local`):

```bash
mkdir -p ~/.config/org.freedesktop.FileManager1.common
sed 's|@PREFIX@|'"$HOME"'/.local|' \
  configs/portals/filemanager1/config > ~/.config/org.freedesktop.FileManager1.common/config
```

---

## 5. Firefox — браузер по умолчанию

```bash
xdg-settings set default-web-browser firefox_firefox.desktop
```

или через `gio`:

```bash
gio mime x-scheme-handler/https firefox_firefox.desktop
```

Проверка: `xdg-settings get default-web-browser`.

---

## 6. Zoom — нативный диалог вместо терминального пикера

Qt+CEF-клиент Zoom уходит в терминальный пикер, поэтому ему подкладывается
user-level `.desktop` (перекрывает системный и переживает обновления):

```bash
mkdir -p ~/.local/share/applications
```

Создайте `~/.local/share/applications/Zoom.desktop` со следующим содержимым:

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

## 7. Всё, что нужно настроить вручную

1. **Шрифт** `JetBrainsMono Nerd Font` (waybar/hyprlock): распакуйте архивы Nerd
   Font в `~/.local/share/fonts/` и выполните `fc-cache -f`.
2. **Firefox**: `about:config` →
   `widget.use-xdg-desktop-portal.file-picker = 1` (файловые диалоги — yazi) и
   `widget.use-xdg-desktop-portal.open-uri = 1` («Показать в папке»).
3. **Обои**: hyprpaper/hyprlock указывают на
   `~/Pictures/Mikasa_Ackerman_Aesthetic_Wallpaper_4K_Attack_on_Titan_Lockscreen.jpg`
   — положите файл или поправьте пути в `hyprpaper.conf` / `hyprlock.conf`.
4. **waybar** `on-click` ссылается на `~/.local/bin/rofi-bluetooth` и
   `~/.local/bin/rofi-wifi` — создайте эти скрипты или замените команды.

---

## 8. VM-оверрайд (VirtualBox / VMware)

На виртуалке софтовый рендерер (`llvmpipe`) не тянет blur/shadow/animations.
Подключите лёгкий конфиг `configs/hypr/vm.conf` в конец hyprland.conf:

```bash
cp -v configs/hypr/vm.conf ~/.config/hypr/vm.conf
echo -e "\n# VM detected\nsource = ~/.config/hypr/vm.conf" >> ~/.config/hypr/hyprland.conf
```

Он отключает эффекты, ставит масштаб 1 и `WLR_NO_HARDWARE_CURSORS=1`.
Проверка:

```bash
hyprctl getoption decoration:blur:enabled
hyprctl getoption animations:enabled
```

---

## Ссылки

- [Hyprland Wiki](https://wiki.hypr.land/Configuring/)
- [Waybar](https://github.com/Alexays/Waybar)
- [Yazi](https://yazi-rs.github.io/)
- [xdg-desktop-portal-termfilechooser](https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser)
- [org.freedesktop.FileManager1.common](https://github.com/boydaihungst/org.freedesktop.FileManager1.common)
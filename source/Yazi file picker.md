# Yazi как файловый пикер в диалогах (xdg-desktop-portal-termfilechooser)

> Файловые диалоги приложений (открыть/сохранить/выбор папки) открываются
> в терминале с yazi вместо стандартного GTK-диалога. Установку делает
> фаза `install_wayland` (сборка termfilechooser), конфиги кладёт фаза
> `copy_configs` — запуск: `sudo -E python3 install.py --host pc|laptop`.

> **Исключение — Zoom**: Qt+CEF-клиент Zoom уходит в терминальный пикер,
> поэтому фаза `copy_configs` создаёт `~/.local/share/applications/Zoom.desktop`
> с `Exec=env QT_QPA_PLATFORMTHEME=gtk3 GTK_USE_PORTAL=0 ...` — у Zoom
> остаётся нативный диалог.

---

## Как это работает

1. Приложение запрашивает файл через XDG Desktop Portal (интерфейс `FileChooser`).
2. Бэкенд `xdg-desktop-portal-termfilechooser` (в `~/.local/libexec`) запускает
   обёртку `yazi-wrapper.sh`.
3. Обёртка открывает kitty с `yazi --chooser-file=/tmp/...` — режим выбора.
4. В yazi **Enter** — выбрать файл (или папку/несколько), **Q** — отмена.
   Путь записывается в файл-приёмник, yazi закрывается, приложение получает файл.

## Установка (сборка из исходников)

В Ubuntu пакета нет, собирается в `~/.local` без root:

```bash
sudo apt install -y build-essential ninja-build meson libinih-dev libsystemd-dev scdoc
git clone --depth 1 https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser /tmp/tfc-build
cd /tmp/tfc-build && meson setup build --prefix="$HOME/.local" && ninja -C build install
```

## Конфиги (`configs/portals/`)

**`~/.config/xdg-desktop-portal-termfilechooser/config`**
```ini
[filechooser]
cmd=yazi-wrapper.sh
default_dir=$HOME
env=TERMCMD='kitty --title "filechooser"'
open_mode=suggested
save_mode=last
```

**`~/.config/xdg-desktop-portal/portals.conf`** — назначаем бэкенд для FileChooser:
```ini
[preferred]
default=gtk
org.freedesktop.impl.portal.FileChooser=termfilechooser
```

**`~/.config/environment.d/portal.conf`** — GTK-приложения идут через портал:
```
GTK_USE_PORTAL=1
```
(в Hyprland та же переменная задаётся `env = GTK_USE_PORTAL,1` в hyprland.conf)

## Что включить вручную

- **Firefox / LibreWolf**: `about:config` → `widget.use-xdg-desktop-portal.file-picker = 1`
- Chromium и большинство Wayland-приложений используют портал сами

## Проверка

```bash
systemctl --user restart xdg-desktop-portal.service
GDK_DEBUG=portals zenity --file-selection     # должна открыться kitty с yazi
```

Логи бэкенда: `journalctl --user -eu xdg-desktop-portal-termfilechooser`

## «Показать в папке» — тоже yazi (org.freedesktop.FileManager1)

«Show in folder» из менеджеров загрузок (Firefox/Chromium) использует D-Bus-интерфейс
`org.freedesktop.FileManager1`, а не FileChooser-портал. Чтобы он открывал yazi
с выделенным файлом, ставится сервис **org.freedesktop.FileManager1.common**
(тот же автор, что и у termfilechooser):

```bash
sudo apt install -y libdbus-1-dev
git clone --depth 1 https://github.com/boydaihungst/org.freedesktop.FileManager1.common /tmp/fm1-build
cd /tmp/fm1-build && meson setup build --prefix="$HOME/.local" && ninja -C build install
pkill dolphin   # dolphin держит имя org.freedesktop.FileManager1, пока запущен
```

Конфиг (`configs/portals/filemanager1/config`, в скрипте подставляется `$HOME/.local`):

```
cmd=$HOME/.local/share/org.freedesktop.FileManager1.common/yazi-wrapper.sh
```

- Сервис-файл в `~/.local/share/dbus-1/services/` приоритетнее системного
  `org.kde.dolphin.FileManager1.service` — при активации поднимется наш.
- Обёртка по умолчанию запускает `kitty --class yazi yazi <путь>` — файл выделен.
- Firefox: `about:config` → `widget.use-xdg-desktop-portal.open-uri = 1`
  (по умолчанию `2` тоже работает).
- Проверка:
  ```bash
  busctl --user call org.freedesktop.FileManager1 /org/freedesktop/FileManager1 \
    org.freedesktop.FileManager1 ShowItems as s 1 "file://$HOME/Downloads/файл" ""
  ```

## Ограничения

- Приложения, игнорирующие портал, покажут свой диалог.

## Ссылки

- [hunkyburrito/xdg-desktop-portal-termfilechooser](https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser)
- [boydaihungst/org.freedesktop.FileManager1.common](https://github.com/boydaihungst/org.freedesktop.FileManager1.common)
- [File Manager DBus Interface](https://www.freedesktop.org/wiki/Specifications/file-manager-interface/)
- [XDG Desktop Portal (ArchWiki)](https://wiki.archlinux.org/title/XDG_Desktop_Portal)
- [Yazi — chooser mode](https://yazi-rs.github.io/docs/usage/chooser/)

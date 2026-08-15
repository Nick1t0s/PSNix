# Hyprland — установка и настройка (Ubuntu)

> Установщик теперь ставит только пакеты (`install_packages`). Wayland-стек и
> копирование конфигов делаются вручную — полное руководство по восстановлению
> конфигов: **«Восстановление конфигов Hyprland.md»** в этой же папке.
> Команда запуска пакетной фазы: `sudo -E python3 tasks/install_packages.py`

---

## Шаг 1 — Пакеты (Wayland-стек, вручную)

```bash
sudo apt install -y \
  hyprland hypridle hyprlock hyprpaper waybar wofi kitty \
  xdg-desktop-portal-gtk xdg-desktop-portal-hyprland \
  brightnessctl playerctl pavucontrol wireplumber \
  grim slurp
```

- `hypridle` — idle-демон (лок через 5 минут, выключение монитора)
- `hyprlock` — экран блокировки
- `hyprpaper` — обои
- `waybar` — статус-бар (см. `Waybar.md`)
- `wofi` — меню приложений (`$menu` в hyprland.conf)
- `kitty` — терминал (`$terminal` и `$fileManager = kitty -e yazi`)
- `brightnessctl`, `playerctl`, `wireplumber` — клавиши яркости/медиа/громкости
- `grim`, `slurp` — скриншоты (PrtScrn / Shift+PrtScrn)

## Шаг 2 — Терминальный файл-пикер (yazi в диалогах)

Файловые диалоги приложений открываются в yazi через
`xdg-desktop-portal-termfilechooser` (подробности в `Yazi file picker.md`):

```bash
sudo apt install -y build-essential ninja-build meson libinih-dev libsystemd-dev scdoc
git clone --depth 1 https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser /tmp/tfc-build
cd /tmp/tfc-build && meson setup build --prefix="$HOME/.local" && ninja -C build install
```

## Шаг 3 — Конфиги (вручную)

Конфиги копируются из `configs/` в `~/.config/` (см. **«Восстановление
конфигов Hyprland.md»**). Существующие бэкапятся в `*.bak`:

| Куда | Что |
|---|---|
| `configs/hypr/` | `hyprland.conf`, `hypridle.conf`, `hyprlock.conf`, `hyprpaper.conf` |
| `configs/waybar/` | `hyprland-config`, `hyprland-style.css`, `scripts/cpu-temp.sh` |
| `configs/portals/` | конфиги терминального файл-пикера |

После установки:

```bash
systemctl --user restart xdg-desktop-portal.service
```

## Шаг 4 — Вручную

1. **Шрифт** `JetBrainsMono Nerd Font` (используют waybar и hyprlock):
   распакуйте архивы Nerd Font в `~/.local/share/fonts/` и выполните `fc-cache -f`.
2. **Firefox**: `about:config` → `widget.use-xdg-desktop-portal.file-picker = 1`
   (файловые диалоги будут открываться в yazi).
3. **Обои** hyprpaper/hyprlock указывают на `~/Pictures/...jpg` — поправьте путь под свои.

## Браузер по умолчанию

Назначить **Firefox** браузером по умолчанию можно так (дописывает секцию
`[Default Applications]` в `~/.config/mimeapps.list`):

```
x-scheme-handler/http=firefox_firefox.desktop
x-scheme-handler/https=firefox_firefox.desktop
x-scheme-handler/ftp=firefox_firefox.desktop
text/html=firefox_firefox.desktop
```

На Ubuntu Firefox и Chromium ставятся как snap — поэтому id десктоп-файла
`firefox_firefox.desktop` (а не `firefox.desktop`, которого в `/usr/share/applications`
нет). Хром — `chromium_chromium.desktop`.

Сменить вручную:

```bash
xdg-settings set default-web-browser firefox_firefox.desktop
# или
gio mime x-scheme-handler/https firefox_firefox.desktop
```

Проверка: `xdg-settings get default-web-browser`.

## Горячие клавиши (основные)

- `Super+R` — меню приложений (wofi)
- `Super+E` — файловый менеджер (kitty + yazi)
- `Ctrl+Alt+L` — блокировка (hyprlock)
- `PrtScrn` — скриншот области (grim+slurp → буфер), `Shift+PrtScrn` — весь экран
- `Ctrl+Alt+T` — терминал
- `Super+H/J/K/L` — фокус, `Super+Ctrl+H/J/K/L` — перемещение окна
- `Super+Shift+H/J/K/L` — resize окна
- `Super+1..0` — воркспейсы
- `Ctrl+Super+←/→` — переключение воркспейсов
- `Super+Space`-переключение раскладки (`grp:win_space_toggle`)

## Ссылки

- [Hyprland Wiki](https://wiki.hypr.land/Configuring/)
- [Waybar](https://github.com/Alexays/Waybar)
- [Yazi](https://yazi-rs.github.io/)

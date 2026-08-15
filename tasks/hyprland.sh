#!/usr/bin/env bash
# Hyprland: окружение + waybar + терминальный файл-пикер (yazi в диалогах).
# Хост (pc|laptop) приходит из PSNIX_HOST — его выставляет install.py.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
configs="$REPO_ROOT/configs"
host="${PSNIX_HOST:-laptop}"

# 1. Пакеты
sudo apt install -y \
  hyprland hypridle hyprlock hyprpaper waybar wofi kitty \
  xdg-desktop-portal-gtk xdg-desktop-portal-hyprland \
  brightnessctl playerctl pavucontrol wireplumber \
  grim slurp

# 2. Терминальный файл-пикер: xdg-desktop-portal-termfilechooser (yazi в диалогах)
sudo apt install -y build-essential ninja-build meson libinih-dev libsystemd-dev scdoc
if [ ! -x "$HOME/.local/libexec/xdg-desktop-portal-termfilechooser" ]; then
  rm -rf /tmp/tfc-build
  git clone --depth 1 https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser /tmp/tfc-build || exit 1
  ( cd /tmp/tfc-build && meson setup build --prefix="$HOME/.local" && ninja -C build install ) || exit 1
fi

# 2b. «Показать в папке» -> yazi: org.freedesktop.FileManager1.common
sudo apt install -y libdbus-1-dev
if [ ! -x "$HOME/.local/libexec/file_manager_dbus" ]; then
  rm -rf /tmp/fm1-build
  git clone --depth 1 https://github.com/boydaihungst/org.freedesktop.FileManager1.common /tmp/fm1-build || exit 1
  ( cd /tmp/fm1-build && meson setup build --prefix="$HOME/.local" && ninja -C build install ) || exit 1
fi
# Ubuntu не ставит сервис-файл (нет pkg-config systemd) — создаём сами
mkdir -p "$HOME/.local/share/dbus-1/services"
cat > "$HOME/.local/share/dbus-1/services/org.freedesktop.FileManager1.service" <<EOF
[D-BUS Service]
Name=org.freedesktop.FileManager1
Exec=$HOME/.local/libexec/file_manager_dbus
EOF
# Dolphin держит имя org.freedesktop.FileManager1, пока запущен — закрываем,
# чтобы «Показать в папке» активировался наш сервис (в ~/.local он имеет приоритет)
pkill dolphin 2>/dev/null || true

# 3. Конфиги из репозитория (с бэкапом существующих)
install_config() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -e "$dst" ] && [ ! -e "$dst.bak" ]; then
    cp -a "$dst" "$dst.bak"
  fi
  cp -a "$src" "$dst"
}

install_config "$configs/$host/hyprland.conf"                "$HOME/.config/hypr/hyprland.conf"
install_config "$configs/hypr/hypridle.conf"                 "$HOME/.config/hypr/hypridle.conf"
install_config "$configs/hypr/hyprlock.conf"                 "$HOME/.config/hypr/hyprlock.conf"
install_config "$configs/hypr/hyprpaper.conf"                "$HOME/.config/hypr/hyprpaper.conf"
install_config "$configs/$host/waybar/hyprland-config"       "$HOME/.config/waybar/hyprland-config"
install_config "$configs/waybar/hyprland-style.css"          "$HOME/.config/waybar/hyprland-style.css"
install_config "$configs/waybar/scripts/cpu-temp.sh"         "$HOME/.config/waybar/scripts/cpu-temp.sh"
install_config "$configs/portals/termfilechooser/config"     "$HOME/.config/xdg-desktop-portal-termfilechooser/config"
install_config "$configs/portals/xdg-desktop-portal/portals.conf" "$HOME/.config/xdg-desktop-portal/portals.conf"
install_config "$configs/portals/environment.d/portal.conf"  "$HOME/.config/environment.d/portal.conf"
install_config "$configs/portals/filemanager1/config"        "$HOME/.config/org.freedesktop.FileManager1.common/config"
sed -i "s|@PREFIX@|$HOME/.local|" "$HOME/.config/org.freedesktop.FileManager1.common/config"
chmod +x "$HOME/.config/waybar/scripts/cpu-temp.sh"

# 4. Перезапуск порталов, чтобы подхватился новый файл-пикер
systemctl --user restart xdg-desktop-portal.service || true

# 5. Firefox — браузер по умолчанию (на Ubuntu это snap: firefox_firefox.desktop)
touch "$HOME/.config/mimeapps.list"
set_default_mime() {
  local mime="$1" app="$2"
  if grep -q "^$mime=" "$HOME/.config/mimeapps.list" 2>/dev/null; then
    sed -i "s|^$mime=.*|$mime=$app|" "$HOME/.config/mimeapps.list"
  elif grep -q "^\[Default Applications\]" "$HOME/.config/mimeapps.list" 2>/dev/null; then
    sed -i "/^\[Default Applications\]/a $mime=$app" "$HOME/.config/mimeapps.list"
  else
    printf '\n[Default Applications]\n%s=%s\n' "$mime" "$app" >> "$HOME/.config/mimeapps.list"
  fi
}
for mime in x-scheme-handler/http x-scheme-handler/https x-scheme-handler/ftp x-scheme-handler/about x-scheme-handler/unknown text/html application/xhtml+xml; do
  set_default_mime "$mime" "firefox_firefox.desktop"
done

echo "  Шрифт JetBrainsMono Nerd Font для waybar/hyprlock поставьте вручную:"
echo "  распакуйте архивы Nerd Font в ~/.local/share/fonts/ и выполните fc-cache -f"
echo "  В Firefox включите портал-пикер: about:config -> widget.use-xdg-desktop-portal.file-picker = 1"
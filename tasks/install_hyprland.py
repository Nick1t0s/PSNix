#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from pathlib import Path

import helpers

TERMFILECHOOSER_REPO = "https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser"
FILEMANAGER_REPO = "https://github.com/boydaihungst/org.freedesktop.FileManager1.common"

PKGS = (
    "hyprland", "hypridle", "hyprlock", "hyprpaper", "waybar", "wofi", "kitty",
    "xdg-desktop-portal-gtk", "xdg-desktop-portal-hyprland",
    "brightnessctl", "playerctl", "pavucontrol", "wireplumber",
    "grim", "slurp",
)

FIREFOX_MIMES = (
    "x-scheme-handler/http", "x-scheme-handler/https", "x-scheme-handler/ftp",
    "x-scheme-handler/about", "x-scheme-handler/unknown",
    "text/html", "application/xhtml+xml",
)


def run():
    home = helpers.user_home()
    host = helpers.HOST
    configs = helpers.REPO / "configs"

    # 1. Пакеты
    helpers.apt_install(*PKGS)

    # 2. Терминальный файл-пикер: xdg-desktop-portal-termfilechooser (yazi в диалогах)
    helpers.apt_install("build-essential", "ninja-build", "meson", "libinih-dev",
                        "libsystemd-dev", "scdoc")
    tfc = home / ".local/libexec/xdg-desktop-portal-termfilechooser"
    if not tfc.exists():
        helpers.run(["git", "clone", "--depth", "1", TERMFILECHOOSER_REPO, "/tmp/tfc-build"])
        helpers.run(["meson", "setup", "build", f"--prefix={home}/.local"], cwd="/tmp/tfc-build")
        helpers.run(["ninja", "-C", "build", "install"], cwd="/tmp/tfc-build")

    # 2b. «Показать в папке» -> yazi: org.freedesktop.FileManager1.common
    helpers.apt_install("libdbus-1-dev")
    fm1 = home / ".local/libexec/file_manager_dbus"
    if not fm1.exists():
        helpers.run(["git", "clone", "--depth", "1", FILEMANAGER_REPO, "/tmp/fm1-build"])
        helpers.run(["meson", "setup", "build", f"--prefix={home}/.local"], cwd="/tmp/fm1-build")
        helpers.run(["ninja", "-C", "build", "install"], cwd="/tmp/fm1-build")
    # Ubuntu не ставит сервис-файл (нет pkg-config systemd) — создаём сами
    helpers.write_file(
        str(home / ".local/share/dbus-1/services/org.freedesktop.FileManager1.service"),
        f"[D-BUS Service]\nName=org.freedesktop.FileManager1\n"
        f"Exec={home}/.local/libexec/file_manager_dbus\n")
    # Dolphin держит имя org.freedesktop.FileManager1, пока запущен — закрываем
    helpers.run(["pkill", "dolphin"], check=False)

    # 3. Конфиги из репозитория (с бэкапом существующих)
    pairs = [
        (configs / host / "hyprland.conf", home / ".config/hypr/hyprland.conf"),
        (configs / "hypr/hypridle.conf", home / ".config/hypr/hypridle.conf"),
        (configs / "hypr/hyprlock.conf", home / ".config/hypr/hyprlock.conf"),
        (configs / "hypr/hyprpaper.conf", home / ".config/hypr/hyprpaper.conf"),
        (configs / host / "waybar/hyprland-config", home / ".config/waybar/hyprland-config"),
        (configs / "waybar/hyprland-style.css", home / ".config/waybar/hyprland-style.css"),
        (configs / "waybar/scripts/cpu-temp.sh", home / ".config/waybar/scripts/cpu-temp.sh"),
        (configs / "portals/termfilechooser/config",
         home / ".config/xdg-desktop-portal-termfilechooser/config"),
        (configs / "portals/xdg-desktop-portal/portals.conf",
         home / ".config/xdg-desktop-portal/portals.conf"),
        (configs / "portals/environment.d/portal.conf",
         home / ".config/environment.d/portal.conf"),
        (configs / "portals/filemanager1/config",
         home / ".config/org.freedesktop.FileManager1.common/config"),
    ]
    for src, dst in pairs:
        helpers.copy_config(str(src), str(dst))
    fm1_cfg = home / ".config/org.freedesktop.FileManager1.common/config"
    fm1_cfg.write_text(fm1_cfg.read_text(encoding="utf-8")
                       .replace("@PREFIX@", f"{home}/.local"), encoding="utf-8")
    helpers.chmod(str(home / ".config/waybar/scripts/cpu-temp.sh"), "755")

    # 4. Перезапуск порталов, чтобы подхватился новый файл-пикер
    helpers.user_systemctl(["restart", "xdg-desktop-portal.service"], check=False)

    # 5. Firefox — браузер по умолчанию (на Ubuntu это snap: firefox_firefox.desktop)
    for mime in FIREFOX_MIMES:
        helpers.set_default_mime(mime, "firefox_firefox.desktop")

    helpers.emit("  Шрифт JetBrainsMono Nerd Font для waybar/hyprlock поставьте вручную:")
    helpers.emit("  распакуйте архивы Nerd Font в ~/.local/share/fonts/ и выполните fc-cache -f")
    helpers.emit("  В Firefox включите портал-пикер: about:config -> "
                 "widget.use-xdg-desktop-portal.file-picker = 1")

if __name__ == "__main__":
    sys.exit(helpers.task_main("hyprland", run))

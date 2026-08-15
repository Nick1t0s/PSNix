#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers

TERMFILECHOOSER_REPO = "https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser"
FILEMANAGER_REPO = "https://github.com/boydaihungst/org.freedesktop.FileManager1.common"

WAYLAND_PKGS = (
    "hyprland", "hypridle", "hyprlock", "hyprpaper", "waybar", "wofi", "kitty",
    "xdg-desktop-portal-gtk", "xdg-desktop-portal-hyprland",
    "brightnessctl", "playerctl", "pavucontrol", "wireplumber",
    "grim", "slurp",
)


def run():
    home = helpers.user_home()

    # 1. Пакеты Wayland-стека
    helpers.emit("── Пакеты Hyprland")
    helpers.apt_install(*WAYLAND_PKGS)

    # 2. Терминальный файл-пикер: xdg-desktop-portal-termfilechooser (yazi в диалогах)
    helpers.emit("── Сборка termfilechooser")
    helpers.apt_install("build-essential", "ninja-build", "meson", "pkg-config",
                        "libinih-dev", "libsystemd-dev", "scdoc")
    tfc = home / ".local/libexec/xdg-desktop-portal-termfilechooser"
    if not tfc.exists():
        helpers.run(["git", "clone", "--depth", "1", TERMFILECHOOSER_REPO, "/tmp/tfc-build"])
        helpers.run(["meson", "setup", "build", f"--prefix={home}/.local"],
                    cwd="/tmp/tfc-build")
        helpers.run(["ninja", "-C", "build", "install"], cwd="/tmp/tfc-build")

    # 3. «Показать в папке» -> yazi: org.freedesktop.FileManager1.common
    helpers.emit("── Сборка FileManager1")
    helpers.apt_install("libdbus-1-dev")
    fm1 = home / ".local/libexec/file_manager_dbus"
    if not fm1.exists():
        helpers.run(["git", "clone", "--depth", "1", FILEMANAGER_REPO, "/tmp/fm1-build"])
        helpers.run(["meson", "setup", "build", f"--prefix={home}/.local"],
                    cwd="/tmp/fm1-build")
        helpers.run(["ninja", "-C", "build", "install"], cwd="/tmp/fm1-build")
    # Ubuntu не ставит сервис-файл (нет pkg-config systemd) — создаём сами
    helpers.write_file(
        str(home / ".local/share/dbus-1/services/org.freedesktop.FileManager1.service"),
        f"[D-BUS Service]\nName=org.freedesktop.FileManager1\n"
        f"Exec={home}/.local/libexec/file_manager_dbus\n")
    # Dolphin держит имя org.freedesktop.FileManager1, пока запущен — закрываем
    helpers.run(["pkill", "dolphin"], check=False)

    # 4. Перезапуск порталов, чтобы подхватился новый файл-пикер
    helpers.user_systemctl(["restart", "xdg-desktop-portal.service"], check=False)

    helpers.emit("")
    helpers.emit("  Шрифт JetBrainsMono Nerd Font для waybar/hyprlock поставьте вручную:")
    helpers.emit("  распакуйте архивы Nerd Font в ~/.local/share/fonts/ и выполните fc-cache -f")
    helpers.emit("  В Firefox включите портал-пикер: about:config -> "
                 "widget.use-xdg-desktop-portal.file-picker = 1")


if __name__ == "__main__":
    sys.exit(helpers.task_main("install_wayland", run))
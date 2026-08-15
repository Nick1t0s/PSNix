#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers

FIREFOX_MIMES = (
    "x-scheme-handler/http", "x-scheme-handler/https", "x-scheme-handler/ftp",
    "x-scheme-handler/about", "x-scheme-handler/unknown",
    "text/html", "application/xhtml+xml",
)

ZOOM_DESKTOP = """[Desktop Entry]
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
"""


def run():
    home = helpers.user_home()
    host = helpers.HOST
    configs = helpers.REPO / "configs"

    # 1. Конфиги Hyprland-окружения (с бэкапом существующих)
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

    # 2. Firefox — браузер по умолчанию (на Ubuntu это snap: firefox_firefox.desktop)
    for mime in FIREFOX_MIMES:
        helpers.set_default_mime(mime, "firefox_firefox.desktop")

    # 3. Zoom: user-level .desktop перекрывает системный (нативный диалог
    #    вместо портала/терминального пикера) и переживает обновления
    apps = home / ".local/share/applications"
    if not (apps / "Zoom.desktop").exists():
        helpers.write_file(str(apps / "Zoom.desktop"), ZOOM_DESKTOP)
        helpers.run(["update-desktop-database", str(apps)], check=False)


if __name__ == "__main__":
    sys.exit(helpers.task_main("copy_configs", run))
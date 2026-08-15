from pathlib import Path

from helpers import capture, emit, prompt, run as run_cmd, write_file

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


def find_zoom_deb() -> str | None:
    dirs = [capture(["xdg-user-dir", "DOWNLOAD"]),
            str(Path.home() / "Downloads"),
            str(Path.home() / "Desktop")]
    for d in dirs:
        if not d or not Path(d).is_dir():
            continue
        for pattern in ("zoom*.deb", "Zoom*.deb"):
            for p in sorted(Path(d).glob(pattern)):
                if p.is_file():
                    return str(p)
    return None


def run():
    home = Path.home()
    emit("")
    emit("  Скачайте Zoom: https://zoom.us/download?os=linux")
    emit("  Пакет zoom_amd64.deb должен попасть в папку загрузок")

    deb = None
    while True:
        prompt("Нажмите Enter, когда файл скачан")
        deb = find_zoom_deb()
        if deb:
            break
        emit("  Файл zoom*.deb не найден.")
        for d in (capture(["xdg-user-dir", "DOWNLOAD"]),
                  str(home / "Downloads"), str(home / "Desktop")):
            if d and Path(d).is_dir():
                emit(f"  Содержимое {d}:")
                for f in sorted(Path(d).iterdir()):
                    emit(f"    {f.name}")
        manual = prompt("Введите путь к файлу вручную (или пусто — продолжить поиск)")
        if manual and Path(manual).is_file():
            deb = manual
            break

    run_cmd(["apt", "install", "-y", deb], sudo=True)

    # Нативный файловый диалог вместо портала: Zoom (Qt + CEF) иначе уходит
    # в терминальный файл-пикер (yazi). User-level .desktop перекрывает системный
    # и переживает обновления Zoom.
    apps = home / ".local/share/applications"
    if not (apps / "Zoom.desktop").exists():
        write_file(str(apps / "Zoom.desktop"), ZOOM_DESKTOP)
        run_cmd(["update-desktop-database", str(apps)], check=False)
#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
import shutil
import tarfile
from pathlib import Path

from helpers import REPO, TaskError, run as run_cmd, write_file


def find_archive() -> Path | None:
    candidates = [*REPO.glob("wt_launcher_linux_*.tar.gz"),
                  *helpers.user_home().glob("Downloads/wt_launcher_linux_*.tar.gz"),
                  *Path(".").glob("wt_launcher_linux_*.tar.gz")]
    for cand in candidates:
        if cand.is_file():
            return cand
    return None


def run():
    home = helpers.user_home()
    archive = find_archive()
    if not archive:
        raise TaskError("Архив wt_launcher_linux_*.tar.gz не найден — положите его в корень репо")

    dest = home / "wta"
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True)
    with tarfile.open(archive) as tf:
        tf.extractall(dest)

    launcher_dir = dest / "WarThunder"
    launcher = launcher_dir / "launcher"
    if not launcher.is_file():
        raise TaskError(f"Бинарник launcher не найден в {launcher_dir}")

    # Ярлык в меню + иконка (из launcher.ico, 256x256 PNG кадр)
    apps = home / ".local/share/applications"
    icons = home / ".local/share/icons/hicolor/256x256/apps"
    apps.mkdir(parents=True, exist_ok=True)
    icons.mkdir(parents=True, exist_ok=True)
    if shutil.which("convert"):
        run_cmd(["convert", f"{launcher_dir}/launcher.ico[5]", str(icons / "warthunder.png")],
            check=False)
    write_file(str(apps / "warthunder.desktop"),
               f"""[Desktop Entry]
Type=Application
Name=War Thunder
Comment=Лаунчер War Thunder
Exec={launcher}
Icon=warthunder
Terminal=false
Categories=Game;
""")

if __name__ == "__main__":
    sys.exit(helpers.task_main("warthunder", run))

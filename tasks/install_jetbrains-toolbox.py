#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
import shutil
import subprocess
import tarfile
import time
from pathlib import Path

from helpers import ENV, TaskError, download, emit, get_json, prompt, run as run_cmd

API = "https://data.services.jetbrains.com/products/releases?code=TBA&latest=true&type=release"


def run():
    emit("")
    emit("  JetBrains Toolbox")
    emit("  Запустите Nekoray и подключите VPN")
    emit("  Без VPN скачивание JetBrains Toolbox может не работать")
    prompt("Нажмите Enter, когда VPN подключён")

    data = get_json(API)
    try:
        ver = data["TBA"][0]["build"]
    except (KeyError, IndexError, TypeError):
        raise TaskError("не удалось получить версию JetBrains Toolbox")

    download(f"https://download.jetbrains.com/toolbox/jetbrains-toolbox-{ver}.tar.gz",
             "/tmp/jetbrains-toolbox.tar.gz")

    dest = helpers.user_home() / ".local/share/JetBrains/Toolbox"
    dest.mkdir(parents=True, exist_ok=True)
    for old in dest.glob("jetbrains-toolbox-*"):
        shutil.rmtree(old, ignore_errors=True)
    with tarfile.open("/tmp/jetbrains-toolbox.tar.gz") as tf:
        tf.extractall(dest)

    apps = sorted(dest.glob("jetbrains-toolbox-*/bin/jetbrains-toolbox"))
    if not apps:
        raise TaskError("не найден бинарник JetBrains Toolbox")
    subprocess.Popen([str(apps[0])], stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, env=ENV)
    for _ in range(30):
        if (dest / ".appState.json").exists():
            break
        time.sleep(1)
    if not (dest / ".appState.json").exists():
        raise TaskError("JetBrains Toolbox не запустился")

if __name__ == "__main__":
    sys.exit(helpers.task_main("jetbrains-toolbox", run))

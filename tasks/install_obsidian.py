#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import TaskError, download, get_json, run as run_cmd


def run():
    ver = get_json("https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest")["tag_name"].lstrip("v")
    if not ver:
        raise TaskError("не удалось получить версию Obsidian")
    download(f"https://github.com/obsidianmd/obsidian-releases/releases/download/v{ver}/obsidian_{ver}_amd64.deb",
             "/tmp/obsidian.deb")
    run_cmd(["apt", "install", "-y", "/tmp/obsidian.deb"], sudo=True)

if __name__ == "__main__":
    sys.exit(helpers.task_main("obsidian", run))

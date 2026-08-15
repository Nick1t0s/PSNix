#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import apt_install, run as run_cmd


def run():
    apt_install("flatpak")
    run_cmd(["flatpak", "remote-add", "--if-not-exists", "flathub",
         "https://dl.flathub.org/repo/flathub.flatpakrepo"])

if __name__ == "__main__":
    sys.exit(helpers.task_main("flatpak", run))

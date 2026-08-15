#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import apt_install, run as run_cmd


def run():
    apt_install("pipx")
    run_cmd(["pipx", "ensurepath"])
    run_cmd(["pipx", "install", "konsave"])

if __name__ == "__main__":
    sys.exit(helpers.task_main("konsave", run))

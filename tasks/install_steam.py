#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import apt_install, run as run_cmd


def run():
    run_cmd(["dpkg", "--add-architecture", "i386"], sudo=True)
    run_cmd(["add-apt-repository", "-y", "multiverse"], sudo=True)
    run_cmd(["apt", "update"], sudo=True)
    apt_install("steam")

if __name__ == "__main__":
    sys.exit(helpers.task_main("steam", run))

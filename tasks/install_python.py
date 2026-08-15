#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import apt_install, run as run_cmd

VERSIONS = [f"python3.{v}" for v in ("9", "10", "11", "12", "13")]
PKGS = [p for v in VERSIONS for p in (v, f"{v}-dev", f"{v}-venv")]


def run():
    run_cmd(["add-apt-repository", "-y", "ppa:deadsnakes/ppa"], sudo=True)
    run_cmd(["apt", "update"], sudo=True)
    apt_install(*PKGS)

if __name__ == "__main__":
    sys.exit(helpers.task_main("python", run))

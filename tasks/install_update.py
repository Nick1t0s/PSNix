#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import run as run_cmd


def run():
    run_cmd(["apt", "update"], sudo=True)
    run_cmd(["apt", "upgrade", "-y"], sudo=True)
    run_cmd(["apt", "autoremove", "-y"], sudo=True)

if __name__ == "__main__":
    sys.exit(helpers.task_main("update", run))

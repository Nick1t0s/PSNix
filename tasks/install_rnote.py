#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import run as run_cmd, snap_install


def run():
    snap_install("rnote")
    run_cmd(["snap", "connect", "rnote:removable-media"], check=False)

if __name__ == "__main__":
    sys.exit(helpers.task_main("rnote", run))

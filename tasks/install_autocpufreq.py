#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import run as run_cmd, snap_install


def run():
    snap_install("auto-cpufreq")
    run_cmd(["systemctl", "enable", "--now", "snap.auto-cpufreq.service.service"], sudo=True)

if __name__ == "__main__":
    sys.exit(helpers.task_main("autocpufreq", run))

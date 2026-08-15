#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import apt_install


def run():
    apt_install("ripgrep", "fd-find", "fzf", "bat", "eza", "tree", "ncdu", "duf")

if __name__ == "__main__":
    sys.exit(helpers.task_main("cli-tools", run))

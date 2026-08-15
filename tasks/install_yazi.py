#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import apt_install, download, run as run_cmd, write_sudo

REPO_DEB = "deb [signed-by=/usr/share/keyrings/yazi-keyring.gpg] https://yazi-rs.github.io/builds/ stable main\n"


def run():
    download("https://yazi-rs.github.io/builds/yazi-keyring.gpg", "/tmp/yazi-keyring.gpg")
    run_cmd(["cp", "/tmp/yazi-keyring.gpg", "/usr/share/keyrings/yazi-keyring.gpg"], sudo=True)
    write_sudo("/etc/apt/sources.list.d/yazi.list", REPO_DEB)
    run_cmd(["apt", "update"], sudo=True)
    apt_install("yazi")

if __name__ == "__main__":
    sys.exit(helpers.task_main("yazi", run))

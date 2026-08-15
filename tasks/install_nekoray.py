#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import apt_install, download, run as run_cmd

URL = ("https://github.com/MatsuriDayo/nekoray/releases/download/"
       "3.26/nekoray-3.26-2023-12-09-debian-x64.deb")


def run():
    apt_install("libxcb-xinerama0", verify=False)
    download(URL, "/tmp/nekoray.deb")
    run_cmd(["apt", "install", "-y", "/tmp/nekoray.deb"], sudo=True)

if __name__ == "__main__":
    sys.exit(helpers.task_main("nekoray", run))

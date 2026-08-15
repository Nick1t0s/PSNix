#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from helpers import download, run as run_cmd, systemd_enable_now, write_sudo

BINARY_URL = ("https://github.com/Nortank12/deepcool-digital-linux/"
              "releases/latest/download/deepcool-digital-linux")

UDEV_RULES = 'SUBSYSTEM=="hidraw", ATTRS{idVendor}=="3633", MODE="0666"\n'

UNIT = """[Unit]
Description=DeepCool Digital

[Service]
ExecStart=/usr/sbin/deepcool-digital-linux
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
"""


def run():
    download(BINARY_URL, "/tmp/deepcool-digital-linux")
    run_cmd(["chmod", "+x", "/tmp/deepcool-digital-linux"])
    run_cmd(["cp", "/tmp/deepcool-digital-linux", "/usr/sbin/"], sudo=True)
    write_sudo("/etc/udev/rules.d/99-deepcool-digital.rules", UDEV_RULES)
    run_cmd(["udevadm", "control", "--reload-rules"], sudo=True)
    run_cmd(["udevadm", "trigger"], sudo=True)
    write_sudo("/etc/systemd/system/deepcool-digital.service", UNIT)
    run_cmd(["systemctl", "daemon-reload"], sudo=True)
    run_cmd(["systemctl", "enable", "deepcool-digital"], sudo=True)
    run_cmd(["systemctl", "start", "deepcool-digital"], sudo=True)

if __name__ == "__main__":
    sys.exit(helpers.task_main("deepcool", run))

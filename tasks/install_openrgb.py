#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from pathlib import Path

from helpers import append_line_sudo, emit, prompt, run as run_cmd, sed_replace_sudo


def run():
    emit("")
    emit("  OpenRGB")
    emit("  Скачайте с https://gitlab.com/CalcProgrammer1/OpenRGB/-/releases:")
    emit("    • openrgb_*.deb          → в ~/Downloads")
    emit("    • 60-openrgb.rules       → в ~/Downloads")
    emit("  Для Ubuntu 24.04+ берите пакет *_trixie_*.deb, для 22.04/23.x — *_bookworm_*.deb")
    emit("  Также включите в BIOS: Settings → Advanced → Mystic Light → Enabled")

    dl = helpers.user_home() / "Downloads"
    local_deb = None
    local_rules = None
    while True:
        prompt("Нажмите Enter, когда файлы скачаны")
        debs = sorted(dl.glob("openrgb*.deb"))
        rules = sorted(dl.glob("60-openrgb.rules"))
        if debs and rules:
            local_deb, local_rules = str(debs[0]), str(rules[0])
            break
        emit("  В ~/Downloads не найдены openrgb*.deb и/или 60-openrgb.rules")

    run_cmd(["apt", "install", "-y", "i2c-tools"], sudo=True)
    run_cmd(["modprobe", "i2c-dev"], sudo=True, check=False)
    run_cmd(["modprobe", "i2c-i801"], sudo=True, check=False)
    append_line_sudo("/etc/modules", "i2c-dev")
    append_line_sudo("/etc/modules", "i2c-i801")
    run_cmd(["cp", local_rules, "/usr/lib/udev/rules.d/"], sudo=True)
    run_cmd(["udevadm", "control", "--reload-rules"], sudo=True)
    run_cmd(["udevadm", "trigger"], sudo=True)
    run_cmd(["apt", "install", "-y", local_deb], sudo=True)

    if sed_replace_sudo("/etc/default/grub",
                        r'^GRUB_CMDLINE_LINUX_DEFAULT="(.*)"$',
                        r'GRUB_CMDLINE_LINUX_DEFAULT="\1 acpi_enforce_resources=lax"'):
        run_cmd(["update-grub"], sudo=True)

if __name__ == "__main__":
    sys.exit(helpers.task_main("openrgb", run))

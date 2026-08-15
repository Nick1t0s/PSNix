from helpers import run as run_cmd, snap_install


def run():
    snap_install("auto-cpufreq")
    run_cmd(["systemctl", "enable", "--now", "snap.auto-cpufreq.service.service"], sudo=True)
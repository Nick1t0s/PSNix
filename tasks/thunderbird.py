from helpers import run as run_cmd, snap_install


def run():
    snap_install("thunderbird")
    run_cmd(["snap", "connect", "thunderbird:fonts"], check=False)
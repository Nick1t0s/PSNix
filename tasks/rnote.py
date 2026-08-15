from helpers import run as run_cmd, snap_install


def run():
    snap_install("rnote")
    run_cmd(["snap", "connect", "rnote:removable-media"], check=False)
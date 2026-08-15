from helpers import run as run_cmd


def run():
    run_cmd(["apt", "update"], sudo=True)
    run_cmd(["apt", "upgrade", "-y"], sudo=True)
    run_cmd(["apt", "autoremove", "-y"], sudo=True)
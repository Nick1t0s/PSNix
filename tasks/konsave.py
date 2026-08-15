from helpers import apt_install, run as run_cmd


def run():
    apt_install("pipx")
    run_cmd(["pipx", "ensurepath"])
    run_cmd(["pipx", "install", "konsave"])
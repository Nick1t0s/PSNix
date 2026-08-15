from helpers import apt_install, run as run_cmd


def run():
    run_cmd(["dpkg", "--add-architecture", "i386"], sudo=True)
    run_cmd(["add-apt-repository", "-y", "multiverse"], sudo=True)
    run_cmd(["apt", "update"], sudo=True)
    apt_install("steam")
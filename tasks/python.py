from helpers import apt_install, run as run_cmd

VERSIONS = [f"python3.{v}" for v in ("9", "10", "11", "12", "13")]
PKGS = [p for v in VERSIONS for p in (v, f"{v}-dev", f"{v}-venv")]


def run():
    run_cmd(["add-apt-repository", "-y", "ppa:deadsnakes/ppa"], sudo=True)
    run_cmd(["apt", "update"], sudo=True)
    apt_install(*PKGS)
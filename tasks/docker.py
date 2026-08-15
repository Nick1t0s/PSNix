import os
from pathlib import Path

from helpers import apt_install, capture, download, run as run_cmd, systemd_enable_now, write_sudo

DOCKER_REPO = "https://download.docker.com/linux/ubuntu/gpg"


def run():
    run_cmd(["apt", "remove", "-y", "docker", "docker-engine", "docker.io", "containerd", "runc"],
        sudo=True, check=False)
    apt_install("ca-certificates", "curl", "gnupg")
    run_cmd(["install", "-m", "0755", "-d", "/etc/apt/keyrings"], sudo=True)

    download(DOCKER_REPO, "/tmp/docker.gpg")
    run_cmd(["gpg", "--batch", "--dearmor", "-o", "/tmp/docker.gpg.dear", "/tmp/docker.gpg"])
    run_cmd(["cp", "/tmp/docker.gpg.dear", "/etc/apt/keyrings/docker.gpg"], sudo=True)
    run_cmd(["chmod", "a+r", "/etc/apt/keyrings/docker.gpg"], sudo=True)

    codename = ""
    for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
        if line.startswith("VERSION_CODENAME="):
            codename = line.split("=", 1)[1].strip('"')
            break
    arch = capture(["dpkg", "--print-architecture"])
    write_sudo("/etc/apt/sources.list.d/docker.list",
               f"deb [arch={arch} signed-by=/etc/apt/keyrings/docker.gpg] "
               f"https://download.docker.com/linux/ubuntu {codename} stable\n")

    run_cmd(["apt", "update"], sudo=True)
    apt_install("docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin",
                "docker-compose-plugin", "docker-ce-rootless-extras", verify=False)
    systemd_enable_now("docker")
    run_cmd(["usermod", "-aG", "docker", os.environ["USER"]], sudo=True)
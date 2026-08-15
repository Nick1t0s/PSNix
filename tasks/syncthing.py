from helpers import apt_install, download, run as run_cmd, systemd_enable_now, write_sudo

REPO_DEB = ("deb [signed-by=/etc/apt/keyrings/syncthing-archive-keyring.gpg] "
            "https://apt.syncthing.net/ syncthing stable-v2\n")


def run():
    run_cmd(["mkdir", "-p", "/etc/apt/keyrings"], sudo=True)
    download("https://syncthing.net/release-key.gpg", "/tmp/syncthing-key.gpg")
    run_cmd(["cp", "/tmp/syncthing-key.gpg", "/etc/apt/keyrings/syncthing-archive-keyring.gpg"], sudo=True)
    write_sudo("/etc/apt/sources.list.d/syncthing.list", REPO_DEB)
    run_cmd(["apt-get", "update"], sudo=True)
    apt_install("syncthing")
    systemd_enable_now("syncthing", user=True)
from helpers import apt_install, systemd_enable_now


def run():
    apt_install("openssh-server")
    systemd_enable_now("ssh")
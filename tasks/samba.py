from helpers import apt_install, systemd_enable_now


def run():
    apt_install("samba", "smbclient")
    systemd_enable_now("smbd")
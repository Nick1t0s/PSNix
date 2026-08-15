from helpers import apt_install


def run():
    apt_install("imagemagick", "rsync", "sshfs", "timeshift")
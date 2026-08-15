from helpers import apt_install


def run():
    apt_install("btop", "nvtop", "iotop", "nload", "iftop", "nethogs", "powerstat")
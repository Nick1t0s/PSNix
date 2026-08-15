from helpers import apt_install


def run():
    apt_install("ripgrep", "fd-find", "fzf", "bat", "eza", "tree", "ncdu", "duf")
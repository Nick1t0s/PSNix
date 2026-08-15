from helpers import apt_install, run as run_cmd


def run():
    apt_install("flatpak")
    run_cmd(["flatpak", "remote-add", "--if-not-exists", "flathub",
         "https://dl.flathub.org/repo/flathub.flatpakrepo"])
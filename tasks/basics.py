from helpers import apt_install


def run():
    apt_install("curl", "wget", "unzip", "p7zip-full")
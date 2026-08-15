from helpers import apt_install, download, run as run_cmd

URL = ("https://github.com/MatsuriDayo/nekoray/releases/download/"
       "3.26/nekoray-3.26-2023-12-09-debian-x64.deb")


def run():
    apt_install("libxcb-xinerama0", verify=False)
    download(URL, "/tmp/nekoray.deb")
    run_cmd(["apt", "install", "-y", "/tmp/nekoray.deb"], sudo=True)
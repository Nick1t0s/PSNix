from helpers import apt_install, download, run as run_cmd, write_sudo

REPO_DEB = "deb [signed-by=/usr/share/keyrings/yazi-keyring.gpg] https://yazi-rs.github.io/builds/ stable main\n"


def run():
    download("https://yazi-rs.github.io/builds/yazi-keyring.gpg", "/tmp/yazi-keyring.gpg")
    run_cmd(["cp", "/tmp/yazi-keyring.gpg", "/usr/share/keyrings/yazi-keyring.gpg"], sudo=True)
    write_sudo("/etc/apt/sources.list.d/yazi.list", REPO_DEB)
    run_cmd(["apt", "update"], sudo=True)
    apt_install("yazi")
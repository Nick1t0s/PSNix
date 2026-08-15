from helpers import TaskError, download, get_json, run as run_cmd


def run():
    ver = get_json("https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest")["tag_name"].lstrip("v")
    if not ver:
        raise TaskError("не удалось получить версию Obsidian")
    download(f"https://github.com/obsidianmd/obsidian-releases/releases/download/v{ver}/obsidian_{ver}_amd64.deb",
             "/tmp/obsidian.deb")
    run_cmd(["apt", "install", "-y", "/tmp/obsidian.deb"], sudo=True)
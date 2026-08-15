#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
import platform

from helpers import TaskError, apt_install, download, get_json, run as run_cmd


def run():
    apt_install("jq")
    tag = get_json("https://api.github.com/repos/Adembc/lazyssh/releases/latest").get("tag_name")
    if not tag or tag == "null":
        raise TaskError("не удалось получить версию lazyssh")
    download(f"https://github.com/Adembc/lazyssh/releases/download/{tag}/"
             f"lazyssh_{platform.system()}_{platform.machine()}.tar.gz",
             "/tmp/lazyssh.tar.gz")
    run_cmd(["tar", "-xzf", "/tmp/lazyssh.tar.gz", "-C", "/tmp"])
    run_cmd(["mv", "/tmp/lazyssh", "/usr/local/bin/"], sudo=True)

if __name__ == "__main__":
    sys.exit(helpers.task_main("lazyssh", run))

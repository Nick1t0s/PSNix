#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
import time

from helpers import TaskError, emit, run_silent


def run():
    emit("  Тихая установка, может занять несколько минут...")
    for _ in range(3):
        if run_silent("curl -fsSL https://ollama.com/install.sh | sh", shell=True) == 0:
            return
        time.sleep(3)
    raise TaskError("не удалось установить Ollama")

if __name__ == "__main__":
    sys.exit(helpers.task_main("ollama", run))

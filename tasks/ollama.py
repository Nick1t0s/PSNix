import time

from helpers import TaskError, emit, run_silent


def run():
    emit("  Тихая установка, может занять несколько минут...")
    for _ in range(3):
        if run_silent("curl -fsSL https://ollama.com/install.sh | sh", shell=True) == 0:
            return
        time.sleep(3)
    raise TaskError("не удалось установить Ollama")
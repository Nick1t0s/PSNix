#!/usr/bin/env python3
# Установщик программ PSNix — движок.
#
# Запускает задачи (модули tasks/<name>.py с функцией run()) в порядке
# из query.json для хоста pc|laptop. Вывод каждой задачи идёт в терминал
# в реальном времени и дублируется в logs/<host>/<name>.txt.
#
# Использование:  python3 install.py --host pc|laptop [--dry-run] [--only a,b]

import argparse
import importlib
import json
import subprocess
import sys
import threading
from pathlib import Path

import helpers

REPO = Path(__file__).resolve().parent
LOGS_DIR = REPO / "logs"
QUERY_FILE = REPO / "query.json"

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> int:
    ap = argparse.ArgumentParser(description="Установщик программ PSNix")
    ap.add_argument("--host", required=True, choices=["pc", "laptop"])
    ap.add_argument("--dry-run", action="store_true",
                    help="только показать список задач без запуска")
    ap.add_argument("--only", metavar="TASK1,TASK2",
                    help="запустить только эти задачи (из списка хоста)")
    args = ap.parse_args()

    query = json.loads(QUERY_FILE.read_text(encoding="utf-8"))
    tasks = query.get(args.host)
    if not tasks:
        print(f"{RED}Хост '{args.host}' отсутствует в {QUERY_FILE.name}{RESET}", file=sys.stderr)
        return 1

    if args.only:
        requested = [t.strip() for t in args.only.split(",") if t.strip()]
        missing = [t for t in requested if t not in tasks]
        if missing:
            print(f"{RED}Неизвестные задачи для '{args.host}': {', '.join(missing)}{RESET}",
                  file=sys.stderr)
            return 1
        tasks = requested

    print(f"\n{BOLD}Установщик программ — {args.host.upper()}{RESET}")
    if args.dry_run:
        print("Задачи (dry-run):")
        for i, name in enumerate(tasks, 1):
            print(f"  {i:2d}. {name}")
        return 0

    # sudo: спросить пароль один раз и держать кэш живым
    print(f"\n{BOLD}Проверка sudo...{RESET}")
    if subprocess.run(["sudo", "-v"]).returncode != 0:
        print(f"{RED}Нет прав sudo — выход.{RESET}")
        return 1
    keeper_stop = threading.Event()

    def sudo_keeper():
        while not keeper_stop.is_set():
            subprocess.run(["sudo", "-n", "true"])
            keeper_stop.wait(60)

    threading.Thread(target=sudo_keeper, daemon=True).start()

    success, failed = [], []
    interrupted = False
    try:
        for name in tasks:
            ok = run_task(args.host, name)
            (success if ok else failed).append(name)
    except KeyboardInterrupt:
        interrupted = True
        print(f"\n{YELLOW}Прервано пользователем.{RESET}")
    finally:
        keeper_stop.set()

    print(f"\n{BOLD}════════════════ ИТОГ ════════════════{RESET}")
    print(f"  Успешно: {GREEN}{len(success)}{RESET}   Провал: {RED}{len(failed)}{RESET}")
    if success:
        print(f"\n{GREEN}Установлено:{RESET}")
        for name in success:
            print(f"    ✔ {name}")
    if failed:
        print(f"\n{RED}Не удалось поставить:{RESET}")
        for name in failed:
            print(f"    ✘ {name}")
        for name in failed:
            logfile = LOGS_DIR / args.host / f"{name}.txt"
            if logfile.exists():
                print(f"\n{BOLD}──── Полный вывод: {name} ────{RESET}")
                print(logfile.read_text(encoding="utf-8", errors="replace"))
    if interrupted:
        print(f"\n{YELLOW}Запуск прерван Ctrl+C — незавершённые задачи засчитаны как проваленные.{RESET}")
    print()

    return 1 if (failed or interrupted) else 0


def run_task(host: str, name: str) -> bool:
    print(f"\n  {CYAN}▶{RESET} {BOLD}{name}{RESET}")
    helpers.HOST = host
    helpers.begin_task(LOGS_DIR / host / f"{name}.txt")
    try:
        module = importlib.import_module(f"tasks.{name}")
        module.run()
    except helpers.TaskError as e:
        print(f"  {RED}✘{RESET} {BOLD}{name}{RESET}: {e}")
        return False
    except ImportError:
        print(f"  {RED}✘{RESET} {BOLD}{name}{RESET}: модуль tasks/{name}.py не найден")
        return False
    except KeyboardInterrupt:
        print(f"  {RED}✘{RESET} {BOLD}{name}{RESET} {YELLOW}(прервано Ctrl+C){RESET}")
        raise
    else:
        print(f"  {GREEN}✔{RESET} {BOLD}{name}{RESET}")
        return True
    finally:
        helpers.end_task()


if __name__ == "__main__":
    sys.exit(main())
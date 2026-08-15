#!/usr/bin/env python3
# Установщик программ PSNix — движок.
#
# Запускается с sudo (sudo -E python3 install.py --host pc|laptop).
# Каждая задача запускается в отдельном терминале: sudo python3 tasks/install_<name>.py.
# Терминал закрывается по окончании задачи; вывод дублируется в logs/<host>/<name>.txt.
#
# Использование:  sudo -E python3 install.py --host pc|laptop [--dry-run] [--only a,b]

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
LOGS_DIR = REPO / "logs"
QUERY_FILE = REPO / "query.json"
TASKS_DIR = REPO / "tasks"

# имя терминала -> флаги перед командой
TERMINALS = [
    ("kitty", ["-e"]),
    ("alacritty", ["-e"]),
    ("foot", ["-e"]),
    ("konsole", ["-e"]),
    ("gnome-terminal", ["--"]),
    ("xterm", ["-e"]),
]

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"


def resolve_terminal() -> tuple[str, list[str]] | None:
    override = os.environ.get("PSNIX_TERMINAL")
    if override:
        for name, flags in TERMINALS:
            if name == override:
                return name, flags
        print(f"{RED}PSNIX_TERMINAL='{override}' не в списке "
              f"({', '.join(n for n, _ in TERMINALS)}){RESET}", file=sys.stderr)
        return None
    for name, flags in TERMINALS:
        if shutil.which(name):
            return name, flags
    return None


def check_root_and_env() -> bool:
    """Требуем root (sudo) и наличие графической сессии для новых терминалов."""
    if os.geteuid() != 0:
        print(f"{RED}Запустите через sudo:{RESET} sudo -E python3 install.py --host pc|laptop",
              file=sys.stderr)
        return False
    if not os.environ.get("WAYLAND_DISPLAY") and not os.environ.get("DISPLAY"):
        print(f"{RED}Не видно графической сессии (WAYLAND_DISPLAY/DISPLAY).{RESET}\n"
              f"  Запустите с сохранением окружения: {BOLD}sudo -E python3 install.py --host pc{RESET}",
              file=sys.stderr)
        return False
    os.environ.setdefault("XDG_RUNTIME_DIR", "/run/user/0")
    runtime = Path(os.environ["XDG_RUNTIME_DIR"])
    if not runtime.exists():
        runtime.mkdir(mode=0o700)
    return True


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

    terminal = resolve_terminal()
    print(f"\n{BOLD}Установщик программ — {args.host.upper()}{RESET}")
    print(f"  Терминал: {terminal[0] if terminal else RED + 'не найден' + RESET}")
    if args.dry_run:
        print("Задачи (dry-run):")
        for i, name in enumerate(tasks, 1):
            print(f"  {i:2d}. {name}")
        return 0

    if terminal is None:
        print(f"{RED}Не найден терминал — установите kitty или xterm{RESET}", file=sys.stderr)
        return 1
    if not check_root_and_env():
        return 1

    success, failed = [], []
    interrupted = False
    for name in tasks:
        try:
            ok = launch_task(args.host, name, terminal)
        except KeyboardInterrupt:
            interrupted = True
            print(f"\n{YELLOW}Прервано пользователем.{RESET}")
            break
        (success if ok else failed).append(name)

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


def launch_task(host: str, name: str, terminal: tuple[str, list[str]]) -> bool:
    """Запуск задачи в отдельном терминале; ждём, пока терминал закроется."""
    task_file = TASKS_DIR / f"install_{name}.py"
    if not task_file.exists():
        print(f"  {RED}✘{RESET} {BOLD}{name}{RESET}: не найден {TASKS_DIR.name}/install_{name}.py")
        return False

    print(f"\n  {CYAN}▶{RESET} {BOLD}{name}{RESET}  (терминал {terminal[0]})")
    cmd = [terminal[0], *terminal[1],
           *([] if os.geteuid() == 0 else ["sudo"]),
           sys.executable, str(task_file)]
    env = os.environ.copy()
    env["PSNIX_HOST"] = host
    try:
        rc = subprocess.run(cmd, env=env).returncode
    except KeyboardInterrupt:
        raise
    if rc == 0:
        print(f"  {GREEN}✔{RESET} {BOLD}{name}{RESET}")
        return True
    print(f"  {RED}✘{RESET} {BOLD}{name}{RESET}  (код {rc}, лог: {LOGS_DIR.name}/{host}/{name}.txt)")
    return False


if __name__ == "__main__":
    sys.exit(main())
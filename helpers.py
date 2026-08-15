#!/usr/bin/env python3
# Общие помощники для задач: запуск команд с выводом в терминал и лог,
# установка пакетов с проверкой (dpkg/snap), работа с файлами.
#
# Задача — это модуль tasks/<name>.py с функцией run(). Команды запускаются
# через helpers.run(): stdout+stderr идут в реальном времени в терминал
# и в лог текущей задачи (logs/<host>/<name>.txt). Ненулевой exit code
# или провал проверки бросает TaskError — задача считается проваленной.

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent
HOST = os.environ.get("PSNIX_HOST", "laptop")

ENV = os.environ.copy()
ENV["DEBIAN_FRONTEND"] = "noninteractive"
ENV["NEEDRESTART_MODE"] = "a"

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"


class TaskError(Exception):
    """Установка не удалась (команда упала или проверка не прошла)."""


# ---- реальный пользователь (задачи работают под sudo/root) ----

def is_root() -> bool:
    return os.geteuid() == 0


def sudo_user() -> str | None:
    """Имя реального пользователя (SUDO_USER), если запущены через sudo."""
    return os.environ.get("SUDO_USER")


def user_home() -> Path:
    """Домашняя директория реального пользователя (не root)."""
    user = sudo_user()
    if user and user != "root":
        return Path(f"/home/{user}")
    return Path.home()


def user_uid_gid() -> tuple[int, int]:
    if is_root():
        uid = int(os.environ.get("SUDO_UID") or 0)
        gid = int(os.environ.get("SUDO_GID") or 0)
    else:
        uid, gid = os.getuid(), os.getgid()
    return uid, gid


def chown_to_user(path: str | Path) -> None:
    """Файлы в домашней папке пользователя не должны принадлежать root."""
    p = Path(path)
    if not is_root():
        return
    try:
        if p.resolve().is_relative_to(user_home().resolve()):
            uid, gid = user_uid_gid()
            if uid:
                os.chown(p, uid, gid)
    except OSError:
        pass


def user_systemctl(args, *, check=True) -> int:
    """systemctl --user от имени реального пользователя (мы под root)."""
    user = sudo_user()
    uid = int(os.environ.get("SUDO_UID") or 0)
    if is_root() and user and uid:
        prefix = ["sudo", "-u", user, "env", f"XDG_RUNTIME_DIR=/run/user/{uid}",
                  "systemctl", "--user"]
    else:
        prefix = ["systemctl", "--user"]
    return run([*prefix, *args], check=check)


def xdg_user_dir(name: str) -> str:
    """xdg-user-dir для реального пользователя (под root отвечает неверно)."""
    user = sudo_user()
    if is_root() and user:
        out = capture(["sudo", "-u", user, "env", "HOME=" + str(user_home()),
                       "xdg-user-dir", name])
        return out or str(user_home())
    return capture(["xdg-user-dir", name])


def task_main(name: str, run_func) -> int:
    """Точка входа standalone-задачи (запускается с sudo, host — из env PSNIX_HOST).

    Логирует в logs/<host>/<name>.txt, возвращает код возврата:
    0 — успех, 1 — TaskError/ошибка, 130 — Ctrl+C.
    """
    host = os.environ.get("PSNIX_HOST") or "default"
    begin_task(REPO / "logs" / host / f"{name}.txt")
    try:
        run_func()
        emit(f"\n{GREEN}✔{RESET} {BOLD}{name}{RESET}: готово")
        return 0
    except TaskError as e:
        emit(f"\n{RED}✘{RESET} {BOLD}{name}{RESET}: {e}")
        return 1
    except KeyboardInterrupt:
        emit(f"\n{YELLOW}✘{RESET} {BOLD}{name}{RESET}: прервано Ctrl+C")
        return 130
    except Exception as e:
        import traceback
        emit(f"\n{RED}✘{RESET} {BOLD}{name}{RESET}: непредвиденная ошибка: {e!r}")
        emit(traceback.format_exc())
        return 1
    finally:
        end_task()


_log = None


def begin_task(logfile: Path) -> None:
    global _log
    logfile.parent.mkdir(parents=True, exist_ok=True)
    _log = logfile.open("w", encoding="utf-8")


def end_task() -> None:
    global _log
    if _log:
        _log.close()
        _log = None


def emit(line: str = "") -> None:
    """Вывод в терминал и в лог текущей задачи."""
    print(line, flush=True)
    if _log:
        _log.write(line + "\n")
        _log.flush()


def run(cmd, *, sudo=False, check=True, cwd=None, shell=False):
    """Запуск команды с выводом в реальном времени (терминал + лог).

    Возвращает код возврата; при check=True и ненулевом коде бросает TaskError.
    Ctrl+C убивает весь process group команды.
    """
    argv = (["sudo"] + list(cmd)) if (sudo and not shell and not is_root()) else cmd
    proc = subprocess.Popen(
        argv,
        shell=shell,
        cwd=cwd,
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        start_new_session=True,
        env=ENV,
    )
    try:
        for line in proc.stdout:
            emit("  " + line.rstrip())
        rc = proc.wait()
    except KeyboardInterrupt:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            proc.wait(timeout=3)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        proc.wait()
        raise TaskError("прервано Ctrl+C")
    if check and rc != 0:
        raise TaskError(f"команда завершилась с кодом {rc}: {argv!r}")
    return rc


def shell(cmd: str, *, check=True) -> int:
    """Запуск строки через sh (конвейеры и т.п.) с выводом в терминал и лог."""
    return run(cmd, shell=True, check=check)


def run_silent(cmd, *, shell=False, sudo=False) -> int:
    """Тихий запуск без вывода (прогресс-бары и т.п.). Возвращает код."""
    argv = (["sudo"] + list(cmd)) if (sudo and not shell and not is_root()) else cmd
    return subprocess.run(argv, shell=shell, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL, env=ENV).returncode


def capture(cmd, *, sudo=False, shell=False) -> str:
    """Тихий запуск: возвращает stdout (без вывода в терминал и лог)."""
    argv = (["sudo"] + list(cmd)) if (sudo and not shell and not is_root()) else cmd
    result = subprocess.run(argv, shell=shell, capture_output=True, text=True, env=ENV)
    return result.stdout.strip()


def prompt(message: str) -> str:
    """Интерактивный промпт с вводом с терминала (аналог read -rp)."""
    line = "  " + message + " "
    sys.stdout.write(line)
    sys.stdout.flush()
    if _log:
        _log.write(line + "\n")
        _log.flush()
    return sys.stdin.readline().strip()


# ---- пакеты -----------------------------------------------------------

def apt_install(*packages, verify=True):
    run(["apt", "install", "-y", *packages], sudo=True)
    if verify:
        missing = [p for p in packages if not dpkg_installed(p)]
        if missing:
            raise TaskError(f"не установлены (dpkg): {', '.join(missing)}")


def dpkg_installed(package: str) -> bool:
    return subprocess.run(["dpkg", "-s", package],
                          capture_output=True).returncode == 0


def snap_install(name: str, *, classic=False):
    cmd = ["snap", "install", name] + (["--classic"] if classic else [])
    run(cmd, sudo=True)
    if not snap_installed(name):
        raise TaskError(f"не установлен snap: {name}")


def snap_installed(name: str) -> bool:
    return subprocess.run(["snap", "list", name],
                          capture_output=True).returncode == 0


def systemd_enable_now(unit: str, *, user=False):
    if user:
        user_systemctl(["enable", unit])
        user_systemctl(["start", unit])
    else:
        run(["systemctl", "enable", "--now", unit], sudo=True)


# ---- сеть -------------------------------------------------------------

def download(url: str, dest: str):
    run(["curl", "-fsSL", "--retry", "5", "--retry-all-errors", "-o", dest, url])


def get_json(url: str):
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


# ---- файлы ------------------------------------------------------------

def write_file(path: str, content: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    chown_to_user(p)


def write_sudo(path: str, content: str):
    with tempfile.NamedTemporaryFile("w", suffix=".tmp", delete=False) as f:
        f.write(content)
        tmp = f.name
    run(["cp", tmp, path], sudo=True)
    os.unlink(tmp)


def append_line_sudo(path: str, line: str):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        text = ""
    if text and not text.endswith("\n"):
        text += "\n"
    write_sudo(path, text + line + "\n")


def copy_config(src: str, dst: str):
    """Копирование конфига из репозитория с бэкапом существующего в *.bak."""
    dst_p = Path(dst)
    dst_p.parent.mkdir(parents=True, exist_ok=True)
    if dst_p.exists() and not Path(f"{dst_p}.bak").exists():
        shutil.copy2(dst_p, f"{dst_p}.bak")
        chown_to_user(f"{dst_p}.bak")
    shutil.copy2(src, dst_p)
    chown_to_user(dst_p)


def sed_replace_sudo(path: str, pattern: str, repl: str) -> bool:
    """Замена одного вхождения regex в корневом файле (через sudo)."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    new_text, n = re.subn(pattern, repl, text, count=1)
    if n:
        write_sudo(path, new_text)
    return bool(n)


def chmod(path: str, mode: str, *, sudo=False):
    run(["chmod", mode, path], sudo=sudo)


def extract_tar(path: str, dest: str):
    with tarfile.open(path) as tf:
        tf.extractall(dest)


def set_default_mime(mime: str, app: str, path: str | None = None):
    """Дописывает/обновляет mime=app в секции [Default Applications]."""
    p = Path(path) if path else user_home() / ".config/mimeapps.list"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("", encoding="utf-8")
    lines = p.read_text(encoding="utf-8").splitlines()
    header_idx = None
    replaced = False
    out = []
    for line in lines:
        if line.startswith("[Default Applications]"):
            header_idx = len(out)
        if line.startswith(f"{mime}="):
            out.append(f"{mime}={app}")
            replaced = True
        else:
            out.append(line)
    if not replaced:
        if header_idx is not None:
            out.insert(header_idx + 1, f"{mime}={app}")
        else:
            if out and out[-1] != "":
                out.append("")
            out.append("[Default Applications]")
            out.append(f"{mime}={app}")
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    chown_to_user(p)
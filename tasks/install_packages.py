#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers

NEKORAY_URL = ("https://github.com/MatsuriDayo/nekoray/releases/download/"
               "3.26/nekoray-3.26-2023-12-09-debian-x64.deb")
JETBRAINS_API = ("https://data.services.jetbrains.com/products/releases?"
                 "code=TBA&latest=true&type=release")
DOCKER_REPO = "https://download.docker.com/linux/ubuntu/gpg"

ZOOM_DESKTOP = """[Desktop Entry]
Name=Zoom Workplace
Comment=Zoom Video Conference
Exec=env QT_QPA_PLATFORMTHEME=gtk3 GTK_USE_PORTAL=0 /usr/bin/zoom %U
Icon=Zoom
Terminal=false
Type=Application
Encoding=UTF-8
Categories=Network;Application;
StartupWMClass=zoom
MimeType=x-scheme-handler/zoommtg;x-scheme-handler/zoomus;x-scheme-handler/tel;x-scheme-handler/callto;x-scheme-handler/zoomphonecall;x-scheme-handler/zoomphonesms;x-scheme-handler/zoomcontactcentercall;application/x-zoom
X-KDE-Protocols=zoommtg;zoomus;tel;callto;zoomphonecall;zoomphonesms;zoomcontactcentercall;
Name[en_US]=Zoom Workplace
"""

FIX_DOCKER_VPN_SCRIPT = """#!/bin/bash
PHYS=enp4s0; TABLE=200; MARK=0x1; TUN=neko-tun

cleanup() {
  ip rule del pref 100 2>/dev/null
  ip route flush table $TABLE 2>/dev/null
  iptables -t mangle -D PREROUTING -i "$PHYS"  -j MARK --set-mark $MARK 2>/dev/null
  iptables -t mangle -D PREROUTING -i br+     -m conntrack --ctstate ESTABLISHED,RELATED -j MARK --set-mark $MARK 2>/dev/null
  iptables -t mangle -D PREROUTING -i docker0 -m conntrack --ctstate ESTABLISHED,RELATED -j MARK --set-mark $MARK 2>/dev/null
}

apply() {
  if ! ip link show "$TUN" >/dev/null 2>&1; then cleanup; return 0; fi
  GW=$(ip -4 route show default | awk '/default/{print $3; exit}')
  HOSTIP=$(ip -4 -o addr show "$PHYS" | awk '{print $4}' | cut -d/ -f1 | head -1)
  [ -z "$GW" ] || [ -z "$HOSTIP" ] && return 0
  cleanup
  ip -4 -o route show | awk '/dev (docker0|br-)/{print $1, $3}' | \\
    while read net dev; do ip route add "$net" dev "$dev" table $TABLE 2>/dev/null; done
  ip route add default via "$GW" dev "$PHYS" table $TABLE 2>/dev/null
  ip route add local "$HOSTIP"/32 dev lo table $TABLE 2>/dev/null
  iptables -t mangle -I PREROUTING -i "$PHYS"  -j MARK --set-mark $MARK
  iptables -t mangle -I PREROUTING -i br+     -m conntrack --ctstate ESTABLISHED,RELATED -j MARK --set-mark $MARK
  iptables -t mangle -I PREROUTING -i docker0 -m conntrack --ctstate ESTABLISHED,RELATED -j MARK --set-mark $MARK
  ip rule add fwmark $MARK/0xffffffff lookup $TABLE pref 100
  logger -t fix-docker-vpn "applied (tun up)"
}

apply
ip monitor link | while read -r _; do
  sleep 0.3; apply
done
"""

FIX_DOCKER_VPN_UNIT = """[Unit]
Description=Keep Docker reachable while nekoray TUN is up
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/sbin/fix-docker-vpn.sh
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
"""

DEEPCOOL_UDEV = 'SUBSYSTEM=="hidraw", ATTRS{idVendor}=="3633", MODE="0666"\n'
DEEPCOOL_URL = ("https://github.com/Nortank12/deepcool-digital-linux/"
                "releases/latest/download/deepcool-digital-linux")
DEEPCOOL_UNIT = """[Unit]
Description=DeepCool Digital

[Service]
ExecStart=/usr/sbin/deepcool-digital-linux
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
"""

SYNCTHING_REPO = ("deb [signed-by=/etc/apt/keyrings/syncthing-archive-keyring.gpg] "
                  "https://apt.syncthing.net/ syncthing stable-v2\n")
YAZI_REPO = "deb [signed-by=/usr/share/keyrings/yazi-keyring.gpg] https://yazi-rs.github.io/builds/ stable main\n"


def find_zoom_deb() -> str | None:
    dirs = [helpers.xdg_user_dir("DOWNLOAD"),
            str(helpers.user_home() / "Downloads"),
            str(helpers.user_home() / "Desktop")]
    for d in dirs:
        if not d or not Path(d).is_dir():
            continue
        for pattern in ("zoom*.deb", "Zoom*.deb"):
            for p in sorted(Path(d).glob(pattern)):
                if p.is_file():
                    return str(p)
    return None


def run():
    host = helpers.HOST
    home = helpers.user_home()
    real_user = helpers.sudo_user() or os.environ.get("USER")

    # 1. База: обновление системы
    helpers.emit("── Обновление системы")
    helpers.run(["apt", "update"], sudo=True)
    helpers.run(["apt", "upgrade", "-y"], sudo=True)
    helpers.run(["apt", "autoremove", "-y"], sudo=True)

    # 2. Apt-пакеты
    helpers.emit("── Apt-пакеты")
    helpers.apt_install("git", "git-lfs")
    helpers.apt_install("build-essential", "cmake")
    helpers.apt_install("curl", "wget", "unzip")
    if not helpers.dpkg_installed("p7zip-full"):
        # Ubuntu 26.04: p7zip-full убран из репозитория, заменён на 7zip
        helpers.apt_install("7zip", verify=False)
        if not helpers.dpkg_installed("7zip"):
            helpers.apt_install("p7zip-full", verify=False)  # 22.04/24.04
            if not helpers.dpkg_installed("p7zip-full"):
                raise helpers.TaskError("архиватор 7-Zip не установлен (7zip/p7zip-full)")
    helpers.apt_install("ripgrep", "fd-find", "fzf", "bat", "eza", "tree", "ncdu", "duf")
    helpers.apt_install("tmux")
    helpers.apt_install("btop", "nvtop", "iotop", "nload", "iftop", "nethogs", "powerstat")
    helpers.apt_install("imagemagick", "rsync", "sshfs", "timeshift")
    helpers.apt_install("nodejs", "npm")
    helpers.apt_install("ffmpeg")
    helpers.apt_install("ghostscript")
    helpers.apt_install("htop")
    helpers.apt_install("jq")
    helpers.apt_install("vim")
    helpers.apt_install("yt-dlp")
    helpers.apt_install("rust-coreutils")
    helpers.apt_install("okular", "okular-extra-backends")
    helpers.apt_install("pdfarranger")
    helpers.apt_install("firefox")
    helpers.apt_install("vlc")
    helpers.apt_install("qbittorrent")
    helpers.apt_install("gh")
    helpers.apt_install("openssh-server")
    helpers.apt_install("samba", "smbclient")

    # 3. Python-версии (deadsnakes)
    helpers.emit("── Python (deadsnakes)")
    helpers.run(["add-apt-repository", "-y", "ppa:deadsnakes/ppa"], sudo=True)
    helpers.run(["apt", "update"], sudo=True)
    py_pkgs = []
    for v in ("9", "10", "11", "12", "13"):
        py_pkgs += [f"python3.{v}", f"python3.{v}-dev", f"python3.{v}-venv"]
    helpers.apt_install(*py_pkgs)

    # 4. Steam (i386 + multiverse)
    helpers.emit("── Steam")
    helpers.run(["dpkg", "--add-architecture", "i386"], sudo=True)
    helpers.run(["add-apt-repository", "-y", "multiverse"], sudo=True)
    helpers.run(["apt", "update"], sudo=True)
    helpers.apt_install("steam")

    # 5. Flatpak + Flathub
    helpers.emit("── Flatpak")
    helpers.apt_install("flatpak")
    helpers.run(["flatpak", "remote-add", "--if-not-exists", "flathub",
                 "https://dl.flathub.org/repo/flathub.flatpakrepo"])

    # 6. Docker (официальный репозиторий)
    helpers.emit("── Docker")
    helpers.run(["apt", "remove", "-y", "docker", "docker-engine", "docker.io",
                 "containerd", "runc"], sudo=True, check=False)
    helpers.apt_install("ca-certificates", "curl", "gnupg")
    helpers.run(["install", "-m", "0755", "-d", "/etc/apt/keyrings"], sudo=True)
    helpers.download(DOCKER_REPO, "/tmp/docker.gpg")
    helpers.run(["gpg", "--batch", "--dearmor", "-o", "/tmp/docker.gpg.dear", "/tmp/docker.gpg"])
    helpers.run(["cp", "/tmp/docker.gpg.dear", "/etc/apt/keyrings/docker.gpg"], sudo=True)
    helpers.run(["chmod", "a+r", "/etc/apt/keyrings/docker.gpg"], sudo=True)
    codename = ""
    for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
        if line.startswith("VERSION_CODENAME="):
            codename = line.split("=", 1)[1].strip('"')
            break
    arch = helpers.capture(["dpkg", "--print-architecture"])
    helpers.write_sudo("/etc/apt/sources.list.d/docker.list",
                       f"deb [arch={arch} signed-by=/etc/apt/keyrings/docker.gpg] "
                       f"https://download.docker.com/linux/ubuntu {codename} stable\n")
    helpers.run(["apt", "update"], sudo=True)
    helpers.apt_install("docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin",
                        "docker-compose-plugin", "docker-ce-rootless-extras", verify=False)
    helpers.systemd_enable_now("docker")
    if real_user:
        helpers.run(["usermod", "-aG", "docker", real_user], sudo=True)

    # 7. Syncthing (репозиторий + user-сервис)
    helpers.emit("── Syncthing")
    helpers.run(["mkdir", "-p", "/etc/apt/keyrings"], sudo=True)
    helpers.download("https://syncthing.net/release-key.gpg", "/tmp/syncthing-key.gpg")
    helpers.run(["cp", "/tmp/syncthing-key.gpg",
                 "/etc/apt/keyrings/syncthing-archive-keyring.gpg"], sudo=True)
    helpers.write_sudo("/etc/apt/sources.list.d/syncthing.list", SYNCTHING_REPO)
    helpers.run(["apt-get", "update"], sudo=True)
    helpers.apt_install("syncthing")
    helpers.systemd_enable_now("syncthing", user=True)

    # 8. Yazi (репозиторий)
    helpers.emit("── Yazi")
    helpers.download("https://yazi-rs.github.io/builds/yazi-keyring.gpg", "/tmp/yazi-keyring.gpg")
    helpers.run(["cp", "/tmp/yazi-keyring.gpg", "/usr/share/keyrings/yazi-keyring.gpg"], sudo=True)
    helpers.write_sudo("/etc/apt/sources.list.d/yazi.list", YAZI_REPO)
    helpers.run(["apt", "update"], sudo=True)
    helpers.apt_install("yazi")

    # 9. Snap-пакеты
    helpers.emit("── Snap-пакеты")
    helpers.snap_install("telegram-desktop")
    helpers.snap_install("obs-studio")
    helpers.snap_install("rnote")
    helpers.run(["snap", "connect", "rnote:removable-media"], check=False)
    helpers.snap_install("thunderbird")
    helpers.run(["snap", "connect", "thunderbird:fonts"], check=False)
    helpers.snap_install("opencode", classic=True)
    if host == "laptop":
        helpers.snap_install("auto-cpufreq")
        helpers.run(["systemctl", "enable", "--now",
                     "snap.auto-cpufreq.service.service"], sudo=True)

    # 10. Скриптовые установки: lazydocker, lazyssh, konsave, ollama
    helpers.emit("── lazydocker")
    helpers.shell("curl -fsSL https://raw.githubusercontent.com/jesseduffield/"
                  "lazydocker/master/scripts/install_update_linux.sh | bash")
    helpers.emit("── lazyssh")
    tag = helpers.get_json(
        "https://api.github.com/repos/Adembc/lazyssh/releases/latest").get("tag_name")
    if not tag or tag == "null":
        raise helpers.TaskError("не удалось получить версию lazyssh")
    helpers.download(f"https://github.com/Adembc/lazyssh/releases/download/{tag}/"
                     f"lazyssh_{platform.system()}_{platform.machine()}.tar.gz",
                     "/tmp/lazyssh.tar.gz")
    helpers.run(["tar", "-xzf", "/tmp/lazyssh.tar.gz", "-C", "/tmp"])
    helpers.run(["mv", "/tmp/lazyssh", "/usr/local/bin/"], sudo=True)
    helpers.emit("── konsave (pipx)")
    helpers.apt_install("pipx")
    helpers.run(["pipx", "ensurepath"])
    helpers.run(["pipx", "install", "konsave"])
    helpers.emit("── Ollama")
    helpers.emit("  Тихая установка, может занять несколько минут...")
    for _ in range(3):
        if helpers.run_silent("curl -fsSL https://ollama.com/install.sh | sh",
                              shell=True) == 0:
            break
        time.sleep(3)
    else:
        raise helpers.TaskError("не удалось установить Ollama")

    # 11. Deb-пакеты: nekoray, obsidian, zoom
    helpers.emit("── Nekoray")
    helpers.apt_install("libxcb-xinerama0", verify=False)
    helpers.download(NEKORAY_URL, "/tmp/nekoray.deb")
    helpers.apt_install_deb("/tmp/nekoray.deb")
    helpers.emit("── Obsidian")
    ver = helpers.get_json("https://api.github.com/repos/obsidianmd/"
                           "obsidian-releases/releases/latest")["tag_name"].lstrip("v")
    if not ver:
        raise helpers.TaskError("не удалось получить версию Obsidian")
    helpers.download(f"https://github.com/obsidianmd/obsidian-releases/releases/download/"
                     f"v{ver}/obsidian_{ver}_amd64.deb", "/tmp/obsidian.deb")
    helpers.apt_install_deb("/tmp/obsidian.deb")

    helpers.emit("── Zoom")
    helpers.emit("  Скачайте Zoom: https://zoom.us/download?os=linux")
    helpers.emit("  Пакет zoom_amd64.deb должен попасть в папку загрузок")
    deb = None
    while True:
        helpers.prompt("Нажмите Enter, когда файл скачан")
        deb = find_zoom_deb()
        if deb:
            break
        helpers.emit("  Файл zoom*.deb не найден.")
        for d in (helpers.xdg_user_dir("DOWNLOAD"),
                  str(home / "Downloads"), str(home / "Desktop")):
            if d and Path(d).is_dir():
                helpers.emit(f"  Содержимое {d}:")
                for f in sorted(Path(d).iterdir()):
                    helpers.emit(f"    {f.name}")
        manual = helpers.prompt("Введите путь к файлу вручную (или пусто — продолжить поиск)")
        if manual and Path(manual).is_file():
            deb = manual
            break
    helpers.apt_install_deb(deb)

    # 12. JetBrains Toolbox
    helpers.emit("── JetBrains Toolbox")
    helpers.emit("  Запустите Nekoray и подключите VPN")
    helpers.emit("  Без VPN скачивание JetBrains Toolbox может не работать")
    helpers.prompt("Нажмите Enter, когда VPN подключён")
    data = helpers.get_json(JETBRAINS_API)
    try:
        jb_ver = data["TBA"][0]["build"]
    except (KeyError, IndexError, TypeError):
        raise helpers.TaskError("не удалось получить версию JetBrains Toolbox")
    helpers.download(f"https://download.jetbrains.com/toolbox/jetbrains-toolbox-{jb_ver}.tar.gz",
                     "/tmp/jetbrains-toolbox.tar.gz")
    dest = home / ".local/share/JetBrains/Toolbox"
    dest.mkdir(parents=True, exist_ok=True)
    for old in dest.glob("jetbrains-toolbox-*"):
        shutil.rmtree(old, ignore_errors=True)
    with tarfile.open("/tmp/jetbrains-toolbox.tar.gz") as tf:
        tf.extractall(dest)
    apps = sorted(dest.glob("jetbrains-toolbox-*/bin/jetbrains-toolbox"))
    if not apps:
        raise helpers.TaskError("не найден бинарник JetBrains Toolbox")
    subprocess.Popen([str(apps[0])], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        if (dest / ".appState.json").exists():
            break
        time.sleep(1)
    if not (dest / ".appState.json").exists():
        raise helpers.TaskError("JetBrains Toolbox не запустился")

    # 13. Только для PC: OpenRGB, DeepCool, fix-docker-vpn
    if host == "pc":
        helpers.emit("── OpenRGB")
        helpers.emit("  Скачайте с https://gitlab.com/CalcProgrammer1/OpenRGB/-/releases:")
        helpers.emit("    • openrgb_*.deb          → в ~/Downloads")
        helpers.emit("    • 60-openrgb.rules       → в ~/Downloads")
        helpers.emit("  Для Ubuntu 24.04+ берите пакет *_trixie_*.deb, "
                     "для 22.04/23.x — *_bookworm_*.deb")
        helpers.emit("  Также включите в BIOS: Settings → Advanced → Mystic Light → Enabled")
        dl = home / "Downloads"
        while True:
            helpers.prompt("Нажмите Enter, когда файлы скачаны")
            debs = sorted(dl.glob("openrgb*.deb"))
            rules = sorted(dl.glob("60-openrgb.rules"))
            if debs and rules:
                local_deb, local_rules = str(debs[0]), str(rules[0])
                break
            helpers.emit("  В ~/Downloads не найдены openrgb*.deb и/или 60-openrgb.rules")
        helpers.apt_install("i2c-tools")
        helpers.run(["modprobe", "i2c-dev"], sudo=True, check=False)
        helpers.run(["modprobe", "i2c-i801"], sudo=True, check=False)
        helpers.append_line_sudo("/etc/modules", "i2c-dev")
        helpers.append_line_sudo("/etc/modules", "i2c-i801")
        helpers.run(["cp", local_rules, "/usr/lib/udev/rules.d/"], sudo=True)
        helpers.run(["udevadm", "control", "--reload-rules"], sudo=True)
        helpers.run(["udevadm", "trigger"], sudo=True)
        helpers.apt_install_deb(local_deb)
        if helpers.sed_replace_sudo("/etc/default/grub",
                                    r'^GRUB_CMDLINE_LINUX_DEFAULT="(.*)"$',
                                    r'GRUB_CMDLINE_LINUX_DEFAULT="\1 acpi_enforce_resources=lax"'):
            helpers.run(["update-grub"], sudo=True)

        helpers.emit("── DeepCool Digital")
        helpers.download(DEEPCOOL_URL, "/tmp/deepcool-digital-linux")
        helpers.run(["chmod", "+x", "/tmp/deepcool-digital-linux"])
        helpers.run(["cp", "/tmp/deepcool-digital-linux", "/usr/sbin/"], sudo=True)
        helpers.write_sudo("/etc/udev/rules.d/99-deepcool-digital.rules", DEEPCOOL_UDEV)
        helpers.run(["udevadm", "control", "--reload-rules"], sudo=True)
        helpers.run(["udevadm", "trigger"], sudo=True)
        helpers.write_sudo("/etc/systemd/system/deepcool-digital.service", DEEPCOOL_UNIT)
        helpers.run(["systemctl", "daemon-reload"], sudo=True)
        helpers.run(["systemctl", "enable", "deepcool-digital"], sudo=True)
        helpers.run(["systemctl", "start", "deepcool-digital"], sudo=True)

        helpers.emit("── fix-docker-vpn")
        helpers.write_sudo("/usr/local/sbin/fix-docker-vpn.sh", FIX_DOCKER_VPN_SCRIPT)
        helpers.run(["chmod", "+x", "/usr/local/sbin/fix-docker-vpn.sh"], sudo=True)
        helpers.write_sudo("/etc/systemd/system/fix-docker-vpn.service", FIX_DOCKER_VPN_UNIT)
        helpers.run(["systemctl", "daemon-reload"], sudo=True)
        helpers.run(["systemctl", "enable", "--now", "fix-docker-vpn.service"], sudo=True)


if __name__ == "__main__":
    sys.exit(helpers.task_main("install_packages", run))
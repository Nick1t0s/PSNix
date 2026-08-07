#!/usr/bin/env bash
# =====================================================================
#  Установщик программ — НОУТБУК (Ubuntu, свежая система)
#  Пакеты берутся из заметок Obsidian vault -> Ubuntu/*
#  Всё, кроме помеченного «только для ПК»
# =====================================================================

GREEN=$'\033[32m'
RED=$'\033[31m'
CYAN=$'\033[36m'
YELLOW=$'\033[33m'
BOLD=$'\033[1m'
RESET=$'\033[0m'

set -o pipefail

# Не даём apt/debconf/needrestart спрашивать интерактивно — иначе промпт
# уйдёт в лог и задача зависнет. Всё ручное — только в блоках ниже.
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a

SUCCESS=()
FAILED=()
declare -A LOGS

mkdir -p "$HOME/Downloads"

echo ""
echo "  ${BOLD}============================================${RESET}"
echo "  ${BOLD}  Установщик программ — НОУТБУК${RESET}"
echo "  ${BOLD}============================================${RESET}"
echo ""

# ---- sudo: спросить пароль один раз и держать кэш живым -------------
echo "  ${BOLD}Проверка sudo...${RESET}"
sudo -v || { echo "  ${RED}Нет прав sudo — выход.${RESET}"; exit 1; }
( trap '' INT; while true; do sudo -n true; sleep 60; done ) &
KEEPER=$!
trap 'kill $KEEPER 2>/dev/null' EXIT

# =====================================================================
#  Движок: вывод команды идёт в терминал в реальном времени (через tee)
#  и дублируется в лог для итогового вывода. Так как stdout/stderr —
#  пайп (не tty), curl/wget/snap сами прячут свои прогресс-бары, поэтому
#  в терминале нет мусора из управляющих последовательностей.
# =====================================================================
# Рекурсивно убивает процесс и всех его потомков (apt/snap часто
# порождают дочерние процессы — kill по одному PID их не снимет).
kill_tree() {
  local sig="$1" pid="$2" child
  for child in $(pgrep -P "$pid" 2>/dev/null); do
    kill_tree "$sig" "$child"
  done
  kill -"$sig" "$pid" 2>/dev/null
}

run() {
  local name="$1" fn="$2" log pid rc killed_manually=0
  log=$(mktemp)
  printf '\n  %b▶%b %b%s%b\n' "$CYAN" "$RESET" "$BOLD" "$name" "$RESET"
  # В фоновой под-оболочке bash сам подменяет stdin на /dev/null, поэтому
  # «0<&0» от этого не спасает — ввод не доходит до интерактивных промптов
  # (debconf и т.п.). Сохраняем настоящий stdin на fd 3 и пробрасываем его.
  exec 3<&0
  ( "$fn" 0<&3 2>&1 | tee "$log" ) &
  pid=$!
  exec 3<&-
  trap 'killed_manually=1; kill_tree TERM "$pid"; sleep 1; kill_tree KILL "$pid"' INT
  wait "$pid"; rc=$?
  trap - INT
  if [ "$killed_manually" -eq 1 ]; then
    printf '  %b✘%b %b%s%b %b(прервано Ctrl+C)%b\n' "$RED" "$RESET" "$BOLD" "$name" "$RESET" "$YELLOW" "$RESET"
    FAILED+=("$name")
    LOGS["$name"]="$log"
  elif [ "$rc" -eq 0 ]; then
    printf '  %b✔%b %b%s%b\n' "$GREEN" "$RESET" "$BOLD" "$name" "$RESET"
    SUCCESS+=("$name")
  else
    printf '  %b✘%b %b%s%b\n' "$RED" "$RESET" "$BOLD" "$name" "$RESET"
    FAILED+=("$name")
    LOGS["$name"]="$log"
  fi
}

# Очистка лога от ANSI-последовательностей и \r: прогресс-бары и переносы
# каретки перетирают строки в терминале и затирают соседний вывод (в т.ч. итог).
clean_log() {
  sed -r 's/\x1B\[[0-9;]*[A-Za-z]//g' "$1" | tr -d '\r'
}

# =====================================================================
#  Задачи
# =====================================================================

task_update() {
  sudo apt update
  sudo apt upgrade -y
  sudo apt autoremove -y
}

task_git() {
  sudo apt install -y git git-lfs
}

task_buildtools() {
  sudo apt install -y build-essential cmake
}

task_basics() {
  sudo apt install -y curl wget unzip p7zip-full
}

task_cli_tools() {
  sudo apt install -y ripgrep fd-find fzf bat eza tree ncdu duf
}

task_tmux() {
  sudo apt install -y tmux
}

task_monitoring() {
  sudo apt install -y btop nvtop iotop nload iftop nethogs
}

task_misc() {
  sudo apt install -y imagemagick rsync sshfs timeshift
}

task_flatpak() {
  sudo apt install -y flatpak
  flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
}

task_nekoray() {
  sudo apt install -y libxcb-xinerama0
  curl -fsSL --retry 5 --retry-all-errors -o /tmp/nekoray.deb https://github.com/MatsuriDayo/nekoray/releases/download/3.26/nekoray-3.26-2023-12-09-debian-x64.deb
  sudo apt install -y /tmp/nekoray.deb
}

task_nodejs() {
  sudo apt install -y nodejs npm
}

task_obs() {
  sudo snap install obs-studio
}

task_obsidian() {
  local ver
  ver=$(curl -fsSL https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest | sed -n 's/.*"tag_name": *"v\([^"]*\)".*/\1/p')
  [ -n "$ver" ] || { echo "  Не удалось получить версию Obsidian" >&2; return 1; }
  curl -fsSL --retry 5 --retry-all-errors -o /tmp/obsidian.deb \
    "https://github.com/obsidianmd/obsidian-releases/releases/download/v${ver}/obsidian_${ver}_amd64.deb"
  sudo apt install -y /tmp/obsidian.deb
}

task_okular() {
  sudo apt install -y okular okular-extra-backends
}

task_pdfarranger() {
  sudo apt install -y pdfarranger
}

task_openssh() {
  sudo apt install -y openssh-server
  sudo systemctl enable --now ssh
}

task_python() {
  sudo add-apt-repository -y ppa:deadsnakes/ppa
  sudo apt update
  sudo apt install -y \
    python3.9 python3.9-dev python3.9-venv \
    python3.10 python3.10-dev python3.10-venv \
    python3.11 python3.11-dev python3.11-venv \
    python3.12 python3.12-dev python3.12-venv \
    python3.13 python3.13-dev python3.13-venv
}

task_steam() {
  sudo dpkg --add-architecture i386
  sudo add-apt-repository -y multiverse
  sudo apt update
  sudo apt install -y steam
}

task_telegram() {
  sudo snap install telegram-desktop
}

task_thunderbird() {
  sudo snap install thunderbird
  snap connect thunderbird:fonts 2>/dev/null || true
}

task_vlc() {
  sudo apt install -y vlc
}

task_docker() {
  sudo apt remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
  sudo apt install -y ca-certificates curl gnupg
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --batch --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt update
  sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
  sudo systemctl enable --now docker
  sudo usermod -aG docker "$USER"
}

task_gh() {
  sudo apt install -y gh
}

task_ghostscript() {
  sudo apt install -y ghostscript
}

task_htop() {
  sudo apt install -y htop
}

task_jq() {
  sudo apt install -y jq
}

task_konsave() {
  sudo apt install -y pipx
  pipx ensurepath
  pipx install konsave
}

task_ollama() {
  local i
  echo "  Тихая установка, может занять несколько минут..."
  for i in 1 2 3; do
    curl -fsSL https://ollama.com/install.sh | sh >/dev/null 2>&1 && return 0
    sleep 3
  done
  return 1
}

task_opencode() {
  sudo snap install opencode --classic
}

task_jetbrains_toolbox() {
  local ver pid i dest app
  echo ""
  echo "  ${CYAN}JetBrains Toolbox${RESET}"
  echo "  ${YELLOW}Запустите Nekoray и подключите VPN${RESET}"
  echo "  ${YELLOW}Без VPN скачивание JetBrains Toolbox может не работать${RESET}"
  read -rp "  Нажмите Enter, когда VPN подключён: " _
  ver=$(curl -fsSL 'https://data.services.jetbrains.com/products/releases?code=TBA&latest=true&type=release' \
    | grep -o '"build":"[^"]*"' | head -n1 | cut -d'"' -f4)
  [ -n "$ver" ] || { echo "  Не удалось получить версию JetBrains Toolbox" >&2; return 1; }
  curl -fsSL --retry 5 --retry-all-errors -o /tmp/jetbrains-toolbox.tar.gz \
    "https://download.jetbrains.com/toolbox/jetbrains-toolbox-${ver}.tar.gz" \
    || { echo "  Ошибка скачивания JetBrains Toolbox" >&2; return 1; }
  dest="$HOME/.local/share/JetBrains/Toolbox"
  mkdir -p "$dest" || { echo "  Не удалось создать $dest" >&2; return 1; }
  rm -rf "$dest"/jetbrains-toolbox-* 2>/dev/null
  tar -xzf /tmp/jetbrains-toolbox.tar.gz -C "$dest" \
    || { echo "  Ошибка распаковки JetBrains Toolbox" >&2; return 1; }
  app=$(echo "$dest"/jetbrains-toolbox-*/bin/jetbrains-toolbox)
  [ -x "$app" ] || { echo "  Не найден бинарник JetBrains Toolbox" >&2; return 1; }
  "$app" >/dev/null 2>&1 &
  pid=$!
  for i in $(seq 1 30); do
    [ -e "$dest/.appState.json" ] && break
    sleep 1
  done
  [ -e "$dest/.appState.json" ] || { echo "  JetBrains Toolbox не запустился" >&2; return 1; }
}

task_firefox() {
  sudo apt install -y firefox
}

task_rust_coreutils() {
  sudo apt install -y rust-coreutils
}

task_samba() {
  sudo apt install -y samba smbclient
  sudo systemctl enable --now smbd
}

task_vim() {
  sudo apt install -y vim
}

task_yazi() {
  curl -fsSL https://yazi-rs.github.io/builds/yazi-keyring.gpg | sudo tee /usr/share/keyrings/yazi-keyring.gpg >/dev/null
  echo 'deb [signed-by=/usr/share/keyrings/yazi-keyring.gpg] https://yazi-rs.github.io/builds/ stable main' | \
    sudo tee /etc/apt/sources.list.d/yazi.list >/dev/null
  sudo apt update
  sudo apt install -y yazi
}

task_ytdlp() {
  sudo apt install -y yt-dlp
}

task_ffmpeg() {
  sudo apt install -y ffmpeg
}

task_rnote() {
  sudo snap install rnote
  snap connect rnote:removable-media 2>/dev/null || true
}

task_warthunder() {
  local archive cand dest launcher_dir
  # Архив лежит в корне репозитория (рядом со скриптом). На случай ручной
  # установки проверяем ещё ~/Downloads и текущую папку.
  archive=""
  for cand in \
    "$(cd "$(dirname "$0")" && pwd)/../wt_launcher_linux_"*.tar.gz \
    "$HOME/Downloads/wt_launcher_linux_"*.tar.gz \
    ./wt_launcher_linux_*.tar.gz; do
    [ -f "$cand" ] && { archive="$cand"; break; }
  done
  [ -n "$archive" ] || { echo "  Архив wt_launcher_linux_*.tar.gz не найден — положите его в корень репо" >&2; return 1; }

  dest="$HOME/wta"
  rm -rf "$dest"
  mkdir -p "$dest"
  tar -xzf "$archive" -C "$dest" || { echo "  Ошибка распаковки архива War Thunder" >&2; return 1; }
  launcher_dir="$dest/WarThunder"
  [ -x "$launcher_dir/launcher" ] || { echo "  Бинарник launcher не найден в $launcher_dir" >&2; return 1; }

  # Ярлык в меню + иконка (из launcher.ico, 256x256 PNG кадр)
  mkdir -p "$HOME/.local/share/applications" "$HOME/.local/share/icons/hicolor/256x256/apps"
  if command -v convert >/dev/null 2>&1; then
    convert "$launcher_dir/launcher.ico[5]" "$HOME/.local/share/icons/hicolor/256x256/apps/warthunder.png" || true
  fi
  cat > "$HOME/.local/share/applications/warthunder.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=War Thunder
Comment=Лаунчер War Thunder
Exec=$launcher_dir/launcher
Icon=warthunder
Terminal=false
Categories=Game;
EOF
}

# ---- только для ноутбука ----
task_autocpufreq() {
  sudo snap install auto-cpufreq
  sudo systemctl enable --now snap.auto-cpufreq.service.service
}

# =====================================================================
#  Установка
# =====================================================================
echo "  ${YELLOW}Вывод установки идёт в реальном времени. Если пакет завис —${RESET}"
echo "  ${YELLOW}нажмите ${BOLD}Ctrl+C${RESET}${YELLOW}: он будет убит и засчитан как проваленный.${RESET}"
echo ""

run "Обновление системы"        task_update
run "Git + git-lfs"             task_git
run "Инструменты сборки"        task_buildtools
run "Базовые утилиты"           task_basics
run "CLI-утилиты"               task_cli_tools
run "tmux"                      task_tmux
run "Мониторинг"                task_monitoring
run "Прочие утилиты"            task_misc
run "Flatpak + Flathub"         task_flatpak
run "Nekoray"                   task_nekoray
run "Node.js + npm"             task_nodejs
run "OBS Studio"                task_obs
run "Obsidian"                  task_obsidian
run "Okular"                    task_okular
run "PDF Arranger"              task_pdfarranger
run "OpenSSH-сервер"            task_openssh
run "Python 3.9-3.13"           task_python
run "Steam"                     task_steam
run "Telegram"                  task_telegram
run "Thunderbird"               task_thunderbird
run "VLC"                       task_vlc
run "Docker"                    task_docker
run "GitHub CLI (gh)"           task_gh
run "Ghostscript"               task_ghostscript
run "htop"                      task_htop
run "jq"                        task_jq
run "Konsave"                   task_konsave
run "Ollama"                    task_ollama
run "OpenCode"                  task_opencode
run "JetBrains Toolbox"         task_jetbrains_toolbox
run "Firefox"                   task_firefox
run "rust-coreutils"            task_rust_coreutils
run "Samba + smbclient"         task_samba
run "Vim"                       task_vim
run "Yazi"                      task_yazi
run "yt-dlp"                    task_ytdlp
run "ffmpeg"                    task_ffmpeg
run "Rnote"                     task_rnote
run "War Thunder"               task_warthunder
run "auto-cpufreq"              task_autocpufreq

# ---- Zoom (интерактивно) ----
echo ""
echo "  ${CYAN}Zoom${RESET}"
echo "  Скачайте Zoom: ${YELLOW}https://zoom.us/download?os=linux${RESET}"
echo "  Пакет zoom_amd64.deb должен попасть в ${BOLD}~/Downloads${RESET}"
zoom_log=$(mktemp)
while :; do
  read -rp "  Нажмите Enter, когда файл скачан: " _
  deb=$(ls "$HOME/Downloads"/zoom*.deb 2>/dev/null | head -n1)
  [ -n "$deb" ] && break
  echo "  ${RED}Файл zoom*.deb не найден в ~/Downloads${RESET}"
done
if sudo apt install -y "$deb" >"$zoom_log" 2>&1; then
  printf '  %b✔%b %b%s%b\033[K\n' "$GREEN" "$RESET" "$BOLD" "Zoom" "$RESET"
  SUCCESS+=("Zoom")
else
  printf '  %b✘%b %b%s%b\033[K\n' "$RED" "$RESET" "$BOLD" "Zoom" "$RESET"
  FAILED+=("Zoom")
  LOGS["Zoom"]="$zoom_log"
fi

# =====================================================================
#  Итог
# =====================================================================
echo ""
echo "  ${BOLD}════════════════ ИТОГ ════════════════${RESET}"
echo "  Успешно: ${GREEN}${#SUCCESS[@]}${RESET}   Провал: ${RED}${#FAILED[@]}${RESET}"
if [ "${#SUCCESS[@]}" -gt 0 ]; then
  echo ""
  echo "  ${GREEN}Установлено:${RESET}"
  for name in "${SUCCESS[@]}"; do
    echo "    ✔ $name"
  done
fi
if [ "${#FAILED[@]}" -gt 0 ]; then
  echo ""
  echo "  ${RED}Не удалось поставить:${RESET}"
  for name in "${FAILED[@]}"; do
    echo "    ✘ $name"
  done
  for name in "${FAILED[@]}"; do
    echo ""
    echo "  ${BOLD}──── Полный вывод: $name ────${RESET}"
    clean_log "${LOGS[$name]}"
  done
fi

echo ""
echo "  ${YELLOW}После завершения выйдите/зайдите в систему (или перезагрузитесь),${RESET}"
echo "  ${YELLOW}чтобы применились права группы docker и прочие изменения.${RESET}"
echo ""

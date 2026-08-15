#!/usr/bin/env bash
# Архив лежит в корне репозитория (рядом с install.py). На случай ручной
# установки проверяем ещё ~/Downloads и текущую папку.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
archive=""
for cand in \
  "$REPO_ROOT"/wt_launcher_linux_*.tar.gz \
  "$HOME/Downloads/wt_launcher_linux_"*.tar.gz \
  ./wt_launcher_linux_*.tar.gz; do
  [ -f "$cand" ] && { archive="$cand"; break; }
done
[ -n "$archive" ] || { echo "  Архив wt_launcher_linux_*.tar.gz не найден — положите его в корень репо" >&2; exit 1; }

dest="$HOME/wta"
rm -rf "$dest"
mkdir -p "$dest"
tar -xzf "$archive" -C "$dest" || { echo "  Ошибка распаковки архива War Thunder" >&2; exit 1; }
launcher_dir="$dest/WarThunder"
[ -x "$launcher_dir/launcher" ] || { echo "  Бинарник launcher не найден в $launcher_dir" >&2; exit 1; }

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
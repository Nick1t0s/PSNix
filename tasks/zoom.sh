#!/usr/bin/env bash
# Zoom: deb-пакет скачивается вручную с https://zoom.us/download?os=linux
echo ""
echo "  Скачайте Zoom: https://zoom.us/download?os=linux"
echo "  Пакет zoom_amd64.deb должен попасть в папку загрузок"

find_zoom_deb() {
  local d cand
  for d in "$(xdg-user-dir DOWNLOAD 2>/dev/null)" "$HOME/Downloads" "$HOME/Desktop"; do
    [ -n "$d" ] && [ -d "$d" ] || continue
    for cand in "$d"/zoom*.deb "$d"/Zoom*.deb; do
      [ -f "$cand" ] && { echo "$cand"; return 0; }
    done
  done
  return 1
}

deb=""
while :; do
  read -rp "  Нажмите Enter, когда файл скачан: " _
  deb="$(find_zoom_deb)"
  [ -n "$deb" ] && break
  echo "  Файл zoom*.deb не найден."
  for d in "$(xdg-user-dir DOWNLOAD 2>/dev/null)" "$HOME/Downloads" "$HOME/Desktop"; do
    [ -n "$d" ] && [ -d "$d" ] || continue
    echo "  Содержимое $d:"
    ls -1 "$d" 2>/dev/null | sed 's/^/    /'
  done
  read -rp "  Введите путь к файлу вручную (или пусто — продолжить поиск): " manual
  [ -n "$manual" ] && [ -f "$manual" ] && { deb="$manual"; break; }
done
sudo apt install -y "$deb" || exit 1

# Нативный файловый диалог вместо портала: Zoom (Qt + CEF) иначе уходит
# в терминальный файл-пикер (yazi). User-level .desktop перекрывает системный
# и переживает обновления Zoom.
mkdir -p "$HOME/.local/share/applications"
if [ ! -f "$HOME/.local/share/applications/Zoom.desktop" ]; then
  cat > "$HOME/.local/share/applications/Zoom.desktop" <<EOF
[Desktop Entry]
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
EOF
  update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
fi
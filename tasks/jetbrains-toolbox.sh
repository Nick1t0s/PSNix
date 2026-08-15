#!/usr/bin/env bash
echo ""
echo "  JetBrains Toolbox"
echo "  Запустите Nekoray и подключите VPN"
echo "  Без VPN скачивание JetBrains Toolbox может не работать"
read -rp "  Нажмите Enter, когда VPN подключён: " _
ver=$(curl -fsSL 'https://data.services.jetbrains.com/products/releases?code=TBA&latest=true&type=release' \
  | grep -o '"build":"[^"]*"' | head -n1 | cut -d'"' -f4)
[ -n "$ver" ] || { echo "  Не удалось получить версию JetBrains Toolbox" >&2; exit 1; }
curl -fsSL --retry 5 --retry-all-errors -o /tmp/jetbrains-toolbox.tar.gz \
  "https://download.jetbrains.com/toolbox/jetbrains-toolbox-${ver}.tar.gz" \
  || { echo "  Ошибка скачивания JetBrains Toolbox" >&2; exit 1; }
dest="$HOME/.local/share/JetBrains/Toolbox"
mkdir -p "$dest" || { echo "  Не удалось создать $dest" >&2; exit 1; }
rm -rf "$dest"/jetbrains-toolbox-* 2>/dev/null
tar -xzf /tmp/jetbrains-toolbox.tar.gz -C "$dest" \
  || { echo "  Ошибка распаковки JetBrains Toolbox" >&2; exit 1; }
app=$(echo "$dest"/jetbrains-toolbox-*/bin/jetbrains-toolbox)
[ -x "$app" ] || { echo "  Не найден бинарник JetBrains Toolbox" >&2; exit 1; }
"$app" >/dev/null 2>&1 &
pid=$!
for i in $(seq 1 30); do
  [ -e "$dest/.appState.json" ] && break
  sleep 1
done
[ -e "$dest/.appState.json" ] || { echo "  JetBrains Toolbox не запустился" >&2; exit 1; }
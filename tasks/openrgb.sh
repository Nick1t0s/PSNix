#!/usr/bin/env bash
# Только для ПК
echo ""
echo "  OpenRGB"
echo "  Скачайте с https://gitlab.com/CalcProgrammer1/OpenRGB/-/releases:"
echo "    • openrgb_*.deb          → в ~/Downloads"
echo "    • 60-openrgb.rules       → в ~/Downloads"
echo "  Для Ubuntu 24.04+ берите пакет *_trixie_*.deb, для 22.04/23.x — *_bookworm_*.deb"
echo "  Также включите в BIOS: Settings → Advanced → Mystic Light → Enabled"
local_deb=""; local_rules=""
while :; do
  read -rp "  Нажмите Enter, когда файлы скачаны: " _
  local_deb=$(ls "$HOME/Downloads"/openrgb*.deb 2>/dev/null | head -n1)
  local_rules=$(ls "$HOME/Downloads"/60-openrgb.rules 2>/dev/null | head -n1)
  [ -n "$local_deb" ] && [ -n "$local_rules" ] && break
  echo "  В ~/Downloads не найдены openrgb*.deb и/или 60-openrgb.rules"
done
sudo apt install -y i2c-tools
sudo modprobe i2c-dev || true
sudo modprobe i2c-i801 || true
echo "i2c-dev"   | sudo tee -a /etc/modules > /dev/null
echo "i2c-i801"  | sudo tee -a /etc/modules > /dev/null
sudo cp "$local_rules" /usr/lib/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo apt install -y "$local_deb"
if ! grep -q 'acpi_enforce_resources=lax' /etc/default/grub; then
  sudo sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT="\(.*\)"$/GRUB_CMDLINE_LINUX_DEFAULT="\1 acpi_enforce_resources=lax"/' /etc/default/grub
  sudo update-grub
fi
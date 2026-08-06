# Nekoray — установка (Ubuntu)

> Репозиторий [MatsuriDayo/nekoray](https://github.com/MatsuriDayo/nekoray) архивирован, последний релиз **3.26**. TUN-режим (нужен для fix-docker-vpn) работает только в `.deb` — AppImage не поддерживает TUN.

## Установка (.deb)

```bash
# зависимости
sudo apt install libxcb-xinerama0

# скачать последний релиз 3.26
curl -L -O https://github.com/MatsuriDayo/nekoray/releases/download/3.26/nekoray-3.26-2023-12-09-debian-x64.deb

# установить
sudo apt install ./nekoray-3.26-2023-12-09-debian-x64.deb
```

Запуск из меню приложений — "NekoRay". TUN-режим включается в настройках ядра (`内核设置 → TUN`); для этого нужны права root.

## fix-docker-vpn

Скрипт и systemd-сервис, чтобы Docker оставался доступным при поднятом Nekoray TUN:

```# 1) скрипт (пересоздаём начисто, права даём отдельно)
sudo tee /usr/local/sbin/fix-docker-vpn.sh >/dev/null <<'EOF'
#!/bin/bash
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
  ip -4 -o route show | awk '/dev (docker0|br-)/{print $1, $3}' | \
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
EOF
sudo chmod +x /usr/local/sbin/fix-docker-vpn.sh

# 2) unit
sudo tee /etc/systemd/system/fix-docker-vpn.service >/dev/null <<'EOF'
[Unit]
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
EOF

# 3) запуск
sudo systemctl daemon-reload
sudo systemctl enable --now fix-docker-vpn.service
systemctl status fix-docker-vpn.service --no-pager
```

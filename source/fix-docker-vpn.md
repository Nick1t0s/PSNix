ТОЛЬКО ДЛЯ ПК
# fix-docker-vpn — доступ к Docker при поднятом Nekoray TUN

> Скрипт и systemd-сервис, который держит Docker-контейнеры доступными, пока поднят туннель `neko-tun` от Nekoray. Настроен под проводную сеть ПК `enp4s0`.

---

## Требования

- ПК с проводной сетью `enp4s0` (на ноутбуке интерфейс другой — скрипт адаптировать)
- Установленный и запущенный Nekoray
- Docker

---

## Шаг 1 — Скрипт

```bash
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
```

---

## Шаг 2 — systemd-сервис

```bash
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
```

---

## Шаг 3 — Запуск

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now fix-docker-vpn.service
systemctl status fix-docker-vpn.service --no-pager
```

---

## Ручная очистка (снести правило вручную)

```bash
PHYS=enp4s0; TABLE=200
GW=$(ip -4 route show default | awk '/default/{print $3; exit}')
HOSTIP=$(ip -4 -o addr show "$PHYS" | awk '{print $4}' | cut -d/ -f1 | head -1)

# чисто снести наше предыдущее
sudo ip rule del pref 100 2>/dev/null
sudo ip route flush table $TABLE 2>/dev/null
sudo iptables -t mangle -D PREROUTING -i "$PHYS"  -j MARK --set-mark 0x1 2>/dev/null
sudo iptables -t mangle -D PREROUTING -i br+     -m conntrack --ctstate ESTABLISHED,RELATED -j MARK --set-mark 0x1 2>/dev/null
sudo iptables -t mangle -D PREROUTING -i docker0 -m conntrack --ctstate ESTABLISHED,RELATED -j MARK --set-mark 0x1 2>/dev/null

# таблица 200 = docker-сети + default наружу + local хоста
ip -4 -o route show | awk '/dev (docker0|br-)/{print $1, $3}' | \
  while read net dev; do sudo ip route add "$net" dev "$dev" table $TABLE 2>/dev/null; done
sudo ip route add default via "$GW" dev "$PHYS" table $TABLE
sudo ip route add local "$HOSTIP"/32 dev lo table $TABLE

# метки
sudo iptables -t mangle -I PREROUTING -i "$PHYS"  -j MARK --set-mark 0x1
sudo iptables -t mangle -I PREROUTING -i br+     -m conntrack --ctstate ESTABLISHED,RELATED -j MARK --set-mark 0x1
sudo iptables -t mangle -I PREROUTING -i docker0 -m conntrack --ctstate ESTABLISHED,RELATED -j MARK --set-mark 0x1
sudo ip rule add fwmark 0x1/0xffffffff lookup $TABLE pref 100
```

> Внимание: `sudo ip rule del pref 9003` (правило Nekoray) нужно удалять всегда отдельно — см. Nekoray.md.

# VirtualBox (ручная установка)

> ⚠️ Интерактивная установка: во время `apt install virtualbox-ext-pack`
> нужно вручную принять лицензию Oracle PUEL. Поэтому VirtualBox не входит
> в автоматические группы.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка (принять лицензию в терминале)

```bash
sudo apt update && sudo apt install -y virtualbox virtualbox-ext-pack linux-headers-generic && sudo usermod -aG vboxusers "$USER" && echo "VirtualBox установлен. Выйдите из системы и зайдите снова, чтобы применилась группа vboxusers."
```

Во время установки `virtualbox-ext-pack` появится текст лицензии Oracle PUEL —
пролистай и прими её.

---

## Шаг 2 — Перелогин

Выйди из системы и зайди снова, чтобы применилась группа `vboxusers`
(нужна для доступа к USB-устройствам в гостевых VM).

---

## Проверка

```bash
vboxmanage --version
groups | grep vboxusers
```

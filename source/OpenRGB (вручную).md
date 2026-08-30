# OpenRGB (ручная установка) — только для ПК

> ⚠️ Интерактивная установка: пакеты `openrgb_*.deb` и `60-openrgb.rules`
> скачиваются вручную с GitLab. Настройка подсветки MSI B760 Gaming Plus WiFi.

---

## Требования

- Ubuntu 22.04 или новее
- Права `sudo`
- Плата MSI B760 Gaming Plus WiFi

---

## Шаг 1 — Включить подсветку в BIOS

1. Перезагрузка → **Del** для входа в BIOS
2. **Settings → Advanced → Mystic Light** → **Enabled**
3. Сохранить — **F10**

---

## Шаг 2 — Скачать вручную

С [официальной страницы релизов](https://gitlab.com/CalcProgrammer1/OpenRGB/-/releases) → в `~/Downloads`:

- `60-openrgb.rules` — правила udev
- `openrgb_1.0rc2_amd64_bookworm_0fca93e.deb` — для Ubuntu 22.04/23.x
- `openrgb_1.0rc2_amd64_trixie_0fca93e.deb` — для Ubuntu 24.04+

---

## Шаг 3 — Модули i2c

```bash
sudo apt install i2c-tools
sudo modprobe i2c-dev
sudo modprobe i2c-i801
```

Автозагрузка при старте:

```bash
echo "i2c-dev" | sudo tee -a /etc/modules
echo "i2c-i801" | sudo tee -a /etc/modules
```

---

## Шаг 4 — Параметр ядра

В `/etc/default/grub` добавь `acpi_enforce_resources=lax`:

```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash acpi_enforce_resources=lax"
```

Применить:

```bash
sudo update-grub
sudo reboot
```

---

## Шаг 5 — Установка udev-правил и пакета

```bash
sudo cp ~/Downloads/60-openrgb.rules /usr/lib/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo apt install ~/Downloads/openrgb_1.0rc2_amd64_*.deb -y
```

> Если файл правил уже есть в `/etc/udev/rules.d/` — удали дубликат:
> `sudo rm /etc/udev/rules.d/60-openrgb.rules && sudo udevadm control --reload-rules`

---

## Шаг 6 — Настроить зоны в OpenRGB

При первом запуске появится окно **Resize the zones**. Укажи количество светодиодов:

|Зона|Устройства|LED|
|---|---|---|
|JRAINBOW1|2 подсветки|20|
|JRAINBOW2|7 кулеров × 16|112|

Нажать **Save and close**.

---

## Шаг 7 — Проверка устройств

```bash
openrgb --list-devices
```

Ожидаемый вывод:

```
0: MSI B760 GAMING PLUS WIFI (MS-7D98)
  Zones: JRGB1  JRAINBOW1  JRAINBOW2
```

Индексы зон: JRGB1=0, JRAINBOW1=1, JRAINBOW2=2.

---

## Шаг 8 — Скрипты управления

`~/rgb-on.sh`:

```bash
#!/bin/bash
openrgb --device 0 --zone 1 --mode static --color FF0000  # JRAINBOW1 красный
openrgb --device 0 --zone 2 --mode static --color 00FF00  # JRAINBOW2 зелёный
```

`~/rgb-off.sh`:

```bash
#!/bin/bash
openrgb --device 0 --zone 1 --mode static --color 000000
openrgb --device 0 --zone 2 --mode static --color 000000
```

```bash
chmod +x ~/rgb-on.sh ~/rgb-off.sh
~/rgb-on.sh   # включить
~/rgb-off.sh  # выключить
```

> `Connection attempt failed` — это нормально: сервер OpenRGB не запущен, команды всё равно выполняются.

---

## Шаг 9 — Автоматизация по расписанию (cron)

```bash
crontab -e
```

Добавить в конец:

```
0 8  * * * /home/nik/rgb-on.sh
0 22 * * * /home/nik/rgb-off.sh
```

Проверка: `crontab -l`.

---

## Шаг 10 — Сервисы (опционально)

### Выключать при выходе системы — `/etc/systemd/system/rgb-off.service`:

```ini
[Unit]
Description=Turn off RGB on shutdown
DefaultDependencies=no
Before=shutdown.target

[Service]
Type=oneshot
ExecStart=/home/nik/rgb-off.sh

[Install]
WantedBy=shutdown.target
```

```bash
sudo systemctl enable rgb-off.service
```

### Выключать при засыпании, включать при пробуждении — `/etc/systemd/system/rgb-sleep.service`:

```ini
[Unit]
Description=RGB on suspend/resume
Before=sleep.target
StopWhenUnneeded=yes

[Service]
Type=oneshot
ExecStart=/home/nik/rgb-off.sh
ExecStop=/home/nik/rgb-on.sh
RemainAfterExit=yes

[Install]
WantedBy=sleep.target
```

```bash
sudo systemctl enable rgb-sleep.service
```

---

## Справка: команды OpenRGB

```bash
openrgb --list-devices                                   # список устройств
openrgb --device 0 --zone 1 --mode static --color FF0000 # цвет зоны
openrgb --profile "my_profile"                           # загрузить профиль
openrgb --device 0 --mode static --color 000000          # выключить всё
```

Режимы: `static`, `breathing`, `flashing`, `rainbow wave`, `meteor`.

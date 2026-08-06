ТОЛЬКО ДЛЯ ПК
# Управление подсветкой MSI B760 Gaming Plus WiFi в Ubuntu

## Требования

- Ubuntu 22.04 или новее
- OpenRGB 1.0+
- Плата MSI B760 Gaming Plus WiFi

---

## Шаг 1 — Включить подсветку в BIOS

1. Перезагрузка → **Del** для входа в BIOS
2. **Settings → Advanced → Mystic Light**
3. Поставить **Enabled**
4. Сохранить — **F10**

---

## Шаг 2 — Загрузить модули i2c

```bash
sudo apt install i2c-tools
sudo modprobe i2c-dev
sudo modprobe i2c-i801
```

Автозагрузка при старте системы:

```bash
echo "i2c-dev" | sudo tee -a /etc/modules
echo "i2c-i801" | sudo tee -a /etc/modules
```

---

## Шаг 3 — Добавить параметр ядра

Открыть `/etc/default/grub` и добавить `acpi_enforce_resources=lax`:

```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash acpi_enforce_resources=lax"
```

Применить:

```bash
sudo update-grub
sudo reboot
```

---

## Шаг 4 — Установить OpenRGB

Скачать с [официальной страницы релизов](https://gitlab.com/CalcProgrammer1/OpenRGB/-/releases):

- `60-openrgb.rules` — правила udev
- `openrgb_1.0rc2_amd64_bookworm_0fca93e.deb` — для Ubuntu 22.04/23.x
- `openrgb_1.0rc2_amd64_trixie_0fca93e.deb` — для Ubuntu 24.04+

```bash
# Установить udev правила
sudo cp ~/Downloads/60-openrgb.rules /usr/lib/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger

# Установить пакет
sudo dpkg -i ~/Downloads/openrgb_1.0rc2_amd64_bookworm_0fca93e.deb
```

> Если файл правил уже есть в `/etc/udev/rules.d/` — удалите дубликат:
> 
> ```bash
> sudo rm /etc/udev/rules.d/60-openrgb.rules
> sudo udevadm control --reload-rules
> ```

---

## Шаг 5 — Настроить зоны в OpenRGB

При первом запуске OpenRGB появится окно **Resize the zones**. Укажите количество светодиодов:

|Зона|Устройства|LED|
|---|---|---|
|JRAINBOW1|2 подсветки|20|
|JRAINBOW2|7 кулеров × 16|112|

Нажать **Save and close**.

---

## Шаг 6 — Проверить устройства

```bash
openrgb --list-devices
```

Пример вывода для MSI B760:

```
0: MSI B760 GAMING PLUS WIFI (MS-7D98)
  Zones: JRGB1  JRAINBOW1  JRAINBOW2
```

Индексы зон: JRGB1=0, JRAINBOW1=1, JRAINBOW2=2

---

## Шаг 7 — Создать скрипты управления

### Включение подсветки (`~/rgb-on.sh`)

```bash
#!/bin/bash
openrgb --device 0 --zone 1 --mode static --color FF0000  # JRAINBOW1 красный
openrgb --device 0 --zone 2 --mode static --color 00FF00  # JRAINBOW2 зелёный
```

### Выключение подсветки (`~/rgb-off.sh`)

```bash
#!/bin/bash
openrgb --device 0 --zone 1 --mode static --color 000000
openrgb --device 0 --zone 2 --mode static --color 000000
```

Сделать исполняемыми:

```bash
chmod +x ~/rgb-on.sh ~/rgb-off.sh
```

Проверить:

```bash
~/rgb-on.sh   # включить
~/rgb-off.sh  # выключить
```

> Сообщение `Connection attempt failed` — это нормально. Оно означает лишь что сервер OpenRGB не запущен, команды всё равно выполняются.

---

## Шаг 8 — Автоматизация по расписанию

```bash
crontab -e
```

Добавить в конец файла:

```
0 8  * * * /home/nik/rgb-on.sh
0 22 * * * /home/nik/rgb-off.sh
```

Сохранить: **Ctrl+O** → Enter → **Ctrl+X**

Проверить что задания записались:

```bash
crontab -l
```

---

## Справка: полезные команды OpenRGB

```bash
# Список устройств
openrgb --list-devices

# Статичный цвет на зону
openrgb --device 0 --zone 1 --mode static --color FF0000

# Загрузить сохранённый профиль
openrgb --profile "my_profile"

# Выключить всю подсветку
openrgb --device 0 --mode static --color 000000
```

### Режимы подсветки

|Режим|Описание|
|---|---|
|`static`|Статичный цвет|
|`breathing`|Плавное мигание|
|`flashing`|Мигание|
|`rainbow wave`|Радужная волна|
|`meteor`|Метеор|

---

## Дополнительная автоматизация

### Выключать при выходе системы

```bash
sudo nano /etc/systemd/system/rgb-off.service
```

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

### Выключать при засыпании, включать при пробуждении

```bash
sudo nano /etc/systemd/system/rgb-sleep.service
```

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
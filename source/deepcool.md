ТОЛЬКО ДЛЯ ПК
# DeepCool AK620 Digital — Установка на Linux (Ubuntu/Debian/Mint)

> Инструкция по установке неофициального драйвера [`deepcool-digital-linux`](https://github.com/Nortank12/deepcool-digital-linux) для отображения температуры CPU на экране кулера.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`
- Кулер подключён по USB к материнской плате

---

## Шаг 1 — Скачай бинарник

```bash
wget https://github.com/Nortank12/deepcool-digital-linux/releases/latest/download/deepcool-digital-linux
```

---

## Шаг 2 — Сделай файл исполняемым

```bash
chmod +x deepcool-digital-linux
```

---

## Шаг 3 — Проверь, что кулер определяется

```bash
sudo ./deepcool-digital-linux --list
```

Ожидаемый вывод:

```
Device list [PID | Name]
-----
X | AK620 DIGITAL
```

Если кулер виден — всё идёт хорошо.

---

## Шаг 4 — Тестовый запуск

```bash
sudo ./deepcool-digital-linux
```

Экран кулера должен ожить и показать температуру CPU.  
Нажми `Ctrl+C` чтобы остановить.

---

## Шаг 5 — Автозапуск через systemd

### 5.1 Скопируй бинарник в системную папку

```bash
sudo cp ./deepcool-digital-linux /usr/sbin/
```

### 5.2 Создай файл сервиса

```bash
sudo nano /etc/systemd/system/deepcool-digital.service
```

Вставь следующее содержимое:

```ini
[Unit]
Description=DeepCool Digital

[Service]
ExecStart=/usr/sbin/deepcool-digital-linux
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Сохрани файл: `Ctrl+O` → `Enter` → `Ctrl+X`

### 5.3 Включи и запусти сервис

```bash
sudo systemctl enable deepcool-digital
sudo systemctl start deepcool-digital
```

Теперь экран будет включаться автоматически при каждой загрузке системы.

---

## Полезные команды

|Команда|Описание|
|---|---|
|`sudo systemctl status deepcool-digital`|Проверить статус сервиса|
|`sudo systemctl stop deepcool-digital`|Остановить сервис|
|`sudo systemctl restart deepcool-digital`|Перезапустить сервис|
|`sudo journalctl -u deepcool-digital -n 50`|Посмотреть логи|

---

## Дополнительные параметры запуска

```
sudo deepcool-digital-linux [OPTIONS]

  -m, --mode <MODE>       Режим отображения
  -f, --fahrenheit        Температура в °F
  -a, --alarm             Включить звуковой сигнал при перегреве
  -u, --update <MS>       Интервал обновления в миллисекундах (по умолчанию: 1000)
  -l, --list              Список подключённых устройств
  -h, --help              Показать справку
```

---

## Устранение неполадок

### Кулер не определяется (`--list` ничего не показывает)

Проверь, что USB подключён к материнской плате, и выполни:

```bash
lsusb | grep -i 3633
```

Если устройство есть, но нет доступа — создай udev-правило:

```bash
echo 'SUBSYSTEM=="hidraw", ATTRS{idVendor}=="3633", MODE="0666"' | sudo tee /etc/udev/rules.d/99-deepcool-digital.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### Сервис не запускается

```bash
sudo journalctl -u deepcool-digital -n 50
```

---

## Ссылки

- [GitHub репозиторий](https://github.com/Nortank12/deepcool-digital-linux)
- [Последний релиз](https://github.com/Nortank12/deepcool-digital-linux/releases/latest)
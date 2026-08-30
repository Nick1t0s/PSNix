# 07 — Snap-приложения

> Приложения из Snap Store: мессенджеры, запись экрана, почта.
> Отдельно — auto-cpufreq (только для ноутбука).

---

## Требования

- Ubuntu / Debian / Linux Mint (snap предустановлен в Ubuntu; иначе `sudo apt install snapd`)
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo snap install telegram-desktop
sudo snap install obs-studio
sudo snap install thunderbird
```

---

## Шаг 2 — Подключение разрешений

```bash
sudo snap connect thunderbird:fonts   # системные шрифты для Thunderbird
```

Проверка подключений: `snap connections thunderbird`.

---

## Шаг 3 — Проверка

```bash
snap list telegram-desktop obs-studio thunderbird
```

---

## Только для ноутбука — auto-cpufreq

> Автоматическое управление частотой CPU (батарея/сеть). На ПК не нужен.

```bash
sudo snap install auto-cpufreq
sudo systemctl enable --now snap.auto-cpufreq.service
```

Проверка: `snap services auto-cpufreq` — сервис `active (running)`, `Startup: enabled`.

|Команда|Описание|
|---|---|
|`sudo auto-cpufreq --stats`|Текущий режим работы|
|`sudo auto-cpufreq --live`|Переключения частоты в реальном времени|
|`sudo systemctl stop snap.auto-cpufreq.service`|Остановить сервис|

---

## Обновление

```bash
sudo snap refresh telegram-desktop obs-studio thunderbird
```

---

## Устранение неполадок

- **OBS не захватывает экран на Wayland** — используй источник «Захват экрана (PipeWire)».
- **OBS нет звука** — в настройках аудио выбери мониторы PipeWire (`Monitor of ...`).
- **Telegram не приходят уведомления** — проверь `snap connections telegram-desktop`.

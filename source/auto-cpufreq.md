ТОЛЬКО ДЛЯ НОУТА
# auto-cpufreq — автоматическое управление частотой CPU

> Инструмент для автономной работы и производительности на ноутбуках. Подбирает оптимальную частоту процессора в зависимости от нагрузки и питания (батарея/сеть).

---

## Требования

- Ноутбук (на ПК не требуется)
- Snap

---

## Шаг 1 — Установка

```bash
sudo snap install auto-cpufreq
```

---

## Шаг 2 — Активация сервиса

```bash
sudo systemctl enable --now snap.auto-cpufreq.service
```

---

## Шаг 3 — Проверка

```bash
snap services auto-cpufreq
systemctl status snap.auto-cpufreq.service --no-pager
```

Ожидаемый вывод: сервис `active (running)`, `Startup: enabled`.

---

## Полезные команды

|Команда|Описание|
|---|---|
|`sudo auto-cpufreq --stats`|Текущие настройки и режим работы|
|`sudo auto-cpufreq --live`|Просмотр переключений частоты в реальном времени|
|`sudo systemctl stop snap.auto-cpufreq.service`|Остановить сервис|
|`sudo systemctl start snap.auto-cpufreq.service`|Запустить сервис|

---

## Устранение неполадок

### Сервис не запускается

```bash
sudo journalctl -u snap.auto-cpufreq.service -n 50
```

### Проверить поддерживается ли CPU

```bash
grep -c processor /proc/cpuinfo
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver
```

Если в `scaling_driver` указан `intel_pstate` или `amd_pstate` — всё работает.

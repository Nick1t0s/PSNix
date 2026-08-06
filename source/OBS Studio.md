# OBS Studio

> Запись экрана, трансляции и стриминг. Устанавливается через Snap.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Snap (предустановлен в Ubuntu)

---

## Шаг 1 — Установка

```bash
sudo snap install obs-studio
```

---

## Шаг 2 — Проверка

```bash
snap list obs-studio
obs-studio --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`obs-studio`|Запустить из терминала|
|`sudo snap refresh obs-studio`|Обновление вручную|

---

## Устранение неполадок

### Не работает захват экрана в Wayland

Используй **Сборка → Источник → Захват экрана (PipeWire)** — он работает на Wayland, в отличие от X11-захвата.

### Нет звука в записи

Проверь, что в настройках аудио выбраны мониторы PipeWire (`Monitor of ...`).

---

## Ссылки

- [obsproject.com](https://obsproject.com/)
- [OBS на Snapcraft](https://snapcraft.io/obs-studio)

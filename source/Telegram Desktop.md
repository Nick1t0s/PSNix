# Telegram Desktop

> Официальный клиент мессенджера Telegram для десктопа. Устанавливается через Snap.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Snap (предустановлен в Ubuntu)

---

## Шаг 1 — Установка

```bash
sudo snap install telegram-desktop
```

---

## Шаг 2 — Проверка

```bash
snap list telegram-desktop
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`telegram-desktop`|Запустить из терминала|
|`sudo snap refresh telegram-desktop`|Обновление вручную|

---

## Устранение неполадок

### Не приходят уведомления

Проверь в настройках Snap, что подключено системное уведомление:

```bash
snap connections telegram-desktop
```

---

## Ссылки

- [telegram.org](https://telegram.org/)
- [Telegram на Snapcraft](https://snapcraft.io/telegram-desktop)

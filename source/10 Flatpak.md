# 10 — Flatpak и Flathub

> Кроссплатформенный менеджер пакетов с песочницей: свежие версии приложений
> из Flathub в изолированной среде.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка и подключение Flathub

```bash
sudo apt install flatpak -y
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

---

## Шаг 2 — Перезагрузка

Перезапусти систему, чтобы Flatpak-приложения появились в меню:

```bash
sudo reboot
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`flatpak install flathub <app-id>`|Установить приложение|
|`flatpak run <app-id>`|Запустить приложение|
|`flatpak list`|Список установленных|
|`flatpak update`|Обновить всё|
|`flatpak uninstall <app-id>`|Удалить приложение|

---

## Устранение неполадок

- **Приложения не видны в меню** — поставь плагин интеграции:
  `sudo apt install xdg-desktop-portal-kde -y` (для GNOME — `xdg-desktop-portal-gtk`).

---

## Ссылки

- [Flathub](https://flathub.org/)

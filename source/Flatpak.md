# Flatpak

> Кроссплатформенный менеджер пакетов с песочницей. Позволяет ставить свежие версии приложений из Flathub в изолированной среде.

---

## Требования

- Ubuntu / Debian / Linux Mint
- `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install flatpak -y
```

---

## Шаг 2 — Добавить Flathub

```bash
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

---

## Шаг 3 — Перезагрузка

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
|`flatpak list`|Список установленных приложений|
|`flatpak update`|Обновить всё|
|`flatpak uninstall <app-id>`|Удалить приложение|

---

## Устранение неполадок

### Приложения не видны в меню KDE

Убедись что установлен плагин интеграции:

```bash
sudo apt install xdg-desktop-portal-kde -y
```

---

## Ссылки

- [Flathub](https://flathub.org/)
- [Flatpak документация](https://flatpak.org/)

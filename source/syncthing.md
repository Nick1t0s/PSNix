# Syncthing — Установка на Linux (Ubuntu/Debian/Mint)

> [Syncthing](https://syncthing.net/) — непрерывная синхронизация файлов между устройствами по принципу peer-to-peer. Установка из официального apt-репозитория (stable-v2).

---

## Шаг 1 — Создаём папку для ключей и скачиваем PGP-ключ

```bash
sudo mkdir -p /etc/apt/keyrings
sudo curl -L -o /etc/apt/keyrings/syncthing-archive-keyring.gpg https://syncthing.net/release-key.gpg
```

---

## Шаг 2 — Добавляем стабильный канал обновлений в список источников APT

```bash
echo "deb [signed-by=/etc/apt/keyrings/syncthing-archive-keyring.gpg] https://apt.syncthing.net/ syncthing stable-v2" | sudo tee /etc/apt/sources.list.d/syncthing.list
```

---

## Шаг 3 — Обновляем список пакетов и устанавливаем Syncthing

```bash
sudo apt-get update
sudo apt-get install syncthing
```

---

## Шаг 4 — Запуск как пользовательский сервис

```bash
systemctl --user enable syncthing
systemctl --user start syncthing
```

---

## Проверка

Веб-интерфейс доступен по адресу `http://127.0.0.1:8384`, статус сервиса:

```bash
systemctl --user status syncthing
```

---

## Ссылки

- [Официальный сайт](https://syncthing.net/)
- [Документация по установке](https://docs.syncthing.net/intro/getting-started.html)

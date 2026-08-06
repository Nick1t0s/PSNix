# OpenSSH-сервер на хост

> SSH-сервер позволяет подключаться к машине удалённо (с ноутбука к ПК и наоборот). Это установка на хост-систему, а не внутрь виртуалки (для виртуалки см. VM.md).

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install openssh-server -y
```

---

## Шаг 2 — Включить и запустить

```bash
sudo systemctl enable --now ssh
```

---

## Шаг 3 — Проверка

```bash
systemctl status ssh --no-pager
ss -tlnp | grep :22
```

Ожидаемый вывод: сервис `active (running)`, порт `0.0.0.0:22` в списке.

---

## Шаг 4 — Настройка брандмауэра

Если включён UFW:

```bash
sudo ufw allow ssh
sudo ufw reload
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`sudo systemctl status ssh`|Статус сервиса|
|`sudo systemctl restart ssh`|Перезапуск после изменения конфига|
|`ssh nik@192.168.x.x`|Подключение с другой машины|
|`sudo ufw status`|Проверить правила брандмауэра|

---

## Устранение неполадок

### Подключение отклоняется

Проверь конфиг и перезапусти:

```bash
sudo sshd -t
sudo systemctl restart ssh
```

### Не загружаются ключи

Если используешь аутентификацию по ключам — скопируй публичный ключ:

```bash
ssh-copy-id nik@192.168.x.x
```

---

## Ссылки

- [OpenSSH](https://www.openssh.com/)

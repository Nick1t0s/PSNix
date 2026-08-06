# Samba / smbclient

> Samba — сервер для предоставления общих папок по протоколу SMB (для Windows/Linux-машин в локальной сети). `smbclient` — клиент для доступа к SMB-шарам из терминала.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install samba -y
```

Клиент (если нужен только доступ к чужим шарам):

```bash
sudo apt install smbclient -y
```

---

## Шаг 2 — Запуск сервиса

```bash
sudo systemctl enable --now smbd
sudo systemctl status smbd --no-pager
```

---

## Шаг 3 — Добавить пользователя

```bash
sudo smbpasswd -a nik
```

Пользователь должен существовать в системе (`/etc/passwd`).

---

## Шаг 4 — Проверка

```bash
testparm
smbclient -L localhost -U nik
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`sudo smbpasswd -a nik`|Добавить SMB-пароль пользователю|
|`smbclient //host/share -U nik`|Подключиться к шаре|
|`smbclient -L host`|Список шар на удалённой машине|
|`sudo nano /etc/samba/smb.conf`|Конфиг сервера|
|`sudo systemctl restart smbd`|Перезапуск после правки конфига|

---

## Устранение неполадок

### Шара не видна с Windows

Проверь брандмауэр и доступность:

```bash
sudo ufw allow samba
sudo ufw status
```

### Ошибка авторизации

Пароль SMB задаётся отдельно от системного — через `sudo smbpasswd -a nik`, а не через `passwd`.

---

## Ссылки

- [samba.org](https://www.samba.org/)

# Obsidian

> Приложение для заметок в формате Markdown с локальным хранением vault. На этой машине установлен в `/opt/Obsidian`.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Скачать .deb

Скачай пакет с [официальной страницы](https://obsidian.md/download) (раздел Linux → `.deb`):

```bash
wget https://github.com/obsidianmd/obsidian-releases/releases/latest/download/obsidian_amd64.deb
```

---

## Шаг 2 — Установка

```bash
sudo apt install ~/Downloads/obsidian_amd64.deb -y
```

Устанавливается в `/opt/Obsidian`. Проверка:

```bash
obsidian --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`obsidian`|Запустить из терминала|
|`sudo apt install obsidian`|Если пакет добавлен в репозиторий|

---

## Vault

На этой системе vault находится в `/home/nik/Obsidian/My Vault/`.

---

## Ссылки

- [obsidian.md](https://obsidian.md/)
- [Релизы Obsidian](https://github.com/obsidianmd/obsidian-releases/releases)

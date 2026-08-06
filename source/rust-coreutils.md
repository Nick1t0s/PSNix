# rust-coreutils (uutils coreutils)

> Переписанные на Rust стандартные утилиты Unix (ls, cp, mv, cat, find и т.д.) — альтернатива базовым coreutils.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install rust-coreutils -y
```

---

## Шаг 2 — Проверка

```bash
uutils --version
ls --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`ls --help`|Справка по утилите|
|`uutils coreutils --help`|Общая справка|

---

## Примечание

Пакет ставит бинарники uutils рядом со стандартными (`/usr/bin/ls` и т.д.), не заменяя системные coreutils. Чтобы использовать Rust-версию — вызывай через `uutils` префикс.

---

## Ссылки

- [Репозиторий uutils/coreutils](https://github.com/uutils/coreutils)

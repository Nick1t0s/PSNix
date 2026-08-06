# Python (несколько версий)

> На системе установлены версии Python 3.9–3.14 одновременно. Все ставятся через PPA `deadsnakes`, системная версия (3.14) идёт из репозитория Ubuntu.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Подключить PPA deadsnakes

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

---

## Шаг 2 — Установить нужные версии

Каждая версия ставится отдельным пакетом. Вместе с интерпретатором желательно ставить `-dev` (заголовки) и `-venv` (виртуальные окружения):

```bash
sudo apt install python3.9 python3.9-dev python3.9-venv -y
sudo apt install python3.10 python3.10-dev python3.10-venv -y
sudo apt install python3.11 python3.11-dev python3.11-venv -y
sudo apt install python3.12 python3.12-dev python3.12-venv -y
sudo apt install python3.13 python3.13-dev python3.13-venv -y
```

Версия 3.14 (текущая системная в Ubuntu 26.04) уже предустановлена.

---

## Шаг 3 — Проверка

```bash
python3.9 --version
python3.10 --version
python3.11 --version
python3.12 --version
python3.13 --version
python3.14 --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`python3.12 -m venv .venv`|Создать виртуальное окружение конкретной версии|
|`source .venv/bin/activate`|Активировать|
|`python3.12 -m pip install pkg`|Ставить пакеты в нужную версию (без конфликтов)|
|`python3 --version`|Системный Python (3.14)|

---

## Устранение неполадок

### `pip` не найден

В некоторых версиях из deadsnakes pip ставится отдельно:

```bash
sudo apt install python3.13-pip -y
```

или

```bash
python3.13 -m ensurepip --upgrade
```

### Смешивание версий с системным Python

Никогда не ставь пакеты в системный `python3` через `sudo pip` — используй виртуальные окружения, чтобы не сломать систему.

---

## Ссылки

- [python.org](https://www.python.org/)
- [PPA deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa)

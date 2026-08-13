# lazyssh

> TUI для управления SSH-подключениями: быстрая навигация и запуск сессий.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`
- `jq` (используется для получения последней версии)

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install -y curl jq

LATEST_TAG=$(curl -fsSL https://api.github.com/repos/Adembc/lazyssh/releases/latest | jq -r .tag_name)
curl -LJO "https://github.com/Adembc/lazyssh/releases/download/${LATEST_TAG}/lazyssh_$(uname)_$(uname -m).tar.gz"

tar -xzf lazyssh_*.tar.gz
sudo mv lazyssh /usr/local/bin/
```

---

## Шаг 2 — Проверка

```bash
lazyssh --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`lazyssh`|Запустить TUI|

---

## Ссылки

- [github.com/Adembc/lazyssh](https://github.com/Adembc/lazyssh)
# GitHub CLI (gh)

> Официальный инструмент командной строки для работы с GitHub: репозитории, PR, issues, релизы прямо из терминала.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Git (уже установлен)

---

## Шаг 1 — Установка

В Ubuntu 26.04 пакет есть в стандартном репозитории:

```bash
sudo apt install gh
```

---

## Шаг 2 — Проверка

```bash
gh --version
```

---

## Шаг 3 — Авторизация

```bash
gh auth login
```

Выбери GitHub.com → HTTPS → **Login with a web browser** и вставь код из терминала.

---

## Полезные команды

|Команда|Описание|
|---|---|
|`gh auth status`|Статус авторизации|
|`gh repo view owner/repo`|Просмотр репозитория|
|`gh pr create`|Создать pull request|
|`gh pr checkout`|Переключиться на PR|
|`gh issue list`|Список issues|
|`gh release create v1.0`|Создать релиз|

---

## Устранение неполадок

### gh не найден после установки

Если пакета нет в репозитории — используй официальный способ установки:

```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
&& sudo mkdir -p -m 755 /etc/apt/keyrings \
&& out=$(mktemp) && wget -nv -O$out https://cli.github.com/keyring/githubcli-archive-keyring.gpg \
&& cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update && sudo apt install gh -y
```

---

## Ссылки

- [Документация gh](https://cli.github.com/manual/)
- [Репозиторий](https://github.com/cli/cli)

# 03 — CLI-утилиты

> Терминальные инструменты: современный поиск и навигация, мультиплексор,
> JSON, скачивание видео, файловый менеджер и TUI-приложения.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Основной набор

```bash
sudo apt install ripgrep fd-find fzf bat eza tree ncdu duf tmux jq yt-dlp -y
```

- `ripgrep` (rg) — мгновенный рекурсивный поиск по содержимому
- `fd-find` (fd) — быстрый поиск файлов
- `fzf` — интерактивный фильтр для списков
- `bat` — просмотр файлов с подсветкой синтаксиса
- `eza` — современная замена `ls`
- `tree` — дерево директорий
- `ncdu` — анализ места на диске
- `duf` — обзор занятого места на всех дисках
- `tmux` — мультиплексор терминала (сессии, окна, панели)
- `jq` — парсинг и фильтрация JSON
- `yt-dlp` — загрузчик видео с YouTube и сотен сайтов

> Примечание: в Ubuntu бинарник fd называется `fdfind` (сделай алиас, если нужно).

Проверка:

```bash
rg --version && fd --version && fzf --version && bat --version
tmux -V && jq --version && yt-dlp --version
```

Свежий yt-dlp через pipx (бинарь из `~/.local/bin` приоритетнее apt-версии):

```bash
sudo apt install -y pipx
pipx ensurepath
pipx install yt-dlp
```

---

## Шаг 2 — Yazi (файловый менеджер, официальный репозиторий)

```bash
curl -fsSL https://yazi-rs.github.io/builds/yazi-keyring.gpg | sudo tee /usr/share/keyrings/yazi-keyring.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/yazi-keyring.gpg] https://yazi-rs.github.io/builds/ stable main' | sudo tee /etc/apt/sources.list.d/yazi.list >/dev/null
sudo apt update && sudo apt install yazi
```

Проверка: `yazi --version`.

---

## Шаг 3 — lazydocker (TUI для Docker)

```bash
curl -fsSL https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash
```

Требует установленный Docker (см. `09 Docker.md`). Проверка: `lazydocker --version`.

---

## Шаг 4 — lazyssh (TUI для SSH-подключений)

```bash
LATEST_TAG=$(curl -fsSL https://api.github.com/repos/Adembc/lazyssh/releases/latest | jq -r .tag_name)
curl -LJO "https://github.com/Adembc/lazyssh/releases/download/${LATEST_TAG}/lazyssh_$(uname)_$(uname -m).tar.gz"
tar -xzf lazyssh_*.tar.gz
sudo mv lazyssh /usr/local/bin/
```

Проверка: `lazyssh --version`.

---

## Шаг 5 — konsave (сохранение/восстановление конфигов, pipx)

```bash
sudo apt install pipx -y
pipx ensurepath
pipx install konsave
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`rg слово`|Поиск слова в текущей папке|
|`fd имя`|Найти файл по имени|
|`ls \| fzf`|Интерактивный фильтр|
|`tmux new -s имя` / `tmux attach -t имя`|Создать / подключиться к сессии|
|`cat file.json \| jq .`|Отформатировать JSON|
|`yt-dlp -x --audio-format mp3 "URL"`|Скачать только аудио в mp3|
|`yazi`|Файловый менеджер|
|`lazydocker` / `lazyssh`|TUI-приложения|

# CLI-утилиты

> Современные терминальные инструменты: быстрый поиск, фильтры и красивая навигация.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install ripgrep fd-find fzf bat eza tree ncdu duf -y
```

- `ripgrep` (rg) — мгновенный рекурсивный поиск по содержимому файлов
- `fd-find` (fd) — быстрый поиск файлов
- `fzf` — интерактивный фильтр для списков (история, файлы, пайпы)
- `bat` — просмотр файлов с подсветкой синтаксиса
- `eza` — современная замена `ls`
- `tree` — дерево директорий
- `ncdu` — анализ места на диске
- `duf` — обзор занятого места на всех дисках

---

## Шаг 2 — Проверка

```bash
rg --version
fd --version
fzf --version
bat --version
eza --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`rg слово`|Поиск слова в текущей папке|
|`fd имя`|Найти файл по имени|
|`ls \| fzf`|Фильтровать вывод интерактивно|
|`bat файл`|Просмотр с подсветкой синтаксиса|
|`eza -la`|Детальный список файлов|
|`tree -L 2`|Дерево глубиной 2 уровня|
|`ncdu`|Интерактивный анализ диска|
|`duf`|Сводка по дискам|

---

## Ссылки

- [github.com/BurntSushi/ripgrep](https://github.com/BurntSushi/ripgrep)
- [github.com/sharkdp/fd](https://github.com/sharkdp/fd)
- [github.com/junegunn/fzf](https://github.com/junegunn/fzf)
- [github.com/sharkdp/bat](https://github.com/sharkdp/bat)

# JetBrains Toolbox

> Утилита для установки и обновления всех IDE JetBrains (PyCharm, WebStorm, IntelliJ IDEA и т.д.) с одного места. Ставится в скрытую директорию пользователя `~/.local/share/JetBrains/Toolbox`.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Интернет-соединение

> ⚠️ **Не используйте `sudo`** — Toolbox предназначен для установки в домашнюю директорию конкретного пользователя. Если поставить его с правами суперпользователя или закинуть в `/opt`, в будущем будут проблемы с правами доступа при скачивании через него самих IDE.

---

## Шаг 1 — Скачать архив

Прямая ссылка на серверы JetBrains всегда отдаёт самую свежую версию Toolbox App:

```bash
wget https://download.jetbrains.com/toolbox/jetbrains-toolbox-<ВЕРСИЯ>.tar.gz
```

Чтобы не вписывать версию вручную, её можно получить из API JetBrains:

```bash
wget "https://download.jetbrains.com/toolbox/jetbrains-toolbox-$(curl -fsSL 'https://data.services.jetbrains.com/products/releases?code=TBA&latest=true&type=release' | grep -o '"build":"[^"]*"' | head -n1 | cut -d'"' -f4).tar.gz"
```

---

## Шаг 2 — Распаковать архив

```bash
tar -xzf jetbrains-toolbox-*.tar.gz
```

---

## Шаг 3 — Распаковать в постоянную директорию

Тихая установка на Linux невозможна: Toolbox — это просто архив. Распакуйте его в постоянную директорию (например, в свою же папку данных), а не в `/tmp`, иначе после перезагрузки ярлык сломается:

```bash
mkdir -p ~/.local/share/JetBrains/Toolbox
rm -rf ~/.local/share/JetBrains/Toolbox/jetbrains-toolbox-*
tar -xzf jetbrains-toolbox-*.tar.gz -C ~/.local/share/JetBrains/Toolbox
```

---

## Шаг 4 — Запустить

Бинарник лежит в подпапке `bin`:

```bash
~/.local/share/JetBrains/Toolbox/jetbrains-toolbox-*/bin/jetbrains-toolbox
```

При первом запуске приложение инициализирует данные в `~/.local/share/JetBrains/Toolbox` и предложит принять пользовательское соглашение. Ярлык в меню приложений появится после принятия соглашения.

После запуска временный архив можно удалить:

```bash
rm -f ~/jetbrains-toolbox-*.tar.gz
```

---

## Запуск

Toolbox появится в меню приложений Ubuntu. Запуск из терминала (с версией из подпапки):

```bash
~/.local/share/JetBrains/Toolbox/jetbrains-toolbox-*/bin/jetbrains-toolbox
```

---

## Ссылки

- [Скачать JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/download/)
- [Помощь по установке Toolbox (JetBrains)](https://toolbox-support.jetbrains.com/)

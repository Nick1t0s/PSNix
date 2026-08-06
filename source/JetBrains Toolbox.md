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
wget "https://download.jetbrains.com/toolbox/jetbrains-toolbox-$(curl -fsSL 'https://data.services.jetbrains.com/products/releases?code=TBA&latest=true&type=release' | grep -o '"version":"[^"]*"' | head -n1 | cut -d'"' -f4).tar.gz"
```

---

## Шаг 2 — Распаковать архив

```bash
tar -xzf jetbrains-toolbox-*.tar.gz
```

---

## Шаг 3 — Запустить установщик

Перейти в распакованную папку (название начинается с `jetbrains-toolbox-`) и запустить установщик:

```bash
cd jetbrains-toolbox-*/
./jetbrains-toolbox
```

Запущенный файл автоматически скопирует Toolbox в `~/.local/share/JetBrains/Toolbox`, создаст ярлык в меню приложений, а затем сам закроется. После этого временные файлы можно смело удалить:

```bash
rm -rf ~/jetbrains-toolbox-*.tar.gz ~/jetbrains-toolbox-*/
```

---

## Запуск

Toolbox появится в меню приложений Ubuntu. Запуск из терминала:

```bash
~/.local/share/JetBrains/Toolbox/bin/jetbrains-toolbox
```

---

## Ссылки

- [Скачать JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/download/)
- [Помощь по установке Toolbox (JetBrains)](https://toolbox-support.jetbrains.com/)

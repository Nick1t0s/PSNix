# jq

> Утилита для работы с JSON из командной строки: парсинг, фильтрация и форматирование.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install jq -y
```

---

## Шаг 2 — Проверка

```bash
jq --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`cat file.json | jq .`|Отформатировать JSON|
|`cat file.json | jq '.name'`|Взять поле|
|`curl -s URL | jq '.[].id'`|Парсить API-ответ|
|`echo '{"a":1}' | jq '.a + 1'`|Арифметика в jq|

---

## Ссылки

- [jqlang.github.io/jq](https://jqlang.github.io/jq/)

# OpenCode

> CLI-инструмент для разработки с поддержкой ИИ-агентов прямо из терминала. Устанавливается через `apt`.

---

## Требования

- Ubuntu / Debian / Linux Mint
- `curl` (уже установлен)

---

## Шаг 1 — Установка

```bash
sudo apt install opencode
```

---

## Шаг 2 — Проверка

```bash
opencode --version
```

---

## Шаг 3 — Запуск

```bash
opencode
```

или с указанием модели:

```bash
opencode --model deepseek-v4-flash-free
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`opencode`|Запустить интерактивную сессию|
|`/help`|Справка внутри сессии|
|`opencode --version`|Версия|
|`opencode upgrade`|Обновление (для apt-версии не нужно, обновляется через `sudo apt upgrade`)|

---

## Устранение неполадок

### `opencode: command not found`

Обнови списки пакетов и установи пакет заново:

```bash
sudo apt update && sudo apt install opencode
```

---

---

# Firefox

> Браузер Mozilla Firefox.

## Установка

```bash
sudo apt install firefox
```

На Ubuntu Firefox ставится через snap (пакет apt является переходником и запустит snap-версию). На Debian / Linux Mint через apt ставится обычный deb-пакет.

## Запуск

```bash
firefox
```

---

## Ссылки

- [opencode.ai](https://opencode.ai/)
- [mozilla.org/firefox](https://www.mozilla.org/firefox/)

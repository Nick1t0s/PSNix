# Thunderbird

> Почтовый клиент и календарь от Mozilla. Устанавливается через Snap.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Snap (предустановлен в Ubuntu)

---

## Шаг 1 — Установка

```bash
sudo snap install thunderbird
```

---

## Шаг 2 — Проверка

```bash
snap list thunderbird
thunderbird --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`thunderbird`|Запустить из терминала|
|`sudo snap refresh thunderbird`|Обновление вручную|

---

## Устранение неполадок

### Не видит системные шрифты

Подключи шрифты к Snap:

```bash
snap connect thunderbird:fonts
```

---

## Ссылки

- [thunderbird.net](https://www.thunderbird.net/)
- [Thunderbird на Snapcraft](https://snapcraft.io/thunderbird)

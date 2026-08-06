# Okular

> Универсальный просмотрщик документов для KDE: PDF, DJVU, EPUB, MOBI, изображения и др.

---

## Требования

- Ubuntu / Debian / Linux Mint (KDE)
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install okular -y
```

---

## Шаг 2 — Проверка

```bash
okular --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`okular file.pdf`|Открыть документ из терминала|
|`sudo apt install okular-extra-backends`|Дополнительные форматы (уже установлены)|

---

## Устранение неполадок

### Не открывается DJVU/EPUB

Установи дополнительные бэкенды:

```bash
sudo apt install okular-extra-backends -y
```

---

## Ссылки

- [okular.kde.org](https://okular.kde.org/)

# Yazi — Установка на Linux (Ubuntu/Debian/Mint)

> Инструкция по установке терминального файлового менеджера [Yazi](https://github.com/sxyazi/yazi) из официального apt-репозитория.

---

## Шаг 1 — Добавляем GPG-ключ репозитория

```bash
curl -fsSL https://yazi-rs.github.io/builds/yazi-keyring.gpg | sudo tee /usr/share/keyrings/yazi-keyring.gpg >/dev/null
```

---

## Шаг 2 — Добавляем сам репозиторий в список источников

```bash
echo 'deb [signed-by=/usr/share/keyrings/yazi-keyring.gpg] https://yazi-rs.github.io/builds/ stable main' | sudo tee /etc/apt/sources.list.d/yazi.list >/dev/null
```

---

## Шаг 3 — Обновляем список пакетов и устанавливаем Yazi

```bash
sudo apt update && sudo apt install yazi
```

---

## Проверка

```bash
yazi --version
```

---

## Ссылки

- [Официальный сайт](https://yazi-rs.github.io/)
- [GitHub репозиторий](https://github.com/sxyazi/yazi)
- [Инструкция по установке](https://yazi-rs.github.io/docs/installation/)

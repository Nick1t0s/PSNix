# 11 — Steam

> Игровая платформа Valve. Требует 32-битные библиотеки (i386) и репозиторий multiverse.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Подготовка репозиториев

```bash
sudo dpkg --add-architecture i386
sudo add-apt-repository -y multiverse
sudo apt update
```

---

## Шаг 2 — Установка

```bash
sudo apt install steam -y
```

Пакет автоматически потянет 32-битные библиотеки, нужные для большинства игр.

---

## Шаг 3 — Проверка

Запусти Steam из меню или из терминала:

```bash
steam
```

При первом запуске пройдёт обновление клиента и вход в аккаунт.

---

## Настройка (опционально)

- **Steam Play (Proton) для Windows-игр**: Настройки → Совместимость →
  «Включить Steam Play для всех остальных продуктов» → выбрать Proton.
- **Слабый GPU**: в параметрах запуска игры добавить `-vulkan -nojoy`.

---

## Устранение неполадок

- **Ошибка 32-битных библиотек**:

  ```bash
  sudo dpkg --add-architecture i386
  sudo apt update
  sudo apt install libc6:i386 libgl1-mesa-glx:i386 -y
  ```

- **Нет звука в KDE** — проверь, что PipeWire работает: `systemctl --user status pipewire`.

---

## Ссылки

- [store.steampowered.com](https://store.steampowered.com/)

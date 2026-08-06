# Steam

> Игровой магазин и платформа Valve. Репозиторий Steam уже подключён в `/etc/apt/sources.list.d/` — осталось установить пакет.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Репозиторий Steam подключён (см. `/etc/apt/sources.list.d/steam.list`)
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install steam -y
```

Пакет `steam` автоматически потянет поддержку 32-битных библиотек, нужных для большинства игр.

---

## Шаг 2 — Проверка

Запусти Steam из меню приложений или из терминала:

```bash
steam
```

При первом запуске пройдёт обновление клиента и вход в аккаунт.

---

## Шаг 3 — Настройка (опционально)

### Включить Steam Play (Proton) для Windows-игр

В Steam: **Настройки → Совместимость → Включить Steam Play для всех остальных продуктов** → выбрать Proton.

### Отключить анимации/прозрачность (слабым GPU)

В параметрах запуска ярлыка игры добавить:

```
-vulkan -nojoy
```

---

## Устранение неполадок

### Steam не запускается (нет звука в KDE)

Установи `pulseaudio-utils` или проверь, что PipeWire работает:

```bash
systemctl --user status pipewire
```

### Ошибка отсутствия 32-битных библиотек

```bash
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install libc6:i386 libgl1-mesa-glx:i386 -y
```

---

## Ссылки

- [Официальный сайт Steam](https://store.steampowered.com/)
- [Репозиторий Valve](https://repo.steampowered.com/steam/)

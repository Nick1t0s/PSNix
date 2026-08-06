# Konsave

> CLI-утилита для сохранения и применения настроек Linux-кастомизации. Из коробки поддерживает KDE Plasma 6.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`
- Python 3

---

## Шаг 1 — Установка

```bash
sudo apt install -y pipx
pipx ensurepath
pipx install konsave
```

Установка через `pipx` изолирует konsave в собственном venv и не трогает системный Python. Вариант с `sudo python3 -m pip install --break-system-packages` на Ubuntu 24.04+ (PEP 668) работает, но опасен: pip может обновить системные пакеты, от которых зависит apt.

---

## Шаг 2 — Проверка

```bash
konsave --version
```

При первом запуске konsave сам создаёт `~/.config/konsave/conf.yaml` из шаблона KDE (авто-детект по `$XDG_CURRENT_DESKTOP`).

---

## Использование

|Команда|Описание|
|---|---|
|`konsave -s myprofile`|Сохранить текущие настройки в профиль|
|`konsave -s myprofile -f`|Сохранить с перезаписью существующего профиля|
|`konsave -a myprofile`|Применить профиль|
|`konsave -e myprofile -d DIR -n name -f`|Экспорт профиля в `DIR/name.knsv` (перезапись)|
|`konsave -i file.knsv`|Импорт профиля из архива|
|`konsave -l`|Список профилей|

Профили хранятся в `~/.config/konsave/profiles/`. После применения выйдите и войдите заново (или перезапустите `plasmashell`).

> **Живая сессия**: `konsave -a` только копирует файлы в `~/.config`. Plasma/KWin читают конфиги при старте и держат в памяти — обои/панель (`plasmashell`) и виртуальные столы (`kwinrc`) на живой сессии не применяются. Надёжно применять, когда Plasma не запущен: из TTY (Ctrl+Alt+F2, после выхода из сессии). `pc/kde-restore.sh` и `laptop/kde-restore.sh` при живой сессии откажутся с инструкцией; форсировать можно через `KDE_RESTORE_LIVE=1` (тогда они перезапустят `plasmashell`, но виртуальные столы всё равно требуют перезапуска KWin).

---

## Быстрый снимок настроек (PSNix)

Скрипты `pc/kde-export.sh` и `laptop/kde-export.sh` сохраняют снимок в `<имя>.knsv` в свою директорию:

```bash
./pc/kde-export.sh        # → pc/KDE.knsv
./pc/kde-export.sh MySet  # → pc/MySet.knsv
```

Обои (пути `Image=`/`PreviewImage=` из `plasma-org.kde.plasma.desktop-appletsrc` и `kscreenlockerrc`) копируются в `pc/wallpapers/` с манифестом `paths.txt`. Восстановление раскладывает их в `~/Pictures` и переписывает пути в конфигах — снимок самодостаточен, удаление исходника обоев ничего не ломает.

---

## Ссылки

- [github.com/Prayag2/konsave](https://github.com/Prayag2/konsave)
- [pypi.org/project/Konsave](https://pypi.org/project/Konsave/)

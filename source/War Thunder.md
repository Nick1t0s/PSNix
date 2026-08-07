# War Thunder (Linux-лаунчер)

> Специальный Linux-лаунчер от Gaijin (`wt_launcher_linux_*.tar.gz`). Не требует Steam — это самодостаточный набор бинарников: `launcher` (GUI на Sciter), `gaijin_selfupdater`, `bpreport` + `libsciter-gtk.so`, `libsteam_api.so` и иконка `launcher.ico`. Всё распаковывается в домашнюю директорию пользователя — `sudo` не нужно.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Архив `wt_launcher_linux_*.tar.gz` в корне репозитория (как в PSNix)
- Пакет `imagemagick` для извлечения иконки (ставится скриптами, но опционально)

---

## Шаг 1 — Распаковать архив

Архив содержит каталог `WarThunder/` верхнего уровня, поэтому распаковываем его так, чтобы итоговая структура была `~/wta/WarThunder/`:

```bash
mkdir -p ~/wta
tar -xzf wt_launcher_linux_*.tar.gz -C ~/wta
```

Результат:

```text
~/wta/WarThunder/
├── bpreport            # бинарник сбора отчётов о краше
├── gaijin_selfupdater  # самообновление лаунчера
├── launcher            # сам лаунчер (GUI)
├── launcher.ico        # иконка приложения
├── launcherr.dat
├── libsciter-gtk.so    # GUI-движок (Sciter)
├── libsteam_api.so
└── package.blk         # список исполняемых файлов
```

> ⚠️ **Не распаковывайте в `/tmp` и не удаляйте каталог после установки** — лаунчер (и его самообновление) живёт именно там. Распаковка в постоянную директорию `~/wta` уже учтена в скриптах установки.

---

## Шаг 2 — Ярлык в меню приложений

Лаунчер запускается по абсолютному пути с любым рабочим каталогом (все библиотеки лежат рядом). Поэтому достаточно создать `.desktop`-файл:

```bash
mkdir -p ~/.local/share/applications ~/.local/share/icons/hicolor/256x256/apps

# извлечь PNG-кадр 256x256 из launcher.ico
convert ~/wta/WarThunder/launcher.ico[5] ~/.local/share/icons/hicolor/256x256/apps/warthunder.png

cat > ~/.local/share/applications/warthunder.desktop <<EOF
[Desktop Entry]
Type=Application
Name=War Thunder
Comment=Лаунчер War Thunder
Exec=$HOME/wta/WarThunder/launcher
Icon=warthunder
Terminal=false
Categories=Game;
EOF
```

Проверить валидность файла:

```bash
desktop-file-validate ~/.local/share/applications/warthunder.desktop
```

---

## Запуск

Из меню приложений — **War Thunder**, или из терминала:

```bash
~/wta/WarThunder/launcher
```

При первом запуске лаунчер сам скачает игровые файлы. Иконка лаунчера: `~/wta/WarThunder/launcher.ico`.

---

## Установка через скрипты PSNix

Задача `task_warthunder` (есть и в `pc/pc.sh`, и в `laptop/laptop.sh`) делает всё автоматически:

1. Ищет `wt_launcher_linux_*.tar.gz` в корне репо, затем в `~/Downloads` и текущей папке;
2. Пересоздаёт `~/wta` и распаковывает архив туда;
3. Извлекает иконку и создаёт `warthunder.desktop`.

Если архив не найден, задача честно падает с сообщением — просто положите архив в корень репо и запустите снова.

---

## Устранение неполадок

### Лаунчер не запускается

```bash
~/wta/WarThunder/launcher
```

Убедитесь, что у `launcher` есть права на исполнение и все файлы на месте:

```bash
ls -la ~/wta/WarThunder/
ldd ~/wta/WarThunder/launcher | grep -i "not found"
```

---

## Ссылки

- [Официальный сайт War Thunder](https://warthunder.com/)

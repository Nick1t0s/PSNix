# 16 — Discord: TCP и UDP через NekoRay без глобального TUN

> Рабочая настройка для ПК и ноутбука. На ПК пользователь подтвердил нормальную
> работу 15.11.2026. На ноутбуке сохранены такие же файлы для восстановления;
> установка и голосовая связь на нём отдельно не проверялись.

## Рабочая схема

Discord установлен официальным **deb-пакетом**. Штатная точка входа — `/usr/bin/discord`.
В установленной версии она вызывает bootstrap/обновлятор и актуальный клиент
из `~/.config/discord/Discord` → `~/.config/discord/app-<версия>/Discord`.
Обёртка вызывает `/usr/bin/discord`, не привязывается к каталогу конкретной версии.
Профиль, авторизация и настройки остаются в `~/.config/discord`.

`~/.local/bin/discord-proxy` запускает клиент через **graftcp v0.8.3**:

- TCP и UDP перехватываются для запущенного процесса и поддерживаемых дочерних
  процессов через ptrace; SOCKS5 NekoRay — `127.0.0.1:2080`;
- `--enable-udp` включает UDP; `--select_proxy_mode only_socks5` не разрешает
  предусмотренный graftcp автоматический переход с SOCKS5 на прямой UDP;
- для Electron дополнительно указан `--proxy-server=socks5://127.0.0.1:2080`;
- `ALL_PROXY`, `HTTP_PROXY`, `HTTPS_PROXY` заданы как **`http://127.0.0.1:2080`**:
  это mixed-порт NekoRay, а встроенный обновлятор отклонял `socks5` в `ALL_PROXY`;
- `LD_PRELOAD`, `DANTE_UDP_ASSOCIATE_ZERO`, `SOCKS_CONF` удаляются из окружения
  этого запуска: библиотека Dante сюда не подключается.

Изменения окружения действуют только для Discord и его потомков. Системный прокси,
глобальный TUN и маршруты не настраиваются. NekoRay должен быть запущен с профилем,
который передаёт UDP. Поддержка ptrace должна быть разрешена для запускаемого
дочернего процесса; запуск от root для проверенной конфигурации не требовался.

## Почему не Dante

Для Telegram работает исправленная Dante, описанная в
[разделе 15](15%20Telegram%20—%20UDP%20через%20NekoRay.md).
При загрузке этой библиотеки в Discord sandbox GPU-процессов падал на
`getsockname` (`syscall 0x33`). Попытка программной отрисовки позволила открыть
окно, но интерфейс зависал. Контрольный запуск без Dante работал.

Рабочий вариант Discord использует graftcp без `LD_PRELOAD` и без добавленных
графических флагов. Не переносить в него `--gpu-launcher`, `--disable-gpu`,
`--disable-software-rasterizer`, `--in-process-gpu` или `--disable-features=Vulkan`
из диагностических запусков. Sandbox Electron не отключался.
Исходники и бинарник graftcp локально не правились; патчи Dante относятся
только к Telegram. Полный перехват всех возможных сетевых API/IPv6 не подтверждён.

## Файлы в PSNix

В обоих каталогах `pc/configs/discord/` и `laptop/configs/discord/`:

- `discord-proxy.sh` → `~/.local/bin/discord-proxy`;
- `discord.desktop` → `~/.local/share/applications/discord.desktop`.

В `shared/graftcp-v0.8.3/` сохранены официальный бинарный архив linux-amd64,
исходники тега v0.8.3, исходные суммы релиза `UPSTREAM-SHA256SUMS`, лицензия,
upstream README, происхождение бинарника `PROVENANCE.txt` и наш `SHA256SUMS`.
Архив содержит тот же исполняемый файл, который работает на ПК.
Готовая сборка рассчитана на x86_64 и требует glibc не старее 2.34;
на другой архитектуре/системе нужно собрать исходники или взять соответствующий
официальный релиз. Контрольная сумма скачанного архива сверена с upstream.

## Восстановление для ПК или ноутбука

Сначала установить официальный deb Discord. Если одновременно есть Discord
из Snap/Flatpak, использовать для этой схемы deb и не запускать вторую копию.
Полностью выйти из Discord, включая трей, до замены graftcp или обёртки.
Команды выполнять из корня PSNix обычным пользователем `nik`:

```bash
HOST=pc                          # для ноутбука: HOST=laptop
REPO_ROOT="$PWD"
sha256sum --check shared/graftcp-v0.8.3/SHA256SUMS

GRAFTCP_ROOT="$HOME/.local/opt/graftcp-v0.8.3"
mkdir -p "$GRAFTCP_ROOT" "$HOME/.local/bin"
tar -xzf shared/graftcp-v0.8.3/graftcp_v0.8.3_linux-amd64.tar.gz -C "$GRAFTCP_ROOT"
ln -sfn "$GRAFTCP_ROOT/usr/bin/graftcp" "$HOME/.local/bin/graftcp"
"$HOME/.local/bin/graftcp" --version

install -Dm755 "$HOST/configs/discord/discord-proxy.sh" "$HOME/.local/bin/discord-proxy"
install -Dm644 "$HOST/configs/discord/discord.desktop" \
  "$HOME/.local/share/applications/discord.desktop"
desktop-file-validate "$HOME/.local/share/applications/discord.desktop"
update-desktop-database "$HOME/.local/share/applications"
```

Для `desktop-file-validate` нужен пакет `desktop-file-utils`.
В desktop-файле сохранён абсолютный путь `/home/nik/.local/bin/discord-proxy`;
для другого пользователя заменить его перед установкой.
Системный `/usr/share/applications/discord.desktop` не править: локальный файл
с тем же ID перекрывает его, а обновление deb-пакета не перезаписывает локальную копию.
Обновлятор Discord, клиент и его исходники тоже не менялись.

### Кэш Wofi и ссылки

Меню настроено как `wofi --show drun`. В кэше Wofi мог остаться полный путь
к системному desktop-файлу, обходящий нашу обёртку. Заменить только эту запись:

```bash
if [ -f "$HOME/.cache/wofi-drun" ]; then
  sed -i "s| /usr/share/applications/discord.desktop$| $HOME/.local/share/applications/discord.desktop|" \
    "$HOME/.cache/wofi-drun"
fi
```

`Name=Discord`, `Icon=discord` и `StartupWMClass=discord` сохранены.
`Terminal=false`, `DBusActivatable=false`, а `Exec` вызывает обёртку с
`--url -- %u`; обработка `discord://` сохранена. На ПК отдельного Discord D-Bus
service не было. Проверить текущий обработчик:

```bash
xdg-mime query default x-scheme-handler/discord
```

Ожидается `discord.desktop`. Если обработчик ещё не назначен, выбрать его:
`xdg-mime default discord.desktop x-scheme-handler/discord`.
Автозапуск при входе в систему этим комплектом не включается. Если он уже
включён отдельно, его команда тоже должна вести в `discord-proxy`.

### Пересборка graftcp при необходимости

Нужны C toolchain, make и Go 1.25+ согласно `local/go.mod` (см. upstream README).
Go при сборке может скачивать зависимости/требуемую версию toolchain.

```bash
BUILD_ROOT=$(mktemp -d /tmp/discord-graftcp-build.XXXXXX)
tar -xzf "$REPO_ROOT/shared/graftcp-v0.8.3/graftcp-v0.8.3-source.tar.gz" -C "$BUILD_ROOT"
cd "$BUILD_ROOT/graftcp-0.8.3"
make
install -Dm755 local/graftcp "$GRAFTCP_ROOT/usr/bin/graftcp"
cd "$REPO_ROOT"
```

## Проверка, обновления и возврат

Открыть **Discord** из Wofi или выполнить `~/.local/bin/discord-proxy`.
Полностью выйти из старого экземпляра перед проверкой: уже запущенный клиент
может принять повторное открытие без перенаправления его существующих соединений.
Проверить отзывчивость интерфейса и голосовую связь; открывшееся окно само по себе
не доказывает ни то, ни другое. `pgrep -a -x graftcp` показывает трассировщик,
`pgrep -a -x Discord` — клиент и его дочерние процессы.

Работа в фоне/трее сохраняется: терминал для запуска из меню не требуется.
Обновления через apt и штатный bootstrap идут обычным путём; обёртка и graftcp
лежат отдельно. После будущих обновлений проверить запуск и звонок снова.
Профиль/авторизацию не удалять, клиент не переименовывать и не патчить.

При двух значках в трее полностью выйти из всех экземпляров. Если приложение
зависло, `pkill -u "$USER" -x Discord` завершает процессы Discord; после этого
проверить `pgrep -a -x graftcp` и завершить только оставшийся трассировщик Discord
по его PID. Не выполнять `pkill graftcp`: он может обслуживать другие приложения.
Во время настройки все Discord и связанные трассировщики были завершены по просьбе
пользователя; это разовая очистка, не часть запуска обёртки.

Для стандартного запуска полностью выйти из Discord, удалить только локальный
`~/.local/share/applications/discord.desktop`, обновить desktop database и убрать
соответствующую локальную запись из кэша Wofi. Системный ярлык deb-пакета останется.
Прямой запуск `/usr/bin/discord` из обычного окружения также обходит обёртку.

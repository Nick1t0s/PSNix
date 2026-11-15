# 15 — Telegram: UDP через NekoRay без глобального TUN

> Комплект для ПК и ноутбука. Настройка и звонок проверены на ПК 15.11.2026;
> на ноутбуке нужно установить комплект и отдельно проверить звонок.

## Что настроено

Telegram установлен официальным бинарником в `~/.local/share/Telegram/Telegram`,
рядом лежит штатный `Updater`. На ПК это не apt- и не Snap-пакет.
Профиль и авторизация остаются в `~/.local/share/TelegramDesktop`.
Для этой схемы на ноутбуке также нужна обычная установка вне Snap/Flatpak.
Официальный архив: <https://telegram.org/dl/desktop/linux>.
После распаковки один раз запустить обычный Telegram, затем полностью выйти:
он создаст стандартную иконку и файлы интеграции.

`telegram-udp` подключает исправленную библиотеку Dante через `LD_PRELOAD` только
к запускаемому Telegram. TCP остаётся обычным: встроенный SOCKS5 Telegram
настроен на `127.0.0.1:2080`. Внешний IPv4 UDP перехватывается Dante и направляется
в тот же SOCKS5 NekoRay. Локальные сети Dante по умолчанию исключает из прокси.
Полный перехват IPv6 и совместимость с другими программами не подтверждены.
Это запуск выбранного приложения, не системный прокси; TUN NekoRay выключен.
Маршруты, Docker и системные библиотеки не меняются.

В Wofi используется `wofi --show drun`. Существующий пункт **Telegram** сохранён:
та же иконка и desktop ID, но `Exec` и действие «Выйти» вызывают обёртку.
`DBusActivatable=false` заставляет меню использовать `Exec`; отдельный D-Bus service
также направлен в обёртку. Обработка ссылок `tg://` сохранена.
`Terminal=false` и `exec` в обёртке позволяют работать в фоне без терминала.
Сворачивание в трей остаётся настройкой самого Telegram; автозапуск при входе
в систему этим комплектом не включается.

`DESKTOPINTEGRATION=0` в окружении процесса предотвращает автоматическую перезапись
исправленных ярлыков. Встроенный обновлятор Telegram не отключён, бинарники
`Telegram` и `Updater` не патчились. Установка apt/Snap вместо этой копии — отдельная
миграция: текущая обёртка привязана к указанному пути, а не к пакетному менеджеру.

## Файлы в PSNix

Для обоих вариантов есть одинаковый каталог `$HOST/configs/telegram/`, где
`HOST=pc` или `HOST=laptop`:

- `telegram-udp.sh` → `~/.local/bin/telegram-udp`;
- `telegram-udp-compat.conf` → `~/.local/opt/dante-1.4.4/telegram-udp-compat.conf`;
- `applications/*.desktop` → `~/.local/share/applications/`;
- `dbus-services/*.service` → `~/.local/share/dbus-1/services/`.

Общая часть в `shared/telegram-dante-1.4.4/`:

- `libdsocks.so` — точная копия работающей исправленной библиотеки с ПК;
- `dante-1.4.4.tar.gz` — исходный архив upstream;
- `nekoray-udp-compat.patch` — обе правки с относительными путями;
- `BUILD-INFO.txt`, `LICENSE`, `SHA256SUMS` — сведения о сборке, лицензия и суммы.

Готовый ELF собран на **Linux x86_64, glibc 2.43** и использует `GLIBC_PRIVATE`.
На другом дистрибутиве/версии libc, особенно на ноутбуке, библиотеку следует
пересобрать. Исходники и патч общие для обеих машин; ELF не универсальный.

## Две правки исходников Dante

Обе включаются только при `DANTE_UDP_ASSOCIATE_ZERO=1`:

1. `lib/udp.c`: адрес в запросе SOCKS5 UDP ASSOCIATE заменяется на `0.0.0.0:0`.
   В установленном NekoRay ненулевой адрес ассоциации использовался как назначение
   вместо адреса сервера из UDP-пакета. Это воспроизведено сравнением STUN-запросов.
2. `lib/Rgetsockname.c`: для UDP возвращается сохранённый локальный адрес и порт,
   а не стандартная заглушка Dante `0.0.0.0:0`; это нужно для локальных ICE-кандидатов.

Сам Dante взят из официального исходного архива 1.4.4; это не перепаковка
библиотеки из Ubuntu-пакета `libdsocksd0t64`. Graftcp для Telegram пробовался
до Dante, но в рабочем запуске Telegram не используется. Для Discord выбран
именно graftcp: см. [раздел 16](16%20Discord%20—%20TCP%20и%20UDP%20через%20NekoRay.md).

## Восстановление

Все команды ниже выполнять из корня PSNix от обычного пользователя `nik`.
Перед заменой библиотеки полностью выйти из Telegram, включая трей.
При другом имени пользователя заменить `/home/nik/` в конфиге, desktop и service.

```bash
HOST=pc                          # для ноутбука: HOST=laptop
REPO_ROOT="$PWD"
DANTE_ROOT="$HOME/.local/opt/dante-1.4.4"
sha256sum --check shared/telegram-dante-1.4.4/SHA256SUMS
```

### Библиотека: пересборка на целевой системе

```bash
sudo apt install build-essential patch pkg-config desktop-file-utils
BUILD_ROOT=$(mktemp -d /tmp/telegram-dante-build.XXXXXX)
tar -xzf "$REPO_ROOT/shared/telegram-dante-1.4.4/dante-1.4.4.tar.gz" -C "$BUILD_ROOT"
cd "$BUILD_ROOT/dante-1.4.4"
patch -p1 < "$REPO_ROOT/shared/telegram-dante-1.4.4/nekoray-udp-compat.patch"
./configure --prefix="$DANTE_ROOT/compat" \
  --disable-server --disable-static --without-gssapi \
  --without-upnp --without-pam --without-libwrap
make -j4
make install
cd "$REPO_ROOT"
```

Вместо пересборки на том же окружении ПК можно восстановить сохранённый ELF:

```bash
install -Dm644 shared/telegram-dante-1.4.4/libdsocks.so \
  "$DANTE_ROOT/compat/lib/libdsocks.so"
```

### Обёртка, конфиг, меню и D-Bus

```bash
install -Dm755 "$HOST/configs/telegram/telegram-udp.sh" "$HOME/.local/bin/telegram-udp"
install -Dm644 "$HOST/configs/telegram/telegram-udp-compat.conf" \
  "$DANTE_ROOT/telegram-udp-compat.conf"
DESKTOP_ID=org.telegram.desktop._5774c16f34a95df4566f9914d94ceb35
install -Dm644 "$HOST/configs/telegram/applications/$DESKTOP_ID.desktop" \
  "$HOME/.local/share/applications/$DESKTOP_ID.desktop"
install -Dm644 "$HOST/configs/telegram/dbus-services/$DESKTOP_ID.service" \
  "$HOME/.local/share/dbus-1/services/$DESKTOP_ID.service"
desktop-file-validate "$HOME/.local/share/applications/$DESKTOP_ID.desktop"
update-desktop-database "$HOME/.local/share/applications"
dbus-send --session --type=method_call --dest=org.freedesktop.DBus \
  /org/freedesktop/DBus org.freedesktop.DBus.ReloadConfig
```

Этот desktop ID относится к установке `/home/nik/.local/share/Telegram/Telegram`
и обычному каталогу профиля. Если Telegram на другой машине создал другой ID,
адаптировать существующий ярлык и service по этим образцам; не оставлять два
видимых пункта Telegram и не менять каталог профиля ради совпадения ID.
Если используется автозапуск Telegram, его `Exec` тоже должен вызывать обёртку.

## Проверка и дальнейшее использование

1. Запустить NekoRay с рабочим профилем, mixed/SOCKS5 на `127.0.0.1:2080`;
   глобальный TUN не включать. Внутренний прокси Telegram оставить включённым.
2. Открыть Telegram из Wofi либо выполнить `~/.local/bin/telegram-udp`.
   Для запуска сразу в трее: `~/.local/bin/telegram-udp -startintray`.
3. Вызов `~/.local/bin/telegram-udp -quit` должен завершить существующий экземпляр.
   Повторное открытие из меню использует обычный механизм одного экземпляра Telegram.
4. Проверить звонок вручную. Успех DNS или отдельного STUN-запроса сам по себе
   не доказывает работу звонков. В тестах были отдельные тайм-ауты STUN.

```bash
pid=$(pgrep -u "$USER" -x Telegram | head -n1)
rg 'dante-1.4.4/compat/lib/libdsocks.so' "/proc/$pid/maps"
ps -o pid,ppid,sid,tty,stat -p "$pid"
tail -n 80 "$DANTE_ROOT/telegram-udp-compat.log"
```

У процесса должна быть загружена наша `libdsocks.so`; при запуске из меню/трея
терминал ему не нужен. Библиотека и обёртка находятся вне каталога `Telegram`,
поэтому штатная замена `Telegram`/`Updater` при обновлении их не затрагивает.
Звонок после будущего обновления проверять отдельно. Свежий клиент также может
потребовать обновить сохранённые desktop/service — их автогенерация отключена.
Не запускать параллельно вторую копию Telegram из apt/Snap/Flatpak.

Для возврата к стандартному запуску полностью выйти из Telegram и запустить
`~/.local/share/Telegram/Telegram` из окружения без `LD_PRELOAD`,
`DANTE_UDP_ASSOCIATE_ZERO` и `DESKTOPINTEGRATION`. Обычная установка Telegram
снова сгенерирует стандартные файлы интеграции. Удалять профиль/авторизацию не нужно.

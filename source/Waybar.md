# Waybar — статус-бар для Hyprland

> Конфиги лежат в `configs/waybar/` (единый конфиг для laptop и PC).
> Hyprland запускает waybar так (в hyprland.conf):
> `exec-once = waybar -c ~/.config/waybar/hyprland-config -s ~/.config/waybar/hyprland-style.css`

---

## Файлы

| Файл | Назначение |
|---|---|
| `hyprland-config` | JSON-конфиг модулей |
| `hyprland-style.css` | стиль |
| `scripts/cpu-temp.sh` | температура CPU Package (модуль `custom/cpu-temp`) |

## Модули

**Слева:** меню приложений (`wofi --show drun`), воркспейсы Hyprland.
**Центр:** температура CPU, память, загрузка CPU.
**Справа:** трей, звук (`wpctl`, `pavucontrol` по клику), раскладка
(`hyprland/language`), часы, сеть, выключение (`hyprctl dispatch exit`).

## Скрипты

- `scripts/cpu-temp.sh` — ищет `hwmon*` с именем `coretemp` и меткой
  «Package id 0», выводит температуру в °C. Вызывается раз в 5 секунд.

`keyboard.sh` и `kde-desktop.sh` — остатки KDE-конфига, для Hyprland
не используются (раскладку показывает встроенный модуль `hyprland/language`).

## Ссылки

- [Waybar Wiki](https://github.com/Alexays/Waybar/wiki)
- [Hyprland/language](https://wiki.hypr.land/0.41.2/Useful-Utilities/Status-Bars/#hyprlandlanguage)

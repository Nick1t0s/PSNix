# Инструменты сборки

> Компиляторы и утилиты для сборки программ из исходников: GCC, G++ и CMake.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install build-essential cmake -y
```

`build-essential` — метапакет: `gcc`, `g++`, `make`, `dpkg-dev` и заголовочные файлы. `cmake` — система сборки.

---

## Шаг 2 — Проверка

```bash
gcc --version
g++ --version
make --version
cmake --version
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`gcc файл.c -o программа`|Скомпилировать C-программу|
|`g++ файл.cpp -o программа`|Скомпилировать C++-программу|
|`make`|Собрать по Makefile|
|`cmake .. && make`|Сгенерировать и собрать|
|`make install`|Установить собранное (нужен sudo)|

---

## Ссылки

- [gcc.gnu.org](https://gcc.gnu.org/)
- [cmake.org](https://cmake.org/)

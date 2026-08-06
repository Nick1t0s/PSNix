# Node.js и npm

> Среда выполнения JavaScript (Node.js) и менеджер пакетов (npm) для разработки.

---

## Требования

- Ubuntu / Debian / Linux Mint
- `sudo`

---

## Шаг 1 — Установка

```bash
sudo apt update
sudo apt install nodejs npm -y
```

В Ubuntu 26.04 ставится Node.js 22 LTS.

---

## Шаг 2 — Проверка

```bash
node --version
npm --version
```

---

## Шаг 3 — Настройка (опционально)

### Обновить npm до свежей версии

```bash
sudo npm install -g npm@latest
```

### Установить nvm для управления версиями (альтернатива apt)

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
```

После этого `nvm install --lts` ставит последний LTS Node независимо от репозитория Ubuntu.

---

## Полезные команды

|Команда|Описание|
|---|---|
|`node -v`|Версия Node.js|
|`npm -v`|Версия npm|
|`npm init -y`|Создать package.json|
|`npm install`|Установить зависимости из package.json|
|`npm run dev`|Запустить dev-скрипт проекта|

---

## Устранение неполадок

### EACCES при глобальной установке

Не используй `sudo npm install -g` для глобальных пакетов — лучше переустановить Node через nvm, чтобы не сломать права в системе.

---

## Ссылки

- [nodejs.org](https://nodejs.org/)
- [Документация npm](https://docs.npmjs.com/)

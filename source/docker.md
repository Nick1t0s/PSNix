# Docker Engine

> Платформа для запуска контейнеров. На этой системе установлен полный комплект: Docker Engine, CLI, Compose-плагин, Buildx и rootless-режим — из официального репозитория Docker.

---

## Требования

- Ubuntu / Debian / Linux Mint
- Права `sudo`

---

## Шаг 1 — Очистка от старых версий

```bash
sudo apt remove docker docker-engine docker.io containerd runc -y 2>/dev/null
sudo apt install ca-certificates curl gnupg -y
```

---

## Шаг 2 — Добавить GPG-ключ и репозиторий

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
```

---

## Шаг 3 — Установка полного набора

```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras -y
```

Что это:

- `docker-ce` — сам движок
- `docker-ce-cli` — команда `docker`
- `containerd.io` — рантайм контейнеров
- `docker-buildx-plugin` — сборка образов (buildx)
- `docker-compose-plugin` — команда `docker compose`
- `docker-ce-rootless-extras` — запуск Docker без root

---

## Шаг 4 — Запуск и добавление в автозагрузку

```bash
sudo systemctl enable --now docker
```

---

## Шаг 5 — Доступ без sudo

```bash
sudo usermod -aG docker $USER
```

После этого нужен перезапуск сеанса (или перезагрузка).

---

## Шаг 6 — Проверка

```bash
docker --version
docker compose version
docker buildx version
sudo systemctl status docker --no-pager
```

Тестовый запуск:

```bash
docker run hello-world
```

---

## Полезные команды

|Команда|Описание|
|---|---|
|`docker ps -a`|Список контейнеров|
|`docker compose up -d`|Запустить compose-проект|
|`docker buildx build -t img .`|Собрать образ|
|`docker system prune -a`|Очистить всё неиспользуемое|

---

## Устранение неполадок

### Docker недоступен при поднятом Nekoray TUN

На ПК для этого есть скрипт `fix-docker-vpn` (см. fix-docker-vpn.md). На ноутбуке интерфейс другой — скрипт нужно адаптировать под `wlp0s20f3`.

### `Got permission denied` без sudo

Не перезашёл в систему после `usermod -aG docker`. Перезагрузись или выйди/зайди заново.

---

## Ссылки

- [Документация Docker](https://docs.docker.com/)
- [Установка Docker Engine](https://docs.docker.com/engine/install/ubuntu/)

ЭТО ПРОСТО СКРИПТ ДЛЯ ВИРТУАЛКИ И КОДИНГ АГЕНТОВ
```
# 1. Полное обновление системы до самого свежего состояния
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y

# 2. Установка Firefox, SSH (для удобного подключения с хоста) и базовых утилит
sudo apt install firefox openssh-server curl git -y
sudo systemctl enable --now ssh

# 3. Очистка от возможных старых версий Docker и установка зависимостей
sudo apt remove docker docker-engine docker.io containerd runc -y 2>/dev/null
sudo apt install ca-certificates curl gnupg -y

# 4. Добавление официального GPG-ключа Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 5. Добавление официального репозитория Docker (автоматически определит кодовое имя версии)
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 6. Установка свежего Docker Engine и Docker Compose (как плагина)
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# 7. Запуск Docker и добавление в автозагрузку
sudo systemctl enable --now docker

# 8. Добавление вашего пользователя в группу docker (чтобы не писать sudo перед каждой командой)
sudo usermod -aG docker $USER

# 9. Установка OpenCode (официальный скрипт)
curl -fsSL https://opencode.ai/install | bash

# 10. Перезагрузка для применения прав группы docker и обновлений
sudo reboot
```
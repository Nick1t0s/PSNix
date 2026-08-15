# VirtualBox

Установка **интерактивная**: во время `apt install virtualbox-ext-pack` нужно вручную принять лицензию Oracle PUEL, поэтому VirtualBox НЕ входит в списки задач (`query.json`).

Ставится одной командой из `laptop/interactive.txt` / `pc/interactive.txt`:

```bash
sudo apt update && sudo apt install -y virtualbox virtualbox-ext-pack linux-headers-generic && sudo usermod -aG vboxusers "$USER" && echo "VirtualBox установлен. Выйдите из системы и зайдите снова, чтобы применилась группа vboxusers."
```

После установки — выйти из системы и зайти заново (группа `vboxusers`).

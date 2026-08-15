#!/usr/bin/env bash
# Только для ПК
wget -O /tmp/deepcool-digital-linux https://github.com/Nortank12/deepcool-digital-linux/releases/latest/download/deepcool-digital-linux
chmod +x /tmp/deepcool-digital-linux
sudo cp /tmp/deepcool-digital-linux /usr/sbin/
echo 'SUBSYSTEM=="hidraw", ATTRS{idVendor}=="3633", MODE="0666"' | sudo tee /etc/udev/rules.d/99-deepcool-digital.rules > /dev/null
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo tee /etc/systemd/system/deepcool-digital.service > /dev/null <<'EOF'
[Unit]
Description=DeepCool Digital

[Service]
ExecStart=/usr/sbin/deepcool-digital-linux
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable deepcool-digital
sudo systemctl start deepcool-digital
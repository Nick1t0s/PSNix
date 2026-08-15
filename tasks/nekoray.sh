#!/usr/bin/env bash
sudo apt install -y libxcb-xinerama0
curl -fsSL --retry 5 --retry-all-errors -o /tmp/nekoray.deb https://github.com/MatsuriDayo/nekoray/releases/download/3.26/nekoray-3.26-2023-12-09-debian-x64.deb
sudo apt install -y /tmp/nekoray.deb
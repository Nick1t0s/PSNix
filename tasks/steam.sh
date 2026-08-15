#!/usr/bin/env bash
sudo dpkg --add-architecture i386
sudo add-apt-repository -y multiverse
sudo apt update
sudo apt install -y steam
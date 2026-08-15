#!/usr/bin/env bash
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y \
  python3.9 python3.9-dev python3.9-venv \
  python3.10 python3.10-dev python3.10-venv \
  python3.11 python3.11-dev python3.11-venv \
  python3.12 python3.12-dev python3.12-venv \
  python3.13 python3.13-dev python3.13-venv
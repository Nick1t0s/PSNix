#!/usr/bin/env bash
# Только для ноутбука
sudo snap install auto-cpufreq
sudo systemctl enable --now snap.auto-cpufreq.service.service
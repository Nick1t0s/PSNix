#!/usr/bin/env bash
ver=$(curl -fsSL https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest | sed -n 's/.*"tag_name": *"v\([^"]*\)".*/\1/p')
[ -n "$ver" ] || { echo "  Не удалось получить версию Obsidian" >&2; exit 1; }
curl -fsSL --retry 5 --retry-all-errors -o /tmp/obsidian.deb \
  "https://github.com/obsidianmd/obsidian-releases/releases/download/v${ver}/obsidian_${ver}_amd64.deb"
sudo apt install -y /tmp/obsidian.deb
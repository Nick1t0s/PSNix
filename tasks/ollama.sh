#!/usr/bin/env bash
echo "  Тихая установка, может занять несколько минут..."
for i in 1 2 3; do
  curl -fsSL https://ollama.com/install.sh | sh >/dev/null 2>&1 && exit 0
  sleep 3
done
exit 1
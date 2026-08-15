#!/usr/bin/env bash
sudo apt install -y jq
tag=$(curl -fsSL https://api.github.com/repos/Adembc/lazyssh/releases/latest | jq -r .tag_name)
[ -n "$tag" ] && [ "$tag" != "null" ] || { echo "  Не удалось получить версию lazyssh" >&2; exit 1; }
curl -fsSL --retry 5 --retry-all-errors -L -o /tmp/lazyssh.tar.gz \
  "https://github.com/Adembc/lazyssh/releases/download/${tag}/lazyssh_$(uname)_$(uname -m).tar.gz"
tar -xzf /tmp/lazyssh.tar.gz -C /tmp
sudo mv /tmp/lazyssh /usr/local/bin/
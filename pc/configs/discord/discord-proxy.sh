#!/bin/sh
exec env -u LD_PRELOAD -u DANTE_UDP_ASSOCIATE_ZERO -u SOCKS_CONF \
  ALL_PROXY="http://127.0.0.1:2080" \
  HTTP_PROXY="http://127.0.0.1:2080" \
  HTTPS_PROXY="http://127.0.0.1:2080" \
  "$HOME/.local/bin/graftcp" \
  --enable-udp --select_proxy_mode only_socks5 --socks5 127.0.0.1:2080 \
  /usr/bin/discord --proxy-server="socks5://127.0.0.1:2080" "$@"

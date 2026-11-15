#!/bin/sh
exec env -u SOCKS_SERVER -u SOCKS4_SERVER -u SOCKS5_SERVER \
  -u HTTP_CONNECT_PROXY -u UPNP_IGD \
  DESKTOPINTEGRATION=0 \
  DANTE_UDP_ASSOCIATE_ZERO=1 \
  SOCKS_CONF="$HOME/.local/opt/dante-1.4.4/telegram-udp-compat.conf" \
  LD_PRELOAD="$HOME/.local/opt/dante-1.4.4/compat/lib/libdsocks.so" \
  "$HOME/.local/share/Telegram/Telegram" "$@"

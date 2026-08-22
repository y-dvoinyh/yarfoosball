#!/bin/sh
set -eu

TPROXY_SECRET=$(tr -d '\r\n' < /run/secrets/tproxy_secret)
export TPROXY_SECRET

case "${TPROXY_SECRET:-}" in
  [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]) ;;
  *) echo "TPROXY_SECRET must contain exactly 32 lowercase hexadecimal characters" >&2; exit 2 ;;
esac

case "${TPROXY_CARRIER_MODE:-websocket}" in
  https|https-lanes|websocket|websocket-lanes) ;;
  *) echo "TPROXY_CARRIER_MODE is not supported" >&2; exit 2 ;;
esac

umask 077
printf '{"profiles":[{"name":"default","secret":"%s","backend":"127.0.0.1:2398","carrier_mode":"%s"}]}' \
  "$TPROXY_SECRET" "${TPROXY_CARRIER_MODE:-websocket}" > /run/tproxy/profiles.json
chown tproxy:tproxy /run/tproxy/profiles.json

if [ ! -s /var/lib/mtproxy/proxy-secret ]; then
  curl --fail --silent --show-error https://core.telegram.org/getProxySecret \
    --output /var/lib/mtproxy/proxy-secret
fi
if [ ! -s /var/lib/mtproxy/proxy-multi.conf ]; then
  curl --fail --silent --show-error https://core.telegram.org/getProxyConfig \
    --output /var/lib/mtproxy/proxy-multi.conf
fi

/usr/local/bin/mtproto-proxy \
  -u nobody -p 8888 -H 2398 -S "$TPROXY_SECRET" \
  --aes-pwd /var/lib/mtproxy/proxy-secret /var/lib/mtproxy/proxy-multi.conf \
  -M "${MTPROXY_WORKERS:-1}" -C "${MTPROXY_MAX_CONNECTIONS:-4096}" &
mtproxy_pid=$!

cleanup() {
  kill "$mtproxy_pid" 2>/dev/null || true
  wait "$mtproxy_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

setpriv --reuid=tproxy --regid=tproxy --init-groups \
  /usr/local/bin/tproxy-server -config /etc/tproxy/config.json &
relay_pid=$!

terminate() {
  kill "$relay_pid" "$mtproxy_pid" 2>/dev/null || true
}
trap terminate INT TERM

set +e
wait "$relay_pid"
relay_status=$?
set -e
cleanup
exit "$relay_status"

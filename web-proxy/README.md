# Telegram WEB proxy integration

This optional Compose overlay adds the official Telegram Desktop proof-of-concept
WEB relay without changing the normal site stack. The relay is the public HTTP
gateway and forwards every request that is not an authenticated bridge request to
the existing Nginx frontend/API routes.

## Start

Generate a separate 16-byte client secret:

```sh
openssl rand -hex 16
```

Set it as `TPROXY_SECRET`, then start the production stack with the overlay:

```sh
docker compose -f docker-compose.yml -f docker-compose.web-proxy.yml up -d --build
```

Use `kickerwave.ru` and that secret in a WEB-proxy-capable Telegram proof-of-concept
client. The prospective share link is:

```text
https://t.me/webproxy?server=kickerwave.ru&secret=<TPROXY_SECRET>
```

The public `t.me/webproxy` route and stock Telegram releases may not support this
proof-of-concept yet. The server protocol is pinned to upstream commit
`2873a08806d6e4d84830b9b5c4b0ec0f46af91f8`.

Do not expose ports 2398, 8080, 8081, 8082, or 8888 at the host/provider firewall.
Do not enable URI or request-header access logs: bridge capabilities and session
credentials are carried there.

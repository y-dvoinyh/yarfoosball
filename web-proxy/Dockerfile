FROM golang:1.25-bookworm AS relay-builder

ARG TPROXY_COMMIT=2873a08806d6e4d84830b9b5c4b0ec0f46af91f8
RUN git clone https://github.com/telegramdesktop/tproxy-server.git /src/tproxy-server \
    && cd /src/tproxy-server \
    && git checkout "$TPROXY_COMMIT" \
    && go test ./... \
    && CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /out/tproxy-server ./cmd/tproxy-server

FROM ubuntu:24.04 AS mtproxy-builder

ARG MTPROXY_COMMIT=f36d8af769ffaeac36978d38c2c0f6d1104c2137
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       ca-certificates git build-essential libssl-dev zlib1g-dev \
    && git clone https://github.com/TelegramMessenger/MTProxy.git /src/MTProxy \
    && cd /src/MTProxy \
    && git checkout "$MTPROXY_COMMIT" \
    && make -j"$(nproc)"

FROM debian:bookworm-slim

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       ca-certificates curl tini util-linux \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --no-create-home --shell /usr/sbin/nologin tproxy

COPY --from=relay-builder /out/tproxy-server /usr/local/bin/tproxy-server
COPY --from=mtproxy-builder /src/MTProxy/objs/bin/mtproto-proxy /usr/local/bin/mtproto-proxy
COPY config.json /etc/tproxy/config.json
COPY entrypoint.sh /usr/local/bin/web-proxy-entrypoint

RUN chmod 0755 /usr/local/bin/web-proxy-entrypoint \
    && mkdir -p /var/lib/mtproxy /run/tproxy \
    && chown tproxy:tproxy /run/tproxy

EXPOSE 8080 8081
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/web-proxy-entrypoint"]

FROM pandoc/core:2.10
LABEL VERSION="0.2.1"
LABEL MAINTAINER="Haseeb Majid<hello@haseebmajid.dev>"

COPY puppeteer.json ./
COPY dist ./dist/

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true
ENV CHROMIUM_PATH /usr/bin/chromium-browser

RUN apk update && \
    echo > /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/v3.12/main" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/v3.12/community" >> /etc/apk/repositories && \
    apk update && \
    apk add --no-cache \
    chromium \
    nss \
    harfbuzz \
    nodejs \
    npm \
    python3 \
    py3-pip && \
    pip3 install dist/* && \
    npm install @mermaid-js/mermaid-cli@8.9.1 && \
    mkdir input output && \
    ln -sf /data/node_modules/@mermaid-js/mermaid-cli/index.bundle.js /usr/local/bin/mmdc && \
    rm -r dist/ && \
    rm -rf /tmp/* /var/cache/apk/

ENTRYPOINT /bin/ash

# CMD [ "markdown_mermaid_to_images", "-f", "/data/input", "-o", "/data/output"]

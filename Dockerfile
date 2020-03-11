FROM pandoc/core:2.9.2

COPY package*.json puppeteer.json ./
COPY dist ./dist/

RUN apk update && apk upgrade && \
    echo > /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/v3.9/main" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/v3.9/community" >> /etc/apk/repositories && \
    apk update && \
    apk add --no-cache \
    chromium \
    nss\
    harfbuzz \
    nodejs \
    npm \
    python3 \
    py3-pip && \
    pip3 install dist/* && \
    npm install puppeteer@1.8.0 && \ 
    npm install --only=prod && \
    ln -sf /data/node_modules/mermaid.cli/index.bundle.js /usr/local/bin/mmdc && \
    rm -r dist/ && \
    rm -rf /tmp/* /var/cache/apk/

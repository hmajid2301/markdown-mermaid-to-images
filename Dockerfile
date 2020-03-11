FROM pandoc/core:2.9.2
LABEL MAINTAINER="Haseeb Majid <hello@haseebmajid.dev>"

COPY package*.json puppeteer.json ./
COPY dist ./dist/

RUN set -ex \
    && echo @edge http://nl.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories \
    && echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories \
    && apk update \
    && apk upgrade \
    && apk add --no-cache \
    chromium@edge \
    nss@edge \
    nodejs \
    npm \
    python3 \
    py3-pip && \
    pip3 install dist/* && \
    npm install --only=prod && \
    ln -sf /data/node_modules/mermaid.cli/index.bundle.js /usr/local/bin/mmdc && \
    rm -r dist/ && \
    rm -rf /tmp/* /var/cache/apk/*
# Arguments
ARG PLATFORM1C_VERSION="8.3.24.1819"
ARG USERNAME=<username>
ARG PASSWORD=<password>

# Base image
FROM ubuntu:bionic AS base

ARG PLATFORM1C_VERSION

#...

# Downloader
FROM python:alpine
RUN pip install --upgrade releases1c

ARG PLATFORM1C_VERSION
ARG USERNAME
ARG PASSWORD

ENV RELEASES1C_USERNAME=$USERNAME
ENV RELEASES1C_PASSWORD=$PASSWORD

RUN set -xe \
    && mkdir /distr \
    && python -m releases1c download Platform83 $PLATFORM1C_VERSION client.deb64.zip /distr/ \
    && python -m releases1c download Platform83 $PLATFORM1C_VERSION deb64.zip /distr/

# Base image
FROM base

COPY --from=downloader /distr/*.zip /opt/distr1c/

RUN set -xe \
    && mkdir /opt/1cdeb \
    && cd /opt/distr1c \
    && unzip '*.zip' -d /opt/1cdeb/ \
    && cd /opt/1cdeb \
    && dpkg -i \
        1c-enterprise-${PLATFORM1C_VERSION}-common_*.deb \
		1c-enterprise-${PLATFORM1C_VERSION}-server_*.deb \
		1c-enterprise-${PLATFORM1C_VERSION}-ws_*.deb \
		1c-enterprise-${PLATFORM1C_VERSION}-crs_*.deb \
		1c-enterprise-${PLATFORM1C_VERSION}-client_*.deb
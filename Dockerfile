FROM python:alpine
RUN pip install --upgrade releases1c

ARG PLATFORM1C_VERSION="8.3.24.1819"
ARG USERNAME=<username>
ARG PASSWORD=<password>

ENV RELEASES1C_USERNAME=$USERNAME
ENV RELEASES1C_PASSWORD=$PASSWORD

RUN set -xe \
    && mkdir /distr \
    && python -m releases1c download Platform83 $PLATFORM1C_VERSION client.deb64.zip /distr/ \
    && python -m releases1c download Platform83 $PLATFORM1C_VERSION deb64.zip /distr/

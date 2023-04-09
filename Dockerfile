# $ docker build --tag 'Docker イメージ名':latest --no-cache .
# $ docker run --name 'Docker コンテナ名' --volume 'ホストOS':/usr/local/src --interactive --tty --detach --rm 'Docker イメージ名':latest

FROM python:3.11.3

ENV youtube_token 'APIトークン'

COPY ./src /usr/local/src
WORKDIR /usr/local/src
VOLUME 'ホストOS' /usr/local/src

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

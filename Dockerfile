FROM python:3

WORKDIR /code

COPY ./telebot/requirements.txt .

RUN pip install -r requirements.txt

COPY . .
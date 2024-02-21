FROM python:3.10-alpine3.18
LABEL authors="deyakk"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tg-bot

COPY . .

RUN pip install -r requirements.txt

RUN rm -rf requirements.txt

CMD ["python", "main.py"]
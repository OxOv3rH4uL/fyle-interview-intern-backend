FROM python:3.8

RUN apt-get update 


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY run.sh .

RUN chmod +x run.sh

ENV FLASK_APP=core/server.py

RUN rm -f core/store.sqlite3

RUN flask db upgrade -d core/migrations/

EXPOSE 7755

ENTRYPOINT ["bash","run.sh"]


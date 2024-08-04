FROM python:3.10-slim

WORKDIR /app

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py

CMD [ "flask","run","--host=0.0.0.0" ]






FROM python:3.8

RUN mkdir /app
COPY *.py requirements.txt /app/
WORKDIR /app
VOLUME /out
RUN pip install --no-cache-dir -r requirements.txt
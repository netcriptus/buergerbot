FROM python:3.9

EXPOSE 5000
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y libssl-dev
RUN pip3 install -U pip
RUN pip3 install -r /app/requirements.txt
CMD uwsgi --ini /app/uwsgi.ini

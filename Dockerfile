FROM python:3.10

WORKDIR /app
COPY . .
RUN pip3 install -U pip
RUN pip3 install -r /app/requirements.txt
CMD sleep infinity

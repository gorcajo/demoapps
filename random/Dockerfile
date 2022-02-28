FROM python:3.8-slim-buster

RUN pip install --upgrade pip

RUN mkdir -p /root/app
WORKDIR /root/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

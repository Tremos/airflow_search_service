FROM python:3.10-alpine

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "9002"]
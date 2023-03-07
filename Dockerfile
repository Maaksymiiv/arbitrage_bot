FROM python:3.10
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -U pip && pip install -U -r requirements.txt
COPY . /app

COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]

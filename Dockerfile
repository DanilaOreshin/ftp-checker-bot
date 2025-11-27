FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY main.py .

CMD ["/opt/venv/bin/python", "main.py"]

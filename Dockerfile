FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY main.py .

RUN python3 -m venv /opt/venv

CMD ["/opt/venv/bin/python", "main.py"]

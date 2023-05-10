FROM python:3.10

WORKDIR /app

COPY ./v1/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./v1 /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090", "--reload"]

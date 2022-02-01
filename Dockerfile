FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install -e .

CMD ["uvicorn", "pantapalabras.api:app", "--host", "0.0.0.0", "--port", "9173"]

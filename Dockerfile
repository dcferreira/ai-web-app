FROM python:3.10 AS builder

RUN pip install --no-cache-dir --upgrade hatch
COPY . /code

WORKDIR /code
RUN hatch build -t wheel

FROM python:3.10

COPY --from=builder /code/dist /code/dist
RUN pip install --no-cache-dir --upgrade /code/dist/*

COPY app.py /code
COPY articles.sqlite /code

WORKDIR /code
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

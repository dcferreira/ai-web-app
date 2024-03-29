FROM python:3.10 AS builder

RUN pip install --no-cache-dir --upgrade hatch
COPY . /code

WORKDIR /code
RUN hatch build -t wheel

FROM python:3.10

WORKDIR /code

COPY --from=builder /code/dist /code/dist
RUN pip install --no-cache-dir --upgrade /code/dist/*
ENV SENTENCE_TRANSFORMERS_HOME=/stransformers
COPY articles.sqlite /code
RUN ls
RUN python -m ai_web_app.main

COPY app.py /code

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

FROM python:3.12-alpine3.17 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

FROM python:3.12-alpine3.17 AS runner

WORKDIR /app

COPY . .

COPY --from=builder /install /usr/local

RUN apk add --no-cache tesseract-ocr

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]

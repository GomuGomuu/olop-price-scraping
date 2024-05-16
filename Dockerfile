FROM python:3.12-alpine3.17
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV FLASK_APP=app
RUN apk add tesseract-ocr
CMD ["python","app.py"]

import logging
import os

from flask import Flask
from redis import Redis
from flask_caching import Cache

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

DEBUG = os.getenv("DEBUG", False)
SELENIUM_HOST = os.getenv("SELENIUM_HOST", "localhost")
SELENIUM_PORT = os.getenv("SELENIUM_PORT", 4444)
SELENIUM_HOST_URL = f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub"

CACHE_CARD_PRICE_KEY = "card_price"
BASE_REDIS_EXPIRATION = 60 * 60 * 24
OCR_PATH = os.getenv("OCR_PATH", "/usr/bin/tesseract")
config = {
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_DB,
    "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 24,
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app=app)
cache.init_app(app)
redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Configure Flask logging
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Importing the other views
from src.views import *  # noqa


def make_key(*args, **kwargs):
    user_data = request.get_json()  # noqa: F405
    return ",".join([f"{key}={value}" for key, value in user_data.items()])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    # obj = {
    #     "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Kouzuki+Oden+%28OP01-031-PAR%29&ed=OP-01&num=OP01-031-PAR",  # noqa
    #     "card_name": "Kouzuki Oden (OP01-031-PAR)"
    # }
    # price = get_price_workflow(obj["url"])

import os
from io import BytesIO

import requests
from PIL import Image
from selenium.webdriver.common.by import By

from app import DEBUG, app
from src.constants import (
    OLOP_X_PRICE_COORDINATES_OFFSET,
    OLOP_Y_PRICE_COORDINATES_OFFSET,
    OLOP_PRICE_BOX_WIDTH,
    OLOP_PRICE_BOX_HEIGHT,
)
from src.services.ocr import TesseractService


class ALOPCardScraper:
    def __init__(self, url, card_name, driver=None, card_price=None):
        self.driver = driver
        self.url = url
        self.price_image = None
        self.card_name = card_name
        self.card_price = card_price
        self.extract_string = None
        self.crop_coordinates = None

    def crop_image(self, image, coordinates, save=True):
        x, y, width, height = coordinates
        image = image.crop((x, y, x + width, y + height))
        if save:
            with open(f"./static/{self.card_name}_price_crop.png", "wb") as f:
                image.save(f)
        return image

    def get_price_image(
        self,
        url: str = None,
    ):
        url = self.url if not url else url
        self.driver.get(url)
        screenshot_stream = self.driver.get_screenshot_as_png()
        marketplace_stores_id = self.driver.find_element(By.ID, "marketplace-stores")
        marketplace_stores_first_child = marketplace_stores_id.find_element(
            By.TAG_NAME, "div"
        )
        first_child_location = marketplace_stores_first_child.location
        self.crop_coordinates = (
            first_child_location["x"] + OLOP_X_PRICE_COORDINATES_OFFSET,
            first_child_location["y"] + OLOP_Y_PRICE_COORDINATES_OFFSET,
            OLOP_PRICE_BOX_WIDTH,
            OLOP_PRICE_BOX_HEIGHT,
        )
        image = Image.open(BytesIO(screenshot_stream))
        self.price_image = self.crop_image(image, self.crop_coordinates, save=False)
        if DEBUG:
            os.makedirs("./static/extracted/", exist_ok=True)
            image.save(f"./static/extracted/{self.card_name}_screenshot.png")
            self.price_image.save(f"./static/extracted/{self.card_name}_price.png")
        return self.price_image

    def download_card_image(self, path=None, file_name="card_image.png"):
        if path:
            self.driver.get(path)
        image_div = self.driver.find_element(By.ID, "card-image-src")
        image_tag = image_div.find_element(By.TAG_NAME, "img")
        image_url = image_tag.get_attribute("src")
        image_ext = image_url.split(".")[-1]
        image = requests.get(image_url)
        with open(f"./static/{file_name}_card.{image_ext}", "wb") as f:
            f.write(image.content)
        return image

    def get_price_string_from_image(self, image: Image = None) -> str:
        image = self.price_image if not image else image
        orc = TesseractService()
        self.extract_string = orc.tesseract.image_to_string(image)
        self.card_price = list(filter(None, self.extract_string.split("\n")))[-1]
        app.logger.info(f"Extracted string: {self.extract_string}")
        return self.card_price

    def get_card_price_from_url(self):
        try:
            self.get_price_image(self.url)
            return self.get_price_string_from_image()
        except Exception as e:
            app.logger.error(f"Error: {e}")

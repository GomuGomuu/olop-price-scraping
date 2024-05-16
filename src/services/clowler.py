from io import BytesIO
from PIL import Image
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.constants import PRICE_COORDINATES, BROWSER_DIMENSIONS
from src.services.ocr import TesseractService


class ALOPCardCrowler:
    def __init__(
        self, driver=None, price_image=None, url=None, card_name=None, card_price=None
    ):
        self.driver = webdriver.Chrome()
        self.url = None
        self.price_image = None
        self.card_name = None
        self.card_price = None
        self.extract_string = None

    def get_price_image(
        self,
        url: str = None,
        crop_coordinates: str = PRICE_COORDINATES,
        browser_dimensions=BROWSER_DIMENSIONS,
    ):
        if url:
            self.driver.get(url)
        self.driver.set_window_size(browser_dimensions[0], browser_dimensions[1])
        screenshot_stream = self.driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot_stream))
        x, y, width, height = crop_coordinates
        self.price_image = image.crop((x, y, x + width, y + height))
        return self.price_image

    def download_card_image(self, path=None, file_name="card_image.png"):
        if path:
            self.driver.get(path)
        image_div = self.driver.find_element(By.ID, "card-image-src")
        image_tag = image_div.find_element(By.TAG_NAME, "img")
        image_url = image_tag.get_attribute("src")
        image_ext = image_url.split(".")[-1]
        image = requests.get(image_url)
        with open(f"cleaned_images/{file_name}_card.{image_ext}", "wb") as f:
            f.write(image.content)
        print(f"Image downloaded and saved as {file_name}_card.{image_ext}")
        return image

    def get_price_string_from_image(self, image) -> str:
        image = image if self.price_image is None else self.price_image
        orc = TesseractService()
        self.extract_string = orc.tesseract.image_to_string(image)
        self.card_price = list(filter(None, self.extract_string.split("\n")))[-1]
        return self.card_price

    def get_card_price_from_url(self, url):
        self.url = url
        self.get_price_image(url)
        return self.get_price_string_from_image(self.price_image)

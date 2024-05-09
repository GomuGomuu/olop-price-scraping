import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from constants import BROWSER_DIMENSIONS, PRICE_COORDINATES


def init_driver(url=None):
    driver = webdriver.Chrome()
    if url:
        driver.get(url)
        print(f"Driver initialized with URL: {url}")
    else:
        print("Driver initialized")

    return driver


def download_html(driver):
    html = driver.page_source

    print("HTML downloaded")
    return html


def get_screen_shot(driver, file_name="screenshot.png", browser_dimensions=BROWSER_DIMENSIONS):
    driver.set_window_size(browser_dimensions[0], browser_dimensions[1])
    driver.save_screenshot(f"web_page_images/{file_name}")

    print(f"Screenshot taken and saved as {file_name}")


def download_card_image(driver, file_name="card_image.png"):
    image_div = driver.find_element(By.ID, "card-image-src")
    image_tag = image_div.find_element(By.TAG_NAME, "img")
    image_url = image_tag.get_attribute("src")
    image_ext = image_url.split(".")[-1]
    image = requests.get(image_url)
    with open(f"cleaned_images/{file_name}_card.{image_ext}", "wb") as f:
        f.write(image.content)

    print(f"Image downloaded and saved as {file_name}_card.{image_ext}")


def crop_image(
        crop_coordinates=PRICE_COORDINATES,
        image_name="screenshot.png",
        cropped_name="cropped.png",
):
    from PIL import Image

    x, y, width, height = crop_coordinates

    image = Image.open(f"web_page_images/{image_name}")
    cropped_image = image.crop((x, y, x + width, y + height))
    cropped_image.save(f"cleaned_images/{cropped_name}")

    print(f"Image cropped and saved as {cropped_name}")
    return cropped_image

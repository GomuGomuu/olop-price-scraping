import os

from requests import RequestException

from app import app
from src.services.browser import ChromeBrowser
from src.services.scraper import ALOPCardScraper
from src.utils import validate_url


def get_price_workflow(url: str, card_name: str = None) -> float:
    safe_url = url if validate_url(url) else RequestException("Invalid URL")
    browser = ChromeBrowser(remote=True)
    try:
        browser.setup_driver()
        scraper = ALOPCardScraper(
            url=safe_url, card_name=card_name, driver=browser.driver
        )
        card_price = scraper.get_card_price_from_url()
    except Exception as e:
        os.makedirs("static/errors", exist_ok=True)
        os.rename(
            f"static/{card_name}_price.png", f"static/errors/{card_name}_price.png"
        )
        os.rename(
            f"static/{card_name}_screenshot.png",
            f"static/errors/{card_name}_screenshot.png",
        )
        app.logger.error(f"Error: {e}")
        raise e
    finally:
        browser.teardown_driver()

    return card_price

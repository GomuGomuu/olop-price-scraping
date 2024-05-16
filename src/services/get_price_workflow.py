from requests import RequestException

from src.services.clowler import ALOPCardCrowler
from src.utils import validate_url


def get_price_workflow(url: str) -> str:
    # verify if url is valid
    safe_url = url if validate_url(url) else RequestException("Invalid URL")

    # verify cache of url

    # if cached not expired, return cached value

    # if not cached, run crowler flow
    crowler = ALOPCardCrowler()
    card_price = crowler.get_card_price_from_url(safe_url)

    return card_price

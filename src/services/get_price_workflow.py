from requests import RequestException

from src.services.clowler import ALOPCardCrowler
from src.utils import validate_url


def get_price_workflow(url: str, card_name: str = None) -> float:
    safe_url = url if validate_url(url) else RequestException("Invalid URL")
    crowler = ALOPCardCrowler(url=safe_url, card_name=card_name)
    card_price = crowler.get_card_price_from_url()
    return card_price

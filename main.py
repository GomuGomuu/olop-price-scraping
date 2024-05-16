from constants import PRICE_COORDINATES
from scraper.services import (
    get_screen_shot,
    crop_image,
    init_driver,
)
from utils import str_to_slug

if __name__ == "__main__":

    list_of_cards = [
        {
            "name": "Trafalgar Law (ST02-009)",
            "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Trafalgar+Law%20(ST02-009)&ed=ST-02&num=ST02-009",
        },
        {
            "name": "Gecko Moria (086) (OP06-086)",
            "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Gecko+Moria+%28086%29+%28OP06-086%29&ed=OP-06&num=OP06-086",
        },
        {
            "name": "King (OP01-096)",
            "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=King+%28OP01-096%29&ed=OP-01&num=OP01-096",
        },
        {
            "name": "Donquixote Rosinante (030) (OP05-030)",
            "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Donquixote+Rosinante+%28030%29+%28OP05-030%29&ed=OP-05&num=OP05-030",
        },
        {
            "name": "Sabo (Sealed Battle 2023 Vol. 1) (OP04-083-SB)",
            "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Sabo+%28Sealed+Battle+2023+Vol.+1%29+%28OP04-083-SB%29&ed=PC-01&num=OP04-083-SB",
        },
        {
            "name": "Vinsmoke Reiju (042) (Alternate Art) (OP06-042-AA)",
            "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Vinsmoke+Reiju+%28042%29+%28Alternate+Art%29+%28OP06-042-AA%29&ed=OP-06&num=OP06-042-AA",
        },
    ]
    gk = [
        {
            "name": "Gecko Moria (086) (OP06-086)",
            "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Gecko+Moria+%28086%29+%28OP06-086%29&ed=OP-06&num=OP06-086",
        }
    ]

    for card in list_of_cards:
        driver = init_driver(card["url"])
        slug_name = str_to_slug(card["name"])
        get_screen_shot(driver, f"{slug_name}.png")
        crop_image(
            image_name=f"{slug_name}.png",
            cropped_name=f"{slug_name}_price.png",
            crop_coordinates=PRICE_COORDINATES,
        )
        # download_card_image(driver, f"{slug_name}.png")

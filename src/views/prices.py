import os

from flask import request, Response, json

from app import app, CACHE_CARD_PRICE_KEY
from src.services.price_workflow import get_price_workflow

from src.utils import slugify, extract_float_value


def make_key(*args, **kwargs):
    user_data = request.get_json()
    try:
        card_name = user_data.get("card_name")
        card_url = user_data.get("url")
        if not card_name or not card_url:
            app.logger.error(
                "The request payload is missing the card_name or url parameter"
            )
            raise Exception(
                "The request payload is missing the card_name or url parameter"
            )
        return f"{CACHE_CARD_PRICE_KEY}_{hash(slugify(f'{card_name}_{card_url}'))}"
    except Exception as e:
        return str(e)


def check_forced_update():
    return True if request.args.get("force") else False


@app.route("/get_price", methods=["POST"])
def get_price():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            if url := data.get("url"):
                card_name = data.get("card_name")

                if not card_name:
                    return Response(
                        "The request payload is missing the card_name parameter",
                        status=400,
                    )
                slug_name = slugify(card_name)

                try:
                    print(f"Request received for {card_name}")
                    price = extract_float_value(get_price_workflow(url, card_name))
                except Exception as e:
                    if e.args[0] == "NoneType' object has no attribute 'quit'":
                        # reboot the selenium docker container
                        app.logger.error(
                            "Selenium container is not running, restarting the container"
                        )
                        os.system("docker restart selenium")

                    app.logger.error(
                        f"Error while getting the price: {str(e)}, url: {url}, card_name: {card_name}"
                    )
                    return Response(
                        json.dumps(
                            {"error": "something went wrong, contact the administrator"}
                        ),
                        status=500,
                        content_type="application/json",
                    )

                payload = {
                    "price": price,
                    "card_name": card_name,
                    "card_slug": slug_name,
                }

                return Response(
                    json.dumps(payload), status=200, content_type="application/json"
                )
            return Response(
                "The request payload is missing the url parameter", status=400
            )
        else:
            return Response("The request payload is not a JSON", status=400)
    else:
        return Response("Method Not Allowed", status=405)

from flask import Flask, request, jsonify

from src.services.get_price_workflow import get_price_workflow
from src.utils import slugify, extract_float_value

app = Flask(__name__)


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/get_price", methods=["POST"])
def get_price():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            if url := data.get("url"):
                card_name = data.get("card_name")
                slug_name = slugify(card_name)
                price = extract_float_value(get_price_workflow(url))

                return {"price": price, "card_name": card_name, "card_slug": slug_name}

            return jsonify(
                {"error": "The request payload is missing the url parameter"}
            )
        else:
            return jsonify({"error": "The request payload is not in JSON format"})
    else:
        return jsonify({"error": "The request method is not POST"})


if __name__ == "__main__":
    app.run()
    # obj = {
    #     "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Kouzuki+Oden+%28OP01-031-PAR%29&ed=OP-01&num=OP01-031-PAR",
    #     "card_name": "Kouzuki Oden (OP01-031-PAR)"
    # }
    # price = get_price_workflow(obj["url"])

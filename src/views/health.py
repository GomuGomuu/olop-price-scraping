from flask import Response

from app import app


@app.route("/", methods=["GET"])
def health_check():
    return Response("OK", status=200)

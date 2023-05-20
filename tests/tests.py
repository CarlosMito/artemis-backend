import pandas as pd
import requests
import json
import ast

from flask import Flask
from flask_restful import Resource, Api, reqparse


URL = "https://api.replicate.com/v1/predictions"
TOKEN = "f3c32325c34d1e3701e0165378a9cab7a25c4503"


def make_post_prediction():
    body = {
        "version": "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
        "input": {
            "prompt": "cyborgue trending on artstation"
        }
    }

    headers = {
        "Authorization": f"Token {TOKEN}"
    }

    response = requests.post(URL, data=json.dumps(body), headers=headers)
    print(response.status_code)
    print(response.json())


def get_status(id):
    headers = {
        "Authorization": f"Token {TOKEN}"
    }

    response = requests.get(f"{URL}/{id}", headers=headers)

    return response.json()


class Prediction(Resource):

    def post():
        parser = reqparse.RequestParser()

        parser.add_argument("version", required=True)
        parser.add_argument("input", required=True)
        args = parser.parse_args()

        print(args["version"])
        print(args["input"])


if __name__ == "__main__":
    make_post_prediction()

    # app = Flask("Artemis")
    # api = Api(app)

    # api.add_resource(Prediction, '/v1/predictions')
    # # api.add_resource(Locations, '/locations')

    # # print(get_status("nbk362dcgffpzmj2sdmkuf2gwi"))

    # app.run()

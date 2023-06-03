
import requests
import json
from api.models import Input
from artemis.settings import REPLICATE_API_TOKEN


class ReplicateAPI:

    class Enpoints:
        TEXT2IMAGE = "v1/predictions"

    BASE_URL = "https://api.replicate.com"
    ENPOINTS = Enpoints

    @staticmethod
    def text2image(instance: Input):

        url = f"{ReplicateAPI.BASE_URL}/{ReplicateAPI.ENPOINTS.TEXT2IMAGE}"
        print(url)

        print(instance)
        print(type(instance))

        # body = {
        #     "version": "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
        #     "input": {
        #         "prompt": "cyborgue trending on artstation"
        #     }
        # }

        # headers = {
        #     "Authorization": f"Token {REPLICATE_API_TOKEN}"
        # }

        # response = requests.post(URL, data=json.dumps(body), headers=headers)
        # print(f"STATUS CODE: {response.status_code}")
        # print(F"RESPONSE:\n{response.json()}")

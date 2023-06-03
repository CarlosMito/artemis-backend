
import requests
import json
from rest_framework.response import Response
from api.models import Input
from artemis.settings import REPLICATE_API_TOKEN
import logging as log
from typing import List


class ReplicateAPI:

    class Enpoints:
        TEXT2IMAGE = "v1/predictions"

    BASE_URL = "https://api.replicate.com"
    ENPOINTS = Enpoints

    @staticmethod
    def status(id_list: List[str]):

        url = f"{ReplicateAPI.BASE_URL}/{ReplicateAPI.ENPOINTS.TEXT2IMAGE}"

        log.debug(url)

        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}"
        }

        return requests.get(f"{url}/{id_list[0]}", headers=headers)

        # responses = {}

        # for id in id_list:
        #     responses[id] = requests.get(f"{url}/{id}", headers=headers).json()

        # return responses

    @staticmethod
    def text2image(instance: Input) -> Response:

        url = f"{ReplicateAPI.BASE_URL}/{ReplicateAPI.ENPOINTS.TEXT2IMAGE}"

        log.debug(repr(instance))
        log.debug(url)

        body = {
            "version": instance.version,
            "input": {
                "prompt": instance.prompt,
                "negative_prompt": instance.negative_prompt
            }
        }

        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}"
        }

        # response = requests.post(url, data=json.dumps(body), headers=headers)
        # log.debug(f"STATUS CODE: {response.status_code}")
        # log.debug(F"RESPONSE:\n{response.json()}")

        # return response

    @staticmethod
    def parse_get_response(rjson) -> dict:

        id = None
        outputs = None
        percentages = None

        if "id" in rjson:
            id = rjson["id"]

        if "output" in rjson:
            outputs = rjson["output"]

        if "logs" in rjson and rjson["logs"] is not None:
            logs = rjson["logs"]

            percentages = []

            for line in logs.split('\n'):
                if "%" in line:
                    index = line.find("%")
                    value = line[:index].strip()

                    if value.isdigit():
                        percentages.append(int(value))

        log.debug(f"ID: {id}")
        log.debug(f"Percentages: {percentages}")
        log.debug(f"Outputs: {outputs}")

        return {
            "id": id,
            "percentages": percentages,
            "outputs": outputs
        }

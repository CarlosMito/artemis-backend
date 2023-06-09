
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
    def status(replicate_id: str):

        url = f"{ReplicateAPI.BASE_URL}/{ReplicateAPI.ENPOINTS.TEXT2IMAGE}"
        log.debug(url)

        headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}

        response = requests.get(f"{url}/{replicate_id}", headers=headers)

        if response.status_code != 200:
            log.debug(response)
            return None

        return ReplicateAPI.parse_get_response(response.json())

    @staticmethod
    def text2image(instance: Input) -> dict:

        url = f"{ReplicateAPI.BASE_URL}/{ReplicateAPI.ENPOINTS.TEXT2IMAGE}"

        log.debug(repr(instance))
        log.debug(url)

        body = {
            "version": instance.version,
            "input": {
                "prompt": instance.prompt,
                "negative_prompt": instance.negative_prompt,
                "num_outputs": instance.num_outputs,
                "num_inference_steps": instance.num_inference_steps,
                "guidance_scale": instance.guidance_scale,
                "scheduler": instance.scheduler,
                "seed": instance.seed
            }
        }

        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}"
        }

        response = requests.post(url, data=json.dumps(body), headers=headers)
        log.debug(f"STATUS CODE: {response.status_code}")

        if response.status_code == 200 or response.status_code == 201:
            log.debug(F"RESPONSE:\n{response.json()}")
            return {"replicate_id": response.json()["id"]}

        log.debug(response.content)

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
                        percentage = int(value)

                        if percentage > percentages[-1]:
                            percentages[-1] = percentage

                # Means is a new output
                elif "input_shape" in line:
                    percentages.append(0)

        log.debug(f"ID: {id}")
        log.debug(f"Percentages: {percentages}")
        log.debug(f"Outputs: {outputs}")

        return {
            "id": id,
            "percentages": percentages,
            "outputs": outputs
        }

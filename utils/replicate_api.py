
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

        styles_prompt = {
            "anime": "anime visual, trending on pixiv, high resolution artwork, final artwork by artgerm",
            "digitalArt": "digital art, trending on artstation",
            "model3d": "3d model style",
            "oilPainting": "oil painting style",
            "photography": "photography style",
            "surrealism": "surrealism",
            "comic": "comic style",
            "impressionist": "impressionist style",
            "graffiti": "graffiti style",
            "popArt": "pop art style"
        }

        # styles_negative_prompt = {
        #     "anime": "",
        #     "digitalArt": "digital art, trending on artstation",
        #     "model3d": "3d model style",
        #     "oilPainting": "oil painting style",
        #     "photography": "photography style",
        #     "surrealism": "surrealism",
        #     "comic": "comic style",
        #     "impressionist": "impressionist style",
        #     "graffiti": "graffiti style",
        #     "popArt": "pop art style"
        # }

        style_prompt = "" if instance.style not in styles_prompt else styles_prompt[instance.style]
        # style_negative_prompt = "" if instance.style not in styles_negative_prompt else styles_negative_prompt[instance.style]
        default_negative_prompt = "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face, blurry, draft, grainy"

        log.debug(f"Style Prompt: {style_prompt}")
        log.debug(f"Style Negative Prompt: {default_negative_prompt}")

        body = {
            "version": instance.version,
            "input": {
                "prompt": f"{instance.prompt}, {style_prompt}".strip(','),
                "negative_prompt": f"{instance.negative_prompt}, {default_negative_prompt}".strip(','),
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

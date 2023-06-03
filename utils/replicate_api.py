
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
        
        log.debug(id_list)
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

# {'id': 'p3hy6h7pijbqzjrhk36342v62a', 'version': 'db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf', 'input': {'negative_prompt': '', 'prompt': 'A bedroom with nobody but a lot of furniture'}, 'logs': '', 'error': None, 'status': 'starting', 'created_at': '2023-06-03T18:43:46.842936768Z', 'urls': {'cancel': 'https://api.replicate.com/v1/predictions/p3hy6h7pijbqzjrhk36342v62a/cancel', 'get': 'https://api.replicate.com/v1/predictions/p3hy6h7pijbqzjrhk36342v62a'}}
# {'id': 'p3hy6h7pijbqzjrhk36342v62a', 'version': 'db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf', 'input': {'negative_prompt': '', 'prompt': 'A bedroom with nobody but a lot of furniture'}, 'logs': 'Using seed: 60488\ninput_shape: torch.Size([1, 77])\n  0%|          | 0/50 [00:00<?, ?it/s]\n  4%|▍         | 2/50 [00:00<00:02, 16.94it/s]\n 10%|█         | 5/50 [00:00<00:02, 19.42it/s]\n 16%|█▌        | 8/50 [00:00<00:02, 20.23it/s]\n 22%|██▏       | 11/50 [00:00<00:01, 20.63it/s]\n 28%|██▊       | 14/50 [00:00<00:01, 20.83it/s]\n 34%|███▍      | 17/50 [00:00<00:01, 20.97it/s]\n 40%|████      | 20/50 [00:00<00:01, 21.04it/s]\n 46%|████▌     | 23/50 [00:01<00:01, 21.12it/s]\n 52%|█████▏    | 26/50 [00:01<00:01, 21.18it/s]\n 58%|█████▊    | 29/50 [00:01<00:00, 21.21it/s]\n 64%|██████▍   | 32/50 [00:01<00:00, 21.22it/s]\n 70%|███████   | 35/50 [00:01<00:00, 21.21it/s]\n 76%|███████▌  | 38/50 [00:01<00:00, 21.22it/s]\n 82%|████████▏ | 41/50 [00:01<00:00, 21.17it/s]\n 88%|████████▊ | 44/50 [00:02<00:00, 21.16it/s]\n 94%|█████████▍| 47/50 [00:02<00:00, 21.18it/s]\n100%|██████████| 50/50 [00:02<00:00, 21.21it/s]\n100%|██████████| 50/50 [00:02<00:00, 20.98it/s]\n', 'output': ['https://replicate.delivery/pbxt/cremkveKFUhgPkJxPLsR5LKtx33GSvhrTEEBjXVmWFvlvTCRA/out-0.png'], 'error': None, 'status': 'succeeded', 'created_at': '2023-06-03T18:43:46.842936Z', 'started_at': '2023-06-03T18:43:46.857584Z', 'completed_at': '2023-06-03T18:43:50.351051Z', 'metrics': {'predict_time': 3.493467}, 'urls': {'cancel': 'https://api.replicate.com/v1/predictions/p3hy6h7pijbqzjrhk36342v62a/cancel', 'get': 'https://api.replicate.com/v1/predictions/p3hy6h7pijbqzjrhk36342v62a'}}
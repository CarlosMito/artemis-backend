import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Constants
URL = "https://api.replicate.com/v1/predictions"
ARTEMIS_URL = "http://127.0.0.1:8000/artemis/api"

# Examples
RESPONSE = "{'id': 'b3izkvloijh7lhpgn45yoa4xm4', 'version': 'db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf', 'input': {'prompt': 'cyborgue trending on artstation'}, 'logs': 'Using seed: 1530\ninput_shape: torch.Size([1, 77])\n  0%|          | 0/50 [00:00<?, ?it/s]\n  4%|▍         | 2/50 [00:00<00:02, 16.90it/s]\n  8%|▊         | 4/50 [00:00<00:02, 18.44it/s]\n 14%|█▍        | 7/50 [00:00<00:02, 19.98it/s]\n 20%|██        | 10/50 [00:00<00:01, 20.60it/s]\n 26%|██▌       | 13/50 [00:00<00:01, 20.91it/s]\n 32%|███▏      | 16/50 [00:00<00:01, 21.06it/s]\n 38%|███▊      | 19/50 [00:00<00:01, 21.18it/s]\n 44%|████▍     | 22/50 [00:01<00:01, 21.19it/s]\n 50%|█████     | 25/50 [00:01<00:01, 21.19it/s]\n 56%|█████▌    | 28/50 [00:01<00:01, 21.20it/s]\n 62%|██████▏   | 31/50 [00:01<00:00, 21.20it/s]\n 68%|██████▊   | 34/50 [00:01<00:00, 21.21it/s]\n 74%|███████▍  | 37/50 [00:01<00:00, 21.23it/s]\n 80%|████████  | 40/50 [00:01<00:00, 21.24it/s]\n 86%|████████▌ | 43/50 [00:02<00:00, 21.25it/s]\n 92%|█████████▏| 46/50 [00:02<00:00, 21.23it/s]\n 98%|█████████▊| 49/50 [00:02<00:00, 21.23it/s]\n100%|██████████| 50/50 [00:02<00:00, 20.99it/s]\n', 'output': ['https://replicate.delivery/pbxt/0buEUDSSwbLMOp7DmDKY9Yay8XPm5VwaUtfPxkaQXjU0he9QA/out-0.png'], 'error': None, 'status': 'succeeded', 'created_at': '2023-05-21T13:38:45.721615Z', 'started_at': '2023-05-21T13:38:45.743832Z', 'completed_at': '2023-05-21T13:38:49.196099Z', 'metrics': {'predict_time': 3.452267}, 'urls': {'cancel': 'https://api.replicate.com/v1/predictions/b3izkvloijh7lhpgn45yoa4xm4/cancel', 'get': 'https://api.replicate.com/v1/predictions/b3izkvloijh7lhpgn45yoa4xm4'}}"
OUTPUT = "https://replicate.delivery/pbxt/0buEUDSSwbLMOp7DmDKY9Yay8XPm5VwaUtfPxkaQXjU0he9QA/out-0.png"


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
    print(f"STATUS CODE: {response.status_code}")
    print(F"RESPONSE:\n{response.json()}")


def get_status(id):
    headers = {
        "Authorization": f"Token {TOKEN}"
    }

    response = requests.get(f"{URL}/{id}", headers=headers)

    return response.json()


def api_tests():
    # make_post_prediction()

    get_status("b3izkvloijh7lhpgn45yoa4xm4")


def image_download_test():
    extension = OUTPUT.split(".")[-1]
    response = requests.get(OUTPUT)

    filename = f"image.{extension}"

    with open(filename, "wb") as file:
        file.write(response.content)


def artemis_api_test():
    # headers = {
    #     "Authorization": f"Token {TOKEN}"
    # }

    # response = requests.get(f"{ARTEMIS_URL}/user", headers={})

    # print(response.json())

    # response = requests.post(f"{ARTEMIS_URL}/text2image", headers={}, data={})
    # response = requests.get(f"{ARTEMIS_URL}/text2image?id=1", headers={}, data={})

    # print(response.json())

    print(get_status("p3hy6h7pijbqzjrhk36342v62a"))


if __name__ == "__main__":
    artemis_api_test()
    # image_download_test()

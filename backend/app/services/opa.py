import requests

OPA_URL = "http://opa:8181/v1/data/fileupload/decision"

def evaluate_policy(input_data: dict) -> dict:
    response = requests.post(
        OPA_URL,
        json={"input": input_data},
        timeout=5
    )
    response.raise_for_status()
    return response.json()["result"]


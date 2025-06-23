import requests

class DeepseekClient:
    def __init__(self, api_key):
        self.endpoint = "https://api.deepseek.com/v1/generate"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def generate(self, prompt: str):
        resp = requests.post(self.endpoint, json={"prompt": prompt}, headers=self.headers)
        resp.raise_for_status()
        return resp.json()["choices"][0]["text"]

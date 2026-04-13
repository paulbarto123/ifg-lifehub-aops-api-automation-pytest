import requests
from configs.config import BASE_URL_CORE_UAT, API_KEY_CORE_UAT

class OrganizationPolicyClient:

    def __init__(self):
        self.url = f"{BASE_URL_CORE_UAT}/v2/pas/organization-policies/search"
        self.headers = {
            "apiKey": API_KEY_CORE_UAT,
            "Content-Type": "application/json"
        }

    def search_policy(self, payload: dict):
        response = requests.post(
            url=self.url,
            headers=self.headers,
            json=payload
        )
        return response
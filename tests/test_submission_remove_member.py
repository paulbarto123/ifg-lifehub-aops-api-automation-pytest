import requests

BASE_URL_CORE_UAT = "https://api-core-uat.ifg-life.id"
API_KEY_CORE_UAT = "AXBJVtacQkg9vOVjurl1qJXPwHIC9Nh3"

def test_search_organization_policy_success():
    url = f"{BASE_URL_CORE_UAT}/v2/pas/organization-policies/search"
    headers = {
        "apiKey": API_KEY_CORE_UAT,
        "Content-Type": "application/json"
    }
    payload = {
        "page": 0,
        "size": 1,
        "organizationPolicyNumber": "EBP/PHT-0000001160/AA (0000001160)"
    }
    response = requests.post(
        url=url,
        headers=headers,
        json=payload
    )
    body = response.json()
    assert response.status_code == 200
    print("Step 1 -- organization policy body: ", body)
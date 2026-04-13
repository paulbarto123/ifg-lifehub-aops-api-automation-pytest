from dotenv.main import logger

from clients.organization_policy_client import OrganizationPolicyClient

def test_search_organization_policy_success():
    client = OrganizationPolicyClient()

    payload = {
        "page": 0,
        "size": 1,
        "organizationPolicyNumber": "EBP/PHT-0000001160/AA (0000001160)"
    }

    response = client.search_policy(payload)
    # logger.info("Response body: %s", response.json())
    # print(response)
    body = response.json()
    print("Step 1 -- organization policy body: ", body)
    # HTTP Assertion
    assert response.status_code == 200
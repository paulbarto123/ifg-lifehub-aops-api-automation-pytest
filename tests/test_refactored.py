import requests
from typing import Dict, Any, Optional

# ======================
# CONFIGURATION
# ======================

ENVIRONMENTS = {
    "UAT": {
        "BASE_URL": "https://api-core-uat.ifg-life.id",
        "API_KEY": "AXBJVtacQkg9vOVjurl1qJXPwHIC9Nh3"
    },
    # Example for future use:
    # "SIT": {
    #     "BASE_URL": "https://api-core-sit.ifg-life.id",
    #     "API_KEY": "xxxxx"
    # }
}

REFUND_PRODUCT_CODES = {"103", "104", "108"}


# ======================
# COMMON HELPERS
# ======================

def get_headers(api_key: str) -> Dict[str, str]:
    return {
        "apiKey": api_key,
        "Content-Type": "application/json"
    }


def post_request(url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(url=url, headers=headers, json=payload)
    assert response.status_code == 200, f"API failed: {response.status_code}, {response.text}"
    return response.json()


# ======================
# API FUNCTIONS
# ======================

def search_organization_policy(
    base_url: str,
    api_key: str,
    organization_policy_number: str,
    page: int = 0,
    size: int = 1
) -> Optional[Dict[str, Any]]:

    url = f"{base_url}/v2/pas/organization-policies/search"
    payload = {
        "page": page,
        "size": size,
        "organizationPolicyNumber": organization_policy_number
    }

    body = post_request(url, get_headers(api_key), payload)
    data_list = body.get("data", {}).get("data", [])

    return data_list[0] if data_list else None


def search_policy_member(
    base_url: str,
    api_key: str,
    organization_policy_number: str,
    page: int = 0,
    size: int = 10
) -> Dict[str, Any]:

    url = f"{base_url}/v2/pas/policy/search"
    payload = {
        "page": page,
        "size": size,
        "organizationPolicyNumber": organization_policy_number
    }

    return post_request(url, get_headers(api_key), payload)


# ======================
# BUSINESS LOGIC
# ======================

def build_collection_vars(
    policy_data: Dict[str, Any],
    default_cash_value: str = "1000000"
) -> Dict[str, Any]:

    product_code = policy_data.get("productCode")
    is_refund = product_code in REFUND_PRODUCT_CODES

    return {
        "organizationId": policy_data.get("organizationId"),
        "organizationPolicyNumber": policy_data.get("organizationPolicyNumber"),
        "productCode": product_code,
        "isRefund": str(is_refund).upper(),
        "cashValue": "" if is_refund else default_cash_value
    }


# ======================
# TEST / SCENARIO
# ======================

def test_search_organization_policy_success(
    env_name: str,
    policy_number: str
):
    env = ENVIRONMENTS[env_name]

    # -------- STEP 1: Search organization policy
    policy_data = search_organization_policy(
        base_url=env["BASE_URL"],
        api_key=env["API_KEY"],
        organization_policy_number=policy_number
    )

    assert policy_data, "No organization policy data found"

    collection_vars = build_collection_vars(policy_data)

    print("STEP 1 - Collection Variables:")
    print(collection_vars)

    # -------- STEP 2: Search policy member
    policy_member_response = search_policy_member(
        base_url=env["BASE_URL"],
        api_key=env["API_KEY"],
        organization_policy_number=collection_vars["organizationPolicyNumber"]
    )

    print("\nSTEP 2 - Policy Member Response:")
    print(policy_member_response)

    return policy_member_response
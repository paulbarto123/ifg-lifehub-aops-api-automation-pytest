import requests
import random
from datetime import datetime
import uuid

BASE_URL_CORE_UAT = "https://api-core-uat.ifg-life.id"
API_KEY_CORE_UAT = "AXBJVtacQkg9vOVjurl1qJXPwHIC9Nh3"
BASE_URL_IFGID_UAT = "https://api-ifgid-uat.ifg-life.id"
API_KEY_IFGID_UAT = "vuUqf1Uu1IcxntBIEw1JA0lh0uUGM3B0"
BASE_URL_AOPS_UAT = "https://api-automation-v2-uat.ifg-life.id"
API_KEY_AOPS_UAT = "hU4PcqkykYz2uJRXPgtbWZNnQg80WX8J"

def test_search_organization_policy_success():

############## Step 1: Search for organization policy
    url_policy_search = f"{BASE_URL_CORE_UAT}/v2/pas/organization-policies/search"
    headers = {
        "apiKey": API_KEY_CORE_UAT,
        "Content-Type": "application/json"
    }
    payload_policy_search = {
        "page": 0,
        "size": 1,
        "organizationPolicyNumber": "EBP/PHT-0000001160/AA (0000001160)"
    }
    response_policy_search = requests.post(
        url=url_policy_search,
        headers=headers,
        json=payload_policy_search
    )
    body_policy_search = response_policy_search.json()
    assert response_policy_search.status_code == 200
    # print("Step 1 -- organization policy body: ", body_policy_search)

    # Example structure for collection variables
    collection_vars = {
        "cashValue": "1000000"  # Example value, replace with actual logic to set this variable
    }

    # Assume `response` is a requests.Response object
    # if response_policy_search.status_code == 200:
    #     # response_json = response_policy_search.json()

    if ( len(body_policy_search["data"]["data"]) > 0 ):
    # if body_policy_search.get("data", {}).get("data"):
        first_item = body_policy_search["data"]["data"][0]

        organization_id = first_item.get("organizationId")
        organization_policy_number = first_item.get("organizationPolicyNumber")
        product_code = first_item.get("productCode")

        refund_codes = ["103", "104", "108"]
        is_refund = product_code in refund_codes

        # Equivalent to pm.collectionVariables.set
        collection_vars["isRefund"] = str(is_refund).upper()
        collection_vars["cashValue"] = "" if is_refund else collection_vars.get("cashValue")
        collection_vars["productCode"] = product_code
        collection_vars["organizationId"] = organization_id
        collection_vars["organizationPolicyNumber"] = organization_policy_number
    
    # print("Collection Variables: ", collection_vars)
    # print("Step 2 -- isRefund: ", collection_vars.get("organizationId"))
    print("Step 1 - Organization Policy Number: ", collection_vars.get("organizationPolicyNumber"))


############## Step 2: Search for organization policy
    url_get_policy_member = f"{BASE_URL_CORE_UAT}/v2/pas/policy/search"
    headers = {
        "apiKey": API_KEY_CORE_UAT,
        "Content-Type": "application/json"
    }
    payload_get_policy_member = {
        # "page": 0,
        "size": 1000,
        "organizationPolicyNumber": collection_vars.get("organizationPolicyNumber")
    }
    response_get_policy_member = requests.post(
        url=url_get_policy_member,
        headers=headers,
        json=payload_get_policy_member
    )
    body_get_policy_member = response_get_policy_member.json()
    assert response_get_policy_member.status_code == 200
  

    # print("Step 2 -- get policy member body: ", body_get_policy_member)

    policy_list = body_get_policy_member.get("data", {}).get("policyList")

    if policy_list:
        # Filter policies with premi >= 0 and status INFORCE
        valid_policies = [
            policy
            for policy in policy_list
            if policy.get("premi", 0) >= 0 and policy.get("policyStatus") == "INFORCE"
        ]

        # print("Valid policies:", valid_policies)

        # Postman test equivalent
        assert len(valid_policies) > 0, (
            "There are policies with premi greater than 0 and status INFORCE"
        )

        # Pick random policy
        if valid_policies:
            random_policy = random.choice(valid_policies)

            collection_vars["randomPolicyNumber"] = random_policy.get("policyNumber")
            collection_vars["planCode"] = random_policy.get("planCode", "") or ""

            # print("Random Policy:", random_policy)
            print("Step 2 - Random Policy Number:", collection_vars.get("randomPolicyNumber"))

################ Step 3: Check Policy No
    url_check_policy_number = f"{BASE_URL_CORE_UAT}/v2/pas/policies/search"
    headers = {
        "apiKey": API_KEY_CORE_UAT,
        "Content-Type": "application/json"
    }
    payload_check_policy_number = {
        "policyNumber": collection_vars.get("randomPolicyNumber")
    }
    response_check_policy_number = requests.post(
        url=url_check_policy_number,
        headers=headers,
        json=payload_check_policy_number
    )
    body_check_policy_number = response_check_policy_number.json()
    assert response_check_policy_number.status_code == 200
    # print("Step 3 -- check policy number body: ", body_check_policy_number)

    # Assume response_json = response.json()
    policy_list = body_check_policy_number.get("data", {}).get("policyList")

    if policy_list and len(policy_list) > 0:
        first_policy = policy_list[0]

        member_id = first_policy.get("id")
        cif = first_policy.get("person", {}).get("cif")
        policy_status = first_policy.get("status")
        policy_number = first_policy.get("policyNumber")
        product_code = first_policy.get("productCode")

        # Retrieve CERTIFICATE_NUMBER from listPolicyVariable
        certificate_number = policy_number  # default fallback

        list_policy_variable = first_policy.get("listPolicyVariable", [])
        for variable in list_policy_variable:
            if variable.get("code") == "CERTIFICATE_NUMBER":
                certificate_number = variable.get("value")
                break

        collection_vars["certificateNumber"] = certificate_number
        collection_vars["memberId"] = member_id
        collection_vars["cif"] = cif
        collection_vars["policyNumber"] = policy_number
        collection_vars["policyStatus"] = policy_status
        # collection_vars["productCode"] = product_code  # intentionally commented out

        # Handle planCode from listPolicyCoverage
        list_policy_coverage = first_policy.get("listPolicyCoverage", [])

        if len(list_policy_coverage) > 0:
            collection_vars["planCode"] = list_policy_coverage[0].get("planCode", "")
        else:
            collection_vars["planCode"] = ""

    print("collection_vars:", collection_vars)



################ Step 4: Get Member Data
    url_get_data_member = f"{BASE_URL_IFGID_UAT}/api/v6/ekyc/data/getEkycInfo"
    headers = {
        "apiKey": API_KEY_IFGID_UAT,
        "Content-Type": "application/json"
    }
    payload_get_data_member = {
        "ekycId": collection_vars.get("cif")
    }
    response_get_data_member = requests.post(
        url=url_get_data_member,
        headers=headers,
        json=payload_get_data_member
    )
    body_get_data_member = response_get_data_member.json()
    assert response_get_data_member.status_code == 200


    if body_get_data_member.get("data") and len(body_get_data_member["data"]) > 0:
        first_data = body_get_data_member["data"][0]
        id_card = first_data.get("idCard", {})

        # Extract values
        name = id_card.get("name")
        id_card_no = id_card.get("idCardNo")
        address = id_card.get("address")
        dob = id_card.get("dob")

        # Convert date from dd-mm-yyyy → yyyy-mm-dd
        formatted_dob = None
        if dob:
            formatted_dob = datetime.strptime(dob, "%d-%m-%Y").strftime("%Y-%m-%d")

        # Set collection variables
        collection_vars["name"] = name
        collection_vars["idCardNo"] = id_card_no
        collection_vars["address"] = address
        collection_vars["dob"] = formatted_dob
        
    print("Step 4 -- get data member body: ", collection_vars)


################ Step 5: Create Workflow Transaction Header
    now = datetime.now()

    # ✅ formattedDate: yyyy-MM-dd HH:mm:ss
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    collection_vars["formattedDate"] = formatted_date
    

    # ✅ hhmmss: ddHHmmss (based on your Postman logic)
    hhmmss = now.strftime("%d%H%M%S")

    collection_vars["referenceNo"] = (
        "kang2025-dese-" +
        str(uuid.uuid4())[:9] +
        "-REMOVEKA" +
        hhmmss
    )
   
    formatted_today = now.strftime("%Y-%m-%d")
    collection_vars["today"] = formatted_today



    url_transaction_header = (
        f"{BASE_URL_AOPS_UAT}/api/v2/ao-workflow-claim/general/transaction/header"
    )

    headers = {
        "apiKey": API_KEY_AOPS_UAT,
        "Content-Type": "application/json"
    }

    payload_transaction_header = {
        "referenceNo": collection_vars.get("referenceNo"),
        "referenceType": "CLAIM_SUBMISSION_NO",
        "transactionType": "lifespace-ps-remove-member",
        "workflow": "",
        "instanceId": "",
        "status": "",
        "details": {
            "PAYLOAD_SUBMISSION": {
                "id": "",
                "transactionEventId": "",
                "transactionEventNumber": "",
                "policyNumber": collection_vars.get("organizationPolicyNumber"),
                "organizationId": collection_vars.get("organizationId"),
                "submissionDate": collection_vars.get("formattedDate"),
                "status": "",
                "transactionEventVariable": [
                    {
                        "code": "PREMIUM_REFUND",
                        "type": "string",
                        "value": collection_vars.get("refundValue")
                    },
                    {
                        "code": "NO_SURAT_REFERENSI",
                        "type": "string",
                        "value": f"KA-{random.randint(0, 1000)}{random.randint(0, 1000)}/TEST/2026"
                    },
                    {
                        "code": "TANGGAL_SURAT_REFERENSI",
                        "type": "date",
                        "value": collection_vars.get("today")
                    },
                    {
                        "code": "PIC_NAME",
                        "type": "string",
                        "value": "QA POS Testing"
                    },
                    {
                        "code": "PIC_EMAIL",
                        "type": "string",
                        "value": "paulus.siahaan@ifg-life.id"
                    },
                    {
                        "code": "PIC_PHONE_NUMBER",
                        "type": "string",
                        "value": "-"
                    },
                    {
                        "code": "PIC_POSITION",
                        "type": "string",
                        "value": "-"
                    }
                ],
                "message": ""
            },
            "DECISION": {}
        }
    }

    response_transaction_header = requests.post(
        url=url_transaction_header,
        headers=headers,
        json=payload_transaction_header,
        timeout=30
    )

    # assert response_transaction_header.status_code == 200, (
    #     f"Unexpected status code: {response_transaction_header.status_code}, "
    #     f"Body: {response_transaction_header.text}"
    # )

    body_transaction_header = response_transaction_header.json()
    print("Step 5 -- create workflow transaction header body: ", body_transaction_header)


################ Step 6: Get Transaction Header Detail
    url_get_data_member = f"{BASE_URL_IFGID_UAT}/api/v6/ekyc/data/getEkycInfo"
    headers = {
        "apiKey": API_KEY_IFGID_UAT,
        "Content-Type": "application/json"
    }
    payload_get_data_member = {
        "ekycId": collection_vars.get("cif")
    }
    response_get_data_member = requests.post(
        url=url_get_data_member,
        headers=headers,
        json=payload_get_data_member
    )
    body_get_data_member = response_get_data_member.json()
    assert response_get_data_member.status_code == 200
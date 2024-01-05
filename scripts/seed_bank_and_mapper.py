#!/usr/bin/env python3

import uuid
import sys
import csv

import requests

mojaloop_dfsp_api_url = "https://bank2.qa.openg2p.net/api/test/repository/parties"
mapper_link_api_url = "https://spar.qa.openg2p.net//mapper/v0.1.0/mapper/link"


with open(sys.argv[1], 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    csv_content = list(csv_reader)
    header = csv_content[0]
    dfsp_list = []
    id_mapper_list = []
    for line in csv_content[1:]:
        national_id = line[header.index("nationalid")]
        first_name = line[header.index("given_name")]
        middle_name = line[header.index("addl_name")]
        last_name = line[header.index("family_name")]
        display_name = f"{first_name} {middle_name} {last_name}"
        dob = line[header.index("dob")]
        id_type = "ACCOUNT_ID"
        id_value = line[header.index("account_no")]
        dfsp_list.append({
            "displayName": display_name,
            "firstName": first_name,
            "middleName": middle_name,
            "lastName": last_name,
            "dateOfBirth": dob,
            "idType": id_type,
            "idValue": id_value,
        })
        id_mapper_list.append({
            "reference_id": str(uuid.uuid4()),
            "timestamp": "2022-12-04T17:20:07-04:00",
            "id": f"token:{national_id}@nationalId",
            "fa": f"account:{id_value}@rhino.dfsp2.bank_acc",
            "name": None,
            "phone_number": None,
            "additional_info": None,
            "locale": "eng",
        })
    
    for i, party in enumerate(dfsp_list):
        res = requests.post(mojaloop_dfsp_api_url, json=party)
        res.raise_for_status()
        print(f"Created {i} parties")
    
    res = requests.post(mapper_link_api_url, json={
        "header": {
            "action": "link",
            "is_encrypted": False,
            "message_id": str(uuid.uuid4()),
            "message_ts": "2022-12-04T18:01:07+00:00",
            "receiver_id": "pymts.example.org",
            "sender_id": "registry.example.org",
            "sender_uri": "http://spar-social-payments-account-registry.spar/internal/callback/mapper",
            "total_count": 0,
            "version": "0.1.0"
        },
        "message": {
            "link_request": id_mapper_list,
            "transaction_id": str(uuid.uuid4())
        },
        "signature": "Signature:  namespace=\"g2p\", kidId=\"{sender_id}|{unique_key_id}|{algorithm}\", algorithm=\"ed25519\", created=\"1606970629\", expires=\"1607030629\", headers=\"(created) (expires) digest\", signature=\"Base64(signing content)"
    })
    print(res.text)
    res.raise_for_status()
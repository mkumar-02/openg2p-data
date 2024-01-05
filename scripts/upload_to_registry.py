#!/usr/bin/env python3

import pyjq
import csv
import sys
import requests

auth_url = "https://mec.openg2p.net/web/session/authenticate"
username = "mtsuser1@none.ignore"
password = "1234567890"
database = "openg2pdb"
api_url = "https://mec.openg2p.net/api/v1/registry/group/"
jq_expr_path = "eth-outputformat.jq"

with open(sys.argv[1], 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    csv_content = list(csv_reader)
    session_id = requests.get(auth_url, json={
        "jsonrpc": "2.0",
        "params": {
            "db": database,
            "login": username,
            "password":password
        }
    }).cookies.get("session_id", None)
    header = csv_content[0]
    for i, line in enumerate(csv_content[1:]):
        result = pyjq.first(open(jq_expr_path, 'r').read().replace("\n", ""), {
            "input": {header[j]: line[j] for j in range(len(line))}
        })
        api_res = requests.post(api_url, cookies={"session_id": session_id}, json=result)
        api_res.raise_for_status()
        print(f"Done line {i}")

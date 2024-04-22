#!/usr/bin/env python3
from cryptography.hazmat.primitives import hashes
import base64
import pyjq
import csv
import sys
import requests

auth_url = "https://nig.openg2p.org/web/session/authenticate"
username = "mtsuser1@none.ignore"
password = "1234567890"
database = "openg2pdb"
api_url = "https://nig.openg2p.org/api/v1/registry/group/"
jq_expr_path = "group-outputformat.jq"
generate_token_hash = True
token_hash_algo = "SHA3_256"
token_partner_id = "openg2p-auth-partner"

def generate_psut(vid : str, partner_id: str, hash_algo: str):
    hash_algo = getattr(hashes, hash_algo)()
    digest = hashes.Hash(hash_algo)
    digest.update(f'{vid}{partner_id}'.encode(encoding="utf-8"))
    return base64.urlsafe_b64encode(digest.finalize()).decode().rstrip("=")

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
        line_data = {header[j]: line[j] for j in range(len(line))}
        if generate_token_hash:
            line_data["Token ID"] = generate_psut(line_data["UIN"], token_partner_id, token_hash_algo)
        result = pyjq.first(open(jq_expr_path, 'r').read().replace("\n", ""), {
            "input": line_data
        })
        api_res = requests.post(api_url, cookies={"session_id": session_id}, json=result)
        api_res.raise_for_status()
        print(f"Done line {i}")

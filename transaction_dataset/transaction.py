import subprocess

monerod_process = subprocess.Popen(["monerod", "--detach"])

import requests

wallet_rpc_url = "http://localhost:18082/json_rpc"
headers = {"Content-Type": "application/json"}

# Example JSON-RPC request to create a transaction
payload = {
    "jsonrpc": "2.0",
    "id": "0",
    "method": "transfer",
    "params": {
        "destinations": [{"amount": 1000000000, "address": "<recipient_address>"}],
        "account_index": 0,
        "subaddr_indices": [],
        "priority": 1,
        "ring_size": 10,
        "get_tx_key": True,
        "do_not_relay": False,
        "get_tx_hex": True
    }
}

response = requests.post(wallet_rpc_url, headers=headers, json=payload)
response_data = response.json()

if "result" in response_data:
    tx_hash = response_data["result"]["tx_hash"]
    tx_key = response_data["result"]["tx_key"]
    tx_hex = response_data["result"]["tx_blob"]
    print("Transaction created successfully:")
    print("Tx Hash:", tx_hash)
    print("Tx Key:", tx_key)
    print("Tx Hex:", tx_hex)
else:
    print("Error:", response_data["error"]["message"])

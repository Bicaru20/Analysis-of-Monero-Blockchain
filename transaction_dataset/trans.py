import requests
import json

# Configuration for sender wallet RPC
sender_wallet_rpc_url = "http://localhost:28083/json_rpc"

# Configuration for receiver wallet address
receiver_address = "9wq792k9sxVZiLn66S3Qzv8QfmtcwkdXgM5cWGsXAPxoQeMQ79md51PLPCijvzk1iHbuHi91pws5B7iajTX9KTtJ4bh2tCh" #wallet 1

# Transfer amount (in atomic units, 1 XMR = 1e12 atomic units)
transfer_amount = 1000000000000  # 1 XMR

# Function to make JSON-RPC requests
def get_balance(url, method, params):
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "get_balance",
        "params": {"account_index":0,"address_indices":[0,1]}
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

def transfer(url, receiver):
    headers = {"Content-Type": "application/json"}
    payload = {"jsonrpc":"2.0","id":"0","method":"transfer","params":{"destinations": [{"amount":100000000000,
                "address": receiver}
                ],
                "ring_size": 1}}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

# Transfer XMR
def transfer_xmr(sender_url, receiver, amount):
    params = {
        "destinations": [{"amount": amount, "address": receiver}],
        "account_index": 0,
        "subaddr_indices": [],
        "priority": 1,
        "ring_size": 1,
        "get_tx_key": True,
        "do_not_relay": False,
        "get_tx_hex": True
    }
    response = transfer(sender_url,  receiver)
    if "result" in response:
        tx_hash = response["result"]["tx_hash"]
        tx_key = response["result"]["tx_key"]
        tx_hex = response["result"]["tx_blob"]
        print(f"Transaction created successfully:\nTx Hash: {tx_hash}\nTx Key: {tx_key}\nTx Hex: {tx_hex}")
    else:
        print(f"Error: {response['error']['message']}")

# Perform the transfer
transfer_xmr(sender_wallet_rpc_url, receiver_address, transfer_amount)

import requests
import json
import random
import time 

from config import sender_wallet_rpc_url, receiver_address

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

def transfer(url, params):
    headers = {"Content-Type": "application/json"}
    payload = {"jsonrpc":"2.0","id":"0","method":"transfer","params":params}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

# Transfer XMR
def transfer_xmr(sender_url, receiver, amount):
    params = {
        "destinations": [{"amount": amount, "address": receiver}],
        "account_index": 0,
        "subaddr_indices": [],
        "priority": 1,
        "ring_size": 2,
        "get_tx_key": True,
        "do_not_relay": False,
        "get_tx_hex": True
    }
    response = transfer(sender_url,  params)
    if "result" in response:
        tx_hash = response["result"]["tx_hash"]
        tx_key = response["result"]["tx_key"]
        tx_hex = response["result"]["tx_blob"]
        # print(f"Transaction created successfully:\nTx Hash: {tx_hash}\nTx Key: {tx_key}\nTx Hex: {tx_hex}")
    else:
        print(f"Error: {response['error']['message']}")


# Transfer amount (in atomic units, 1 XMR = 1e12 atomic units)
for x in range(50):
    transfer_amount = random.randint(5000000000000, 20000000000000)  # 1 XMR
    index = random.randint(0,1)
    sender_wallet = sender_wallet_rpc_url[0]
    i = index
    while i == index:
        i = random.randint(0,2)
    receiver = receiver_address[1]
    transfer_xmr(sender_wallet, receiver, transfer_amount)
    print('Transaction done. Number: ', x)
    print('Transaction quantity: ', transfer_amount/(10**12))
    print('Send to wallet: ', i)
    print('----------------')

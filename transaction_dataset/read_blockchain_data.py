import requests
import json

# Monero daemon RPC URL
rpc_url = "http://localhost:28081/json_rpc"

# Function to make JSON-RPC requests to monerod
def make_rpc_request(method, params=None):
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": method,
        "params": params or {}
    }
    response = requests.post(rpc_url, headers=headers, data=json.dumps(payload))
    return response.json()

# Fetch the current block height
def get_block_count():
    response = make_rpc_request("get_block_count")
    if "result" in response:
        return response["result"]["count"]
    else:
        print(f"Error: {response['error']['message']}")
        return None

# Fetch a block by its height
def get_block_by_height(height):
    params = {"height": height}
    response = make_rpc_request("get_block", params)
    if "result" in response:
        return response["result"]["block"]
    else:
        print(f"Error: {response['error']['message']}")
        return None

# Fetch transaction details by transaction ID
def get_transaction(txid):
    params = {"txs_hashes": [txid]}
    response = make_rpc_request("get_transactions", params)
    if "result" in response:
        return response["result"]["txs"]
    else:
        print(f"Error: {response['error']['message']}")
        return None

# Example usage
if __name__ == "__main__":
    block_count = get_block_count()
    if block_count:
        print(f"Current block height: {block_count}")

        # Get the latest block
        latest_block = get_block_by_height(block_count - 1)
        if latest_block:
            print(f"Latest block: {latest_block}")

            # Get transactions from the latest block
            block_data = json.loads(latest_block)
            tx_hashes = block_data["tx_hashes"]
            for txid in tx_hashes:
                transaction = get_transaction(txid)
                print(f"Transaction {txid}: {transaction}")

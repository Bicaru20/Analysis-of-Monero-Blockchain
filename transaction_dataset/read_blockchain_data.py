import requests
import json
import pandas as pd

from to_neo4j import new_node

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
        return response["result"]["json"]
    else:
        print(f"Error: {response['error']['message']}")
        return None

def get_transactions(txid):
    url = "http://127.0.0.1:28081/get_transactions"
    # Define the JSON payload
    payload = {
        "txs_hashes": [
            txid
    ],
    "decode_as_json":True
    }
    # Define the headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Fetch transaction details by transaction ID
def get_transaction(txid):
    response = get_transactions(txid)
    if "txs_as_json" in response:
        return response['txs']
    else:
        print(f"Error: {response['error']['message']}")
        return None

# Example usage
if __name__ == "__main__":
    block_count = get_block_count()
    if block_count:
        # print(f"Current block height: {block_count}")

        # Get the latest block
        # inputs = {'Block': [], 'Amount': [], 'total_amount': [], 'key_image': []}
        # outputs = {'Block': [], 'Amount': [], 'total_amount': [], 'key': []}
        new_n = False
        new_n_out = False
        block_c = 0
        for real in range(3529, 3530): # 3269 3271
            print("-----------------")
            print("BLOCK: ", real)
            latest_block = get_block_by_height(real)
            block_c += 1
            inputs_neo = []
            outputs_neo = []
            new_n = False
            new_n_out = False
            if latest_block:
                # print(f"Latest block: {latest_block}")

                # Get transactions from the latest block
                block_data = json.loads(latest_block)
                tx_hashes = block_data["tx_hashes"]
                for txid in tx_hashes:
                    transaction = get_transaction(txid)
                    if transaction is None: continue
                    for trans in transaction:
                        t = json.loads(trans['as_json'])
                        vin = t['vin']
                        vout = t['vout']
                        # print(f"Transaction {txid}: {vin}\n")
                        total = 0
                        new_n = False
                        new_n_out = False
                        for v in vin:
                            # inputs['Block'].append(block_c)
                            new_n = True
                            temp = v['key']['amount']/(10**12)
                            total += temp
                            # key_image = v['key']['k_image']
                            # inputs['Amount'].append(temp)
                            # inputs['total_amount'].append(total)
                            # inputs['key_image'].append(key_image)
                        inputs_neo.append({'Block': block_c, 'Amount': total, 'txid': txid})
                        total = 0
                        for v in vout:
                             new_n_out = True

                        #     outputs['Block'].append(block_c)
                             temp = v['amount']/(10**12)
                             total += temp
                        #     key_image = v['target']['key']
                        #     outputs['Amount'].append(temp)
                        #     outputs['total_amount'].append(total)
                        #     outputs['key'].append(key_image)
                        outputs_neo.append({'Block': block_c, 'Amount': total, 'txid': txid})
                        
            new_node(inputs_neo) if new_n else new_node([{'Block': block_c, 'Amount': 0, 'txid': 0}])
            if new_n_out: new_node(outputs_neo, out= True)                
        # pd.DataFrame(inputs).to_csv('Inputs_transactions.csv', index=False)
        # pd.DataFrame(inputs).to_csv('Outputs_transactions.csv', index=False)
                        

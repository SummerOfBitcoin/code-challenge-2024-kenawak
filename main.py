import json
import hashlib
import os

# Function to validate JSON contents
def validate_json(json_data):
    required_keys = ['txid', 'hash', 'version', 'locktime', 'vin', 'vout']
    for key in required_keys:
        if key not in json_data:
            return False
    if json_data['version'] != 1:
        return False
    return True

# Function for proof of work
def proof_of_work(data, target):
    nonce = 0
    while True:
        hash_result = hashlib.sha256((data + str(nonce)).encode()).hexdigest()
        if hash_result < target:
            return nonce, hash_result
        nonce += 1

# Function to mine block from mempool transactions
def mine_block_from_mempool(mempool_path, difficulty_target):
    transactions = []
    for filename in os.listdir(mempool_path):
        with open(os.path.join(mempool_path, filename), 'r') as file:
            data = json.load(file)
            if validate_json(data):
                transactions.append(data)
    block_header = json.dumps(transactions)
    nonce, block_hash = proof_of_work(block_header, difficulty_target)
    return nonce, block_hash, transactions

# Sample usage
mempool_folder = './mempool/'
difficulty_target = "0000ffff00000000000000000000000000000000000000000000000000000000"
output_file = "output.txt"

nonce, block_hash, transactions = mine_block_from_mempool(mempool_folder, difficulty_target)

with open(output_file, 'w') as f:
    # Write block header to file
    f.write("The block header:\n")
    f.write(json.dumps(transactions) + "\n")

    # Serialize coinbase transaction
    coinbase_transaction = json.dumps(transactions[0]['vin'][0])

    # Write serialized coinbase transaction to file
    f.write("The serialized coinbase transaction:\n")
    f.write(coinbase_transaction + "\n")

    # Write transaction IDs (txids) of the transactions mined in the block to file
    f.write("Transaction IDs (txids) of the transactions mined in the block:\n")
    for transaction in transactions:
        f.write(transaction['txid'] + "\n")

from config import DRIVER as driver

def create_transaction(tx, txid, block_height, amount, out ):
    
    if not out:
        # Create nodes and relationships for transactions
        if txid == 0:
                tx.run("""
                MERGE (b:Block {height: $block_height})
                MERGE (t:inpu)-[:INPUT]->(b)
                """, block_height=block_height)
        else:
                tx.run("""
                MERGE (b:Block {height: $block_height})
                MERGE (t:Transaction {txid: $txid})
                ON CREATE SET t.amount = $amount
                MERGE (t)-[:INPUT]->(b)
                """, block_height=block_height, txid=txid, amount=amount)
        
        # Create relationship between current block and previous block if previous_block_height is not None
        tx.run("""
        MATCH (b:Block {height: $block_height})
        OPTIONAL MATCH (pb:Block {height: $previous_block_height})
        WHERE pb IS NOT NULL
        MERGE (b)-[:PREVIOUS_BLOCK]->(pb)
        """, block_height=block_height, previous_block_height=block_height-1)
    
    else:
        tx.run("""
                MERGE (b:Block {height: $block_height})
                MERGE (t:Transaction {txid: $txid})
                ON CREATE SET t.amount = $amount
                MERGE (b)-[:OUTPUT]->(t)
                """, block_height=block_height, txid=txid, amount=amount)

def new_node(transactions, out= False):
    with driver.session() as session:

        for tx in transactions:
            session.write_transaction(create_transaction, tx["txid"], tx["Block"], tx["Amount"], out)

    # Close the driver connection
    driver.close()

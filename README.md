# Analysis-of-Monero-Blockchain
TFG de Biel Castellarnau Ruiz estudiant del grau de enginyeria de dades (2020-2024) a la UAB.


Cypher queries to create the dataset:
    
    ```cypher
LOAD CSV FROM 'file:///csv_headers/blocks.csv' AS row
WITH collect(row)[0] AS columns
LOAD CSV FROM 'file:///csv/blocks.csv' AS row
WITH row, columns
CREATE (b:Block {
  id: row[toInteger(apoc.coll.indexOf(columns, ':ID'))],
  height: toInteger(row[toInteger(apoc.coll.indexOf(columns, ':height'))]),
  hash: row[toInteger(apoc.coll.indexOf(columns, ':hash'))],
  timestamp: row[toInteger(apoc.coll.indexOf(columns, ':timestamp'))]
});
    ```
    
    ```cypher
    // Load column names into a list
LOAD CSV FROM 'file:///csv_headers/blocks-rels.csv' AS row
WITH collect(row)[0] AS columns
// Load data using the column names
LOAD CSV FROM 'file:///csv/blocks-rels.csv' AS row
WITH row, columns
MATCH (b1:Block {id: row[toInteger(apoc.coll.indexOf(columns, ':START_ID'))]})
MATCH (b2:Block {id: row[toInteger(apoc.coll.indexOf(columns, ':END_ID'))]})
CREATE (b1)-[pb:PREV_BLOCK]->(b2);
    ```
    
    ```cypher
LOAD CSV FROM 'file:///csv_headers/blocks.csv' AS row
WITH collect(row)[0] AS columns
LOAD CSV FROM 'file:///csv/blocks.csv' AS row
WITH row, columns
CREATE (b:Block {
  id: row[toInteger(apoc.coll.indexOf(columns, ':ID'))],
  height: toInteger(row[toInteger(apoc.coll.indexOf(columns, ':height'))]),
  hash: row[toInteger(apoc.coll.indexOf(columns, ':hash'))],
  timestamp: row[toInteger(apoc.coll.indexOf(columns, ':timestamp'))]
});
    ```
    
    ```cypher
    LOAD CSV FROM 'file:///csv_headers/transactions.csv' AS row
WITH collect(row)[0] AS columns
LOAD CSV FROM 'file:///csv/transactions.csv' AS row
WITH row, columns
CREATE (t:Transactions {
  id: row[toInteger(apoc.coll.indexOf(columns, ':ID'))],
  hash: row[toInteger(apoc.coll.indexOf(columns, 'hash'))],
  fee: row[toInteger(apoc.coll.indexOf(columns, 'fee'))]
});
    ```
    
    ```cypher
LOAD CSV FROM 'file:///csv_headers/tx-blocks.csv' AS row
WITH collect(row)[0] AS columns
// Load data using the column names
LOAD CSV FROM 'file:///csv/tx-blocks.csv' AS row
WITH row, columns
MATCH (t:Transactions {id: row[toInteger(apoc.coll.indexOf(columns, ':START_ID'))]})
MATCH (b:Block {id: row[toInteger(apoc.coll.indexOf(columns, ':END_ID'))]})
CREATE (t)-[ib:IN_BLOCK]->(b);
    ```
    
    ```cypherLOAD CSV FROM 'file:///csv_headers/outputs.csv' AS row
WITH collect(row)[0] AS columns
LOAD CSV FROM 'file:///csv/outputs.csv' AS row
WITH row, columns
CREATE (o:Outputs {
  id: row[toInteger(apoc.coll.indexOf(columns, ':ID'))],
  value: row[toInteger(apoc.coll.indexOf(columns, 'value'))],
  inde: row[toInteger(apoc.coll.indexOf(columns, 'index'))]
});
    ```
    
    ```cypher
    LOAD CSV FROM 'file:///csv_headers/output-rels.csv' AS row
WITH collect(row)[0] AS columns
// Load data using the column names
LOAD CSV FROM 'file:///csv/output-rels.csv' AS row
WITH row, columns
MATCH (t:Transactions {id: row[toInteger(apoc.coll.indexOf(columns, ':START_ID'))]})
MATCH (o:Outputs {id: row[toInteger(apoc.coll.indexOf(columns, ':END_ID'))]})
CREATE (t)-[txo:TX_OUTPUT]->(o);
    ```
    
    ```cypher
LOAD CSV FROM 'file:///csv_headers/inputs.csv' AS row
WITH collect(row)[0] AS columns
LOAD CSV FROM 'file:///csv/inputs.csv' AS row
WITH row, columns
CREATE (i:Input {
  id: row[toInteger(apoc.coll.indexOf(columns, ':ID'))],
  value: row[toInteger(apoc.coll.indexOf(columns, 'value'))],
  mixin: row[toInteger(apoc.coll.indexOf(columns, 'mixin'))],
  anonset: row[toInteger(apoc.coll.indexOf(columns, 'anonset'))],
  key_offset: row[toInteger(apoc.coll.indexOf(columns, 'key_offset'))]
});
    ```
    
    ```cypher
LOAD CSV FROM 'file:///csv_headers/input-rels.csv' AS row
WITH collect(row)[0] AS columns
// Load data using the column names
LOAD CSV FROM 'file:///csv/input-rels.csv' AS row
WITH row, columns
MATCH (t:Transactions {id: row[toInteger(apoc.coll.indexOf(columns, ':START_ID'))]})
MATCH (i:Input {id: row[toInteger(apoc.coll.indexOf(columns, ':END_ID'))]})
CREATE (i)-[txi:TX_INPUT]->(t)
    ```
    
    ```cypherLOAD CSV FROM 'file:///csv_headers/input-output-refs.csv' AS row
WITH collect(row)[0] AS columns
// Load data using the column names
LOAD CSV FROM 'file:///csv/input-output-refs.csv' AS row
WITH row, columns
MATCH (o:Outputs {id: row[toInteger(apoc.coll.indexOf(columns, ':END_ID'))]})
MATCH (i:Input {id: row[toInteger(apoc.coll.indexOf(columns, ':START_ID'))]})
CREATE (i)-[ref:REFERENCES]->(t)
    ```
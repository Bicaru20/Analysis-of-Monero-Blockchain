from neo4j import GraphDatabase

# Configuration for sender wallet RPC
sender_wallet_rpc_url = ["http://localhost:28083/json_rpc", "http://localhost:38083/json_rpc", "http://localhost:48083/json_rpc"]

# Configuration for receiver wallet address
receiver_address = ["9wviCeWe2D8XS82k2ovp5EUYLzBt9pYNW2LXUFsZiv8S3Mt21FZ5qQaAroko1enzw3eGr9qC7X1D7Geoo2RrAotYPwq9Gm8", "9wq792k9sxVZiLn66S3Qzv8QfmtcwkdXgM5cWGsXAPxoQeMQ79md51PLPCijvzk1iHbuHi91pws5B7iajTX9KTtJ4bh2tCh", "A2rgGdM78JEQcxEUsi761WbnJWsFRCwh1PkiGtGnUUcJTGenfCr5WEtdoXezutmPiQMsaM4zJbpdH5PMjkCt7QrXAhV8wDB"]

# Connection to Neo4j
CONN = "bolt://localhost:7687"
USER = "neo4j"
PSW = "123"
DRIVER = GraphDatabase.driver(CONN, auth= (USER, PSW))

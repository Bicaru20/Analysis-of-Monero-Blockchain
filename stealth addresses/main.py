from Bob import Bob
from Alice import Alice
from ecdsa.ellipticcurve import CurveEdTw, PointEdwards, Point
from confi import G, l

import hashlib


user_Bob = Bob(G, l)
user_Alice = Alice(G)

# Bob publics keys
Apub = user_Bob.get_Apub()
Bpub = user_Bob.get_Bpub()
print(f"Apub : {(Apub.x(), Apub.y())}")
print(f"Bpub : {(Bpub.x(), Bpub.y())}")

# Alice generates a new unique PubKey
P, R = user_Alice.new_public_key(Apub, Bpub)
print(f"P : {(P.x(), P.y())}")
print(f"R : {(R.x(), R.y())}")

# Bob checks the transaction
print(user_Bob.check_transaction(R, P))


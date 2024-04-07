from Bob import Bob
from Alice import Alice

# Define the parameters
q = 2**255 - 19
d = -121665/121666
# E = lambda x, y: -x**2 + y**2 - 1 - d*x**2*y**2
# G = E(-0.4302, 0.8)
x = 15112221349535400772501151409588531511454012693041857206046113283949847762202
y = 11579208923731619542357098500868790785326998466564056403945758400791312963989
G = (x, y)
l = 2**252 + 27742317777372353535851937790883648493

user_Bob = Bob(G, l)
user_Alice = Alice(G)

# Bob publics keys
Apub = user_Bob.get_Apub()
Bpub = user_Bob.get_Bpub()
print(f"Apub : {Apub}")
print(f"Bpub : {Bpub}")

# Alice generates a new unique PubKey
P, R = user_Alice.new_public_key(Apub, Bpub)
print(f"P : {P}")
print(f"R : {R}")



# Bob checks the transaction
print(user_Bob.check_transaction(R, P))


from config import G, l, q
from ring_signature import Ring


ring = Ring(G, l, q)
message = "Hello world"
n = 5
omega = ring.sign(message, n)
print(omega)
print(ring.verification(omega, n, message))
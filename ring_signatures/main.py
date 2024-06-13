from config import G, l, q
from ring_signature import Ring
import random

ring = Ring(G, l, q)
message = "Hello world"

for _ in range(10):
    n = random.randint(5,15)
    omega = ring.sign(message, n)
    print(ring.verification(omega, n, message))
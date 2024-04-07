from ring_signature import Ring

# Define the parameters
q = 2**255 - 19
d = -121665/121666
# E = lambda x, y: -x**2 + y**2 - 1 - d*x**2*y**2
# G = E(-0.4302, 0.8)
x = 15112221349535400772501151409588531511454012693041857206046113283949847762202
y = 11579208923731619542357098500868790785326998466564056403945758400791312963989
# G = (x, y)
G = 33
l = 2**252 + 27742317777372353535851937790883648493


ring = Ring(G, l, q)
message = "Hello world"
n = 5
omega = ring.sign(message, n)
print(omega)
print(ring.verification(omega, n))
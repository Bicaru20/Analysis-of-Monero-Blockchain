from ecdsa.ellipticcurve import CurveEdTw, PointEdwards, Point
import random

# Define the parameters
q = 2**255 - 19

# Invers of a number mod q
def inv_mod_q(a):
    return pow(a, q-2, q)

d = -121665*inv_mod_q(121666)
# E = lambda x, y: -x**2 + y**2 - 1 - d*x**2*y**2
# G = E(-0.4302, 0.8)
x = 15112221349535400772501151409588531511454012693041857206046113283949847762202
y = 11579208923731619542357098500868790785326998466564056403945758400791312963989
# G = (x, y)
G = 33
l = 2**252 + 27742317777372353535851937790883648493

curve_ed25519 = CurveEdTw(q, -1, int(d))
print(curve_ed25519.contains_point(x, y))
G = PointEdwards(curve_ed25519, x, y, 1, x*y, generator=True)
infinite = Point(None, None, None)
x = random.randint(1, l)

def double_and_add(point, escalar, infinite):
    bin_str = bin(escalar)[2:]
    result = infinite

    for i, e in enumerate(bin_str[::-1]):
        if e == "1":
            result = result + point
        if i != len(bin_str) - 1:
            point = point.double()
    return result

Pub = double_and_add(G, x, infinite)
print(curve_ed25519.contains_point(Pub.x(), Pub.y()))
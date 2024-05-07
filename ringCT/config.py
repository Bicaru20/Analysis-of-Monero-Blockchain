from ecdsa.ellipticcurve import CurveEdTw, PointEdwards, Point
from helper import inv_mod_q

# Define the curve parameters
q = 2**255 - 19
d = -121665*inv_mod_q(121666, q)
x = 15112221349535400772501151409588531511454012693041857206046113283949847762202
y = 11579208923731619542357098500868790785326998466564056403945758400791312963989
G = (x, y)
l = 2**252 + 27742317777372353535851937790883648493

# Define the curve
curve_ed25519 = CurveEdTw(q, -1, int(d))
if curve_ed25519.contains_point(x, y):
    G = PointEdwards(curve_ed25519, x, y, 1, x*y, generator=True)

infinite = Point(None, None, None)

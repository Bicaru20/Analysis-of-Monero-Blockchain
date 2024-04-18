def double_and_add(point, escalar, infinite):
    bin_str = bin(escalar)[2:]
    result = infinite

    for i, e in enumerate(bin_str[::-1]):
        if e == "1":
            result = result + point
        if i != len(bin_str) - 1:
            point = point.double()
    return result

def inv_mod_q(a, q):
    return pow(a, q-2, q)
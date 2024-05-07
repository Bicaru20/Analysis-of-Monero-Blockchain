import hashlib 

def H(m):
    if isinstance(m, list):
        m = ''.join(m)
    m = str(m)
    msg = m.encode("utf-8")
    msg_hash = hashlib.sha1(msg).digest()
    return msg_hash

def H_s(m, q):
    if isinstance(m, list):
        m = ''.join(m)
    m = str(m)
    msg = m.encode("utf-8")
    msg_hash = hashlib.sha1(msg).digest()
    hashed_int = int.from_bytes(msg_hash, byteorder='big')
    # Reduce the integer modulo q to get a value between 0 and q-1
    result = hashed_int % q
    return result
            


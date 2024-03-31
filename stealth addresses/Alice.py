import hashlib
import random

class Alice():
    def __init__(self, generator) -> None:
        self.__r = random.randint(0, 2**256)
        self.R = generator*self.__r
        self.generator = generator

    def new_public_key(self, A, B):
        P = (self._permut(A*self.__r))*self.generator + B
        return P, self.R
    
    def _permut(self, m):
        m = str(m)
        msg = m.encode("utf-8")
        return int(hashlib.sha1(msg).hexdigest(), 16)
    

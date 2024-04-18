import hashlib
import random

from helper import double_and_add
from confi import infinite, q
class Alice():
    def __init__(self, generator) -> None:
        self.__r = random.randint(0, 2**256)
        self.R = double_and_add(generator, self.__r, infinite)
        self.generator = generator

    def new_public_key(self, A, B):
        P = (double_and_add(A, self.__r, infinite))
        P_hash = self.__Hs(hex(P.x())[2:] + hex(P.y())[2:])
        P = double_and_add(self.generator, P_hash, infinite) + B
        return P, self.R
    
    def __Hs(self, input):
        msg = input.encode("utf-8")

        hash_object = hashlib.sha256()
        hash_object.update(msg)  
        hash_bytes = hash_object.digest()
        
        hash_value = int.from_bytes(hash_bytes, byteorder='big')
        
        return hash_value % q
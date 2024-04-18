import hashlib
import random

from helper import double_and_add
from confi import infinite, q


class Bob():
    def __init__(self, generator, l) -> None:
        self.__Apriv = random.randint(1, l)
        self.Apub = double_and_add(generator, self.__Apriv, infinite)

        self.__Bpriv = random.randint(1, l)
        self.Bpub = double_and_add(generator, self.__Bpriv, infinite)

        self.generator = generator

        # Public key to str
        self.Apubstr = hex(self.Apub.x())[2:] + hex(self.Apub.y())[2:]
        self.Bpubstr = hex(self.Bpub.x())[2:] + hex(self.Bpub.y())[2:]

    def get_Apriv(self, pwd):
        if pwd == "password":
            return self.__Apriv
    
    def get_Bpriv(self, pwd):
        if pwd == "password":
            return self.__Bpriv
    
    def get_Apub(self):
        return self.Apub
    
    def get_Bpub(self):
        return self.Bpub
        
    def check_transaction(self, R, P):
        point = double_and_add(R, self.__Apriv, infinite)
        hash_point = self.__Hs(hex(point.x())[2:] + hex(point.y())[2:])
        x = hash_point + self.__Bpriv
        P_Bob = double_and_add(self.generator, x, infinite)
        if P == P_Bob:
            return True
        return False
    
    def __Hs(self, input):
        msg = input.encode("utf-8")

        hash_object = hashlib.sha256()
        hash_object.update(msg)  
        hash_bytes = hash_object.digest()
        
        hash_value = int.from_bytes(hash_bytes, byteorder='big')
        
        return hash_value % q
    


# print(f"Private key : {crypto.dump_privatekey(crypto.FILETYPE_PEM, BobA)}\n")
# print(f"Public key : {crypto.dump_publickey(crypto.FILETYPE_PEM, BobA)}\n")

# print(f"Private key : {crypto.dump_privatekey(crypto.FILETYPE_PEM, BobB)}\n")
# print(f"Public key : {crypto.dump_publickey(crypto.FILETYPE_PEM, BobB)}\n")

# self.p = int(hashlib.sha1(msg).hexdigest(), 16)
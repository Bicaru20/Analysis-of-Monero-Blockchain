from OpenSSL import crypto
import hashlib
import random


class Bob():
    def __init__(self, generator, l) -> None:
        self.__Apriv = random.randint(1, l)
        self.Apub = self.__Apriv * generator

        self.__Bpriv = random.randint(1, l)
        self.Bpub = self.__Bpriv * generator

        self.generator = generator

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
        x = self._permut(self.__Apriv*R)*self.generator + self.__Bpriv
        if P == x:
            return True
        return False
    
    def _permut(self, m):
        m = str(m)
        msg = m.encode("utf-8")
        return int(hashlib.sha1(msg).hexdigest(), 16)

# print(f"Private key : {crypto.dump_privatekey(crypto.FILETYPE_PEM, BobA)}\n")
# print(f"Public key : {crypto.dump_publickey(crypto.FILETYPE_PEM, BobA)}\n")

# print(f"Private key : {crypto.dump_privatekey(crypto.FILETYPE_PEM, BobB)}\n")
# print(f"Public key : {crypto.dump_publickey(crypto.FILETYPE_PEM, BobB)}\n")

# self.p = int(hashlib.sha1(msg).hexdigest(), 16)
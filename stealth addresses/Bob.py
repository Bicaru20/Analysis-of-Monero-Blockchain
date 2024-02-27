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
        x = (self.__Apriv*R) + self.__Bpriv
        if P == self.generator*x:
            return True
        return False

# print(f"Private key : {crypto.dump_privatekey(crypto.FILETYPE_PEM, BobA)}\n")
# print(f"Public key : {crypto.dump_publickey(crypto.FILETYPE_PEM, BobA)}\n")

# print(f"Private key : {crypto.dump_privatekey(crypto.FILETYPE_PEM, BobB)}\n")
# print(f"Public key : {crypto.dump_publickey(crypto.FILETYPE_PEM, BobB)}\n")


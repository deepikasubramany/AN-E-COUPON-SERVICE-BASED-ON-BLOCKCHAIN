from KeyGeneration import *
class WalletContract:
    def __init__(self, walletAddress):
        self.walletAddress=walletAddress
        n,e,d=self.keyGeneration()
        self.publicKey=[e,n]
        self.privateKey=[d,n]
    def keyGeneration(self):
        modulusSize=1024
        primeSize = modulusSize // 2
        p = getRandomPrime(primeSize)
        q = getRandomPrime(primeSize)
        while p == q:
            q = getRandomPrime(primeSize)
        n, e, d = getKeys(p, q)
        return n,e,d

    def getWalletAddress(self):
        return self.walletAddress
    def getPublicKey(self):
        return self.publicKey
    def getPrivateKey(self):
        return self.privateKey
    
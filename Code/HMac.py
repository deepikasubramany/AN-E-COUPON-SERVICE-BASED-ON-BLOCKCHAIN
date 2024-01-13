import string
import base64
import Encryption
import hmac, hashlib
import time
from dbconnect import *
signaturetime = int(round(time.time() * 1000))
def verify(msg, sig):
            secret = b'1234'
            computed_sha = hmac.new(secret, msg, digestmod=hashlib.sha3_512).digest()
            if sig != computed_sha:
                return False
            else:
                return True
data=[1,1,1,1000]
E_Coupon=','.join(map(str, data))
msg=E_Coupon +"Ecoupon Purchase Record"
st = int(round(time.time() * 1000))
msg = bytes(msg, 'utf-8')
msgEncrypted = Encryption.cipher.encrypt(msg)
print("Encrypted message:\n", msgEncrypted)
et = int(round(time.time() * 1000))
elapsed_time = et - st
print('Encryption time:', elapsed_time, 'milliseconds')
st = int(round(time.time() * 1000))
secret = b'1234'
computedSig = hmac.new(secret, msg, digestmod=hashlib.sha3_512).digest()
et = int(round(time.time() * 1000))
elapsed_time = et - st
print('Signature Generation time:', elapsed_time, 'milliseconds')
senddata=msgEncrypted.decode('utf-8')+"signature"+computedSig.decode('latin-1')
print("tag of message=", computedSig)
print("length of tag of message=", len(computedSig))
print(senddata)
st = int(round(time.time() * 1000))
data=senddata.split("signature")
messageEncrypted = data[0].encode('utf-8')
message = bytes(Encryption.cipher.decrypt(messageEncrypted), encoding='utf-8')
et = int(round(time.time() * 1000))
elapsed_time = et - st
print('Decryption time:', elapsed_time, 'milliseconds')
tag = data[1].encode('latin-1')
st = int(round(time.time() * 1000))
ver=verify(message, tag)
et = int(round(time.time() * 1000))
elapsed_time = et - signaturetime
print('HMac Signature Generation time:', elapsed_time, 'milliseconds')
sql1='insert into performance(name, result) values("%s","%s")' % \
             ("HMac",elapsed_time)     
inserquery(sql1)
if verify(message, tag):
            message = message.decode('utf-8')
            

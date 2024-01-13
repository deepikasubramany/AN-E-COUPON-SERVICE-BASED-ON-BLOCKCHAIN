import rsa
from base64 import b64encode, b64decode
import time
from dbconnect import *
st = int(round(time.time() * 1000))
msg1 = bytes("E-Coupon Use!", 'utf-8')
msg2 = bytes("Not Use!", 'utf-8')
keysize = 2048


(public, private) = rsa.newkeys(keysize)
'''encrypted = b64encode(rsa.encrypt(msg1, public))
decrypted = rsa.decrypt(b64decode(encrypted), private)'''
signature = b64encode(rsa.sign(msg1, private, "SHA-512"))
verify = rsa.verify(msg1, b64decode(signature), public)

'''print(private.exportKey('PEM'))
print(public.exportKey('PEM'))
print("Encrypted: " + encrypted.decode())
print("Decrypted: '%s'" % decrypted)
print("Signature: " + signature.decode())'''
print("Verify: %s" % verify)
print(rsa.verify(msg2, b64decode(signature), public))
et = int(round(time.time() * 1000))
elapsed_time = et - st
print('Signature  VerificationTime:', elapsed_time, 'milliseconds')
sql1='insert into performance(name, result) values("%s","%s")' % \
             ("RSA",elapsed_time)     
inserquery(sql1)
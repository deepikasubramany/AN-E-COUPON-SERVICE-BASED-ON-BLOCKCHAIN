from collections import OrderedDict
import pickle
from datetime import datetime
from datetime import date
import requests
from flask import Flask, jsonify, request, render_template
import os
from flask import Flask, request, redirect, render_template, url_for, flash, get_flashed_messages
import requests, json
import json
from flask import Flask, jsonify
import datetime
from flask import session
from dbconnect import *
from KeyGeneration import *
import CreateWallet
import pickle
import time
from eCouponContract import *
import rsa
from base64 import b64encode, b64decode
import time
import string
import base64
import Encryption
import hmac, hashlib
def verify(msg, sig):
            secret = b'1234'
            computed_sha = hmac.new(secret, msg, digestmod=hashlib.sha3_512).digest()
            if sig != computed_sha:
                return False
            else:
                return True
msg1 = bytes("E-Coupon Use!", 'utf-8')
msg2 = bytes("Not Use!", 'utf-8')
keysize = 2048

(public, private) = rsa.newkeys(keysize)
class Blockchain:
        def __init__(self):
                self.chain = []
                if(os.path.exists('hyperledger.pkl')):
                        with open('hyperledger.pkl', 'rb') as f:
                                self.chain = pickle.load(f)
                else:
                        self.create_block(proof=1, previous_hash='0')
        def create_block(self, proof, previous_hash):
                block = {'index': len(self.chain) + 1,
				'timestamp': str(datetime.datetime.now()),
				'proof': proof,
				'previous_hash': previous_hash}
                self.chain.append(block)
                return block
        def print_previous_block(self):
                return self.chain[-1]
        def proof_of_work(self, previous_proof):
                new_proof = 1
                check_proof = False
                while check_proof is False:
                        hash_operation = hashlib.sha256(
				str(new_proof**2 - previous_proof**2).encode()).hexdigest()
                        if hash_operation[:5] == '00000':
                                check_proof = True
                        else:
                                new_proof += 1
                return new_proof
        def hash(self, block):
                encoded_block = json.dumps(block, sort_keys=True).encode()
                return hashlib.sha256(encoded_block).hexdigest()
        def chain_valid(self, chain):
                previous_block = chain[0]
                block_index = 1
                while block_index < len(chain):
                        block = chain[block_index]
                        if block['previous_hash'] != self.hash(previous_block):
                                return False
                        previous_proof = previous_block['proof']
                        proof = block['proof']
                        hash_operation = hashlib.sha256(
				str(proof**2 - previous_proof**2).encode()).hexdigest()
                        if hash_operation[:5] != '00000':
                                return False
                        previous_block = block
                        block_index += 1
                return True
class CouponUseContract():
        def __init__(self):
                sql='select * from ecoupon'
                result=recoredselect(sql)
                self.customer=[]
                self.couponRecord=[]
                self.couponPurchase=[]
                self.couponUseRecord =[]
                if(os.path.exists('couponUseRecord.pkl')):
                        with open('couponUseRecord.pkl', 'rb') as f:
                                self.couponUseRecord = pickle.load(f)
                
                for inde,i in enumerate(result):
                        dic1={}
                        dic1["id"]=i[0]
                        dic1["name"]=i[3]
                        dic1["couponcount"]=i[4]
                        dic1["price"]=i[5]
                        dic1["startdate"]=i[2]
                        dic1["validitydate"]=i[6]
                        dic1["counponAddress"]=i[7]
                        self.couponRecord.append(dic1)
                sql='select * from accountcreation where role="Customer"'
                result=recoredselect(sql)
                for inde,i in enumerate(result):
                        dic1={}
                        dic1["id"]=i[0]
                        dic1["walletaddress"]=i[3]
                        dic1["amount"]=i[4]
                        self.customer.append(dic1)
                sql='select * from couponaccess where status="Download"'
                result=recoredselect(sql)
                for inde,i in enumerate(result):
                        dic1={}
                        dic1["id"]=i[0]
                        dic1["uid"]=i[1]
                        dic1["counponAddress"]=i[2]
                        self.couponPurchase.append(dic1)

                
        def execContract(self, customerId, couponaddress, purchaseDetails,ProductId):
                if self.verifyCustomer(customerId) == True:
                        response = self.verifyCouponaddress(couponaddress)
                        
                        if response == False:
                                return False
                        else:
                                response = self.verifyAccessPermission(customerId,couponaddress)
                                
                                if(response==True):
                                        return self.updateRecord(customerId, purchaseDetails, couponaddress,ProductId)
                                else:
                                        return False
                else:
                        return False
        def verifyCustomer(self, customerId):
                response = False
                for each in self.customer:
                        if customerId == each['id']:
                                response = True
                                break
                return response
        def verifyCouponaddress(self, couponaddress):
                response = False
                for info in self.couponRecord:
                        if int(couponaddress) == info['id']:
                                validitydate = info['validitydate'].split("-")
                                couponcount = info['couponcount']
                                validityDateformat= datetime.datetime(int(validitydate[0]), int(validitydate[1]), int(validitydate[2]))
                                currentdate=datetime.datetime.today()
                              
                                if(int(couponcount)>0 and validityDateformat >= currentdate):
                                        response = True;
                                      
                                        break
                return response
        def verifyAccessPermission(self, customerId,couponaddress):
                response = False
                for each in self.couponPurchase:
                        if str(customerId) == each['uid']:
                                if(each['counponAddress']==str(couponaddress)):
                                        response=True
                                        break;
                return response
        def updateRecord(self,customerId, purchaseDetails, couponaddress,ProductId):
                respone=False
                data=purchaseDetails.split("signature")
                messageEncrypted = data[0].encode('utf-8')
                message = bytes(Encryption.cipher.decrypt(messageEncrypted), encoding='utf-8')
                tag = data[1].encode('latin-1')
                if verify(message, tag):
                        previous_block = blockchain.print_previous_block()
                        previous_proof = previous_block['proof']
                        proof = blockchain.proof_of_work(previous_proof)
                        previous_hash = blockchain.hash(previous_block)
                        block = blockchain.create_block(proof, previous_hash)
                        response = {'message': 'A block is MINED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
                        with open('hyperledger.pkl', 'wb') as f:
                                pickle.dump(blockchain.chain, f)
                       
                        data = response
                        
                        self.couponUseRecord.append({"CouponUserId":customerId,"purchaseProduct":ProductId, "CouponAddress":couponaddress, 'previous_hash': data['previous_hash'], 'proof': data['proof'], 'timestamp': data['timestamp']})
                        print(self.couponUseRecord)
                        with open('couponUseRecord.pkl', 'wb') as f:
                                pickle.dump(self.couponUseRecord, f)
                        respone = True
                return respone
def usecoupon(id,simulationtime):
        st = int(round(time.time() * 1000))
        ids=12
        productid=4
        couponId=id
        sql='SELECT * FROM ecoupon WHERE id="%s"'% \
                (couponId)
        discount=0
        result=recoredselect(sql)
        if(len(result)>0):
                discount=int(result[0][9])
                
        sql='select * from  accountcreation where id="%s"'   % \
             (ids)
        result=recoredselect(sql)
        print(result)
        totalamount=0
        if(len(result)>0):
                totalamount= int(result[0][8])

               
        sql='select * from  productinfo where id="%s"'   % \
             (productid)
        result=recoredselect(sql)
        
        remain=0;
        if(len(result)>0):
                price = int(result[0][3])
                dis=(discount/price)*100
                remain=price-dis
                
       
        msg="E-Coupon Use!"+str(ids)

        msg = bytes(msg, 'utf-8')
        msgEncrypted = Encryption.cipher.encrypt(msg)
        print("Encrypted message:\n", msgEncrypted)
        secret = b'1234'
        computedSig = hmac.new(secret, msg, digestmod=hashlib.sha3_512).digest()
        senddata=msgEncrypted.decode('utf-8')+"signature"+computedSig.decode('latin-1')
        cont = CouponUseContract()
        if(cont.execContract(ids, id, senddata,productid)):
                if(totalamount>=remain):
                        et = int(round(time.time() * 1000))
                        elapsed_time = et - st
                        
                        print('Contract Processing Time:', elapsed_time, 'milliseconds')
                        return elapsed_time
                       
                else:
                        et = int(round(time.time() * 1000))
                        elapsed_time = et - st
                        
                        print('Contract Processing Time:', elapsed_time, 'milliseconds')
                        return elapsed_time
        et = int(round(time.time() * 1000))
        elapsed_time = et - st
        print('Contract Processing Time:', elapsed_time, 'milliseconds')
        return elapsed_time
blockchain = Blockchain()
simtime=1
processTime=0
for i in range(simtime):
        processTime=processTime+usecoupon(6,simtime)
print(processTime)
sql1='insert into performance(name, result,simulation) values("%s","%s","%s")' % \
                        ("ContractVerificationHmac",processTime,simtime)
print(sql1)
inserquery(sql1)  
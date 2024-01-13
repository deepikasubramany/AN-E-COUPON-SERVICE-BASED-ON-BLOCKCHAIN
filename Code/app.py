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

                print(self.customer)
                print(self.couponPurchase)
        def execContract(self, customerId, couponaddress, purchaseDetails,ProductId):
                if self.verifyCustomer(customerId) == True:
                        response = self.verifyCouponaddress(couponaddress)
                        print(response)
                        if response == False:
                                return False
                        else:
                                response = self.verifyAccessPermission(customerId,couponaddress)
                                print(response)
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
                        print(data)
                        self.couponUseRecord.append({"CouponUserId":customerId,"purchaseProduct":ProductId, "CouponAddress":couponaddress, 'previous_hash': data['previous_hash'], 'proof': data['proof'], 'timestamp': data['timestamp']})
                        print(self.couponUseRecord)
                        with open('couponUseRecord.pkl', 'wb') as f:
                                pickle.dump(self.couponUseRecord, f)
                        respone = True
                return respone

class ECouponIssueContract():
        def __init__(self):
                sql='SELECT uid,MONTH(DATE) AS startdate,COUNT(uid),SUM(intialcouponcount),SUM(price) FROM ecoupon  GROUP BY uid ,startdate ORDER BY MONTH(DATE) DESC'
                result=recoredselect(sql)
                self.x=[]
                self.couponRecord=[]
                self.couponissueRecord=[]
                self.provider=[]
                if(os.path.exists('couponissueRecord.pkl')):
                        with open('couponissueRecord.pkl', 'rb') as f:
                                self.couponissueRecord = pickle.load(f)
                
                for inde,i in enumerate(result):
                        dic1={}
                        dic1["id"]=i[0]
                        dic1["month"]=i[1]
                        dic1["monthcount"]=i[2]
                        dic1["couponcount"]=i[3]
                        dic1["price"]=i[4]
                        
                        self.couponRecord.append(dic1)
                sql='select * from accountcreation where role="Provider"'
                result=recoredselect(sql)
                for inde,i in enumerate(result):
                        dic1={}
                        dic1["id"]=i[0]
                        dic1["walletaddress"]=i[3]
                        self.provider.append(dic1)
              
                print(self.provider)
                print(self.couponRecord)
              
        def execContract(self, providerId,couponDetails, ecouponContract ):
                if self.verifyCustomer(providerId) == True:
                        response = self.verifyCouponContract(providerId,ecouponContract)
                        print(response)
                        if response == True:
                              return self.updateRecord(providerId, couponDetails)
                        else:
                              return False
                else:
                        return False
        def verifyCustomer(self, providerId):
                response = False
                for each in self.provider:
                        if providerId == each['id']:
                                response = True
                                break
                return response
        def verifyCouponContract(self, providerId,ecouponContract):
                response = False
                for info in self.couponRecord:
                        if int(providerId) == info['id']:
                                
                                couponprice = int(info['price'])
                                couponcount = int(info['couponcount'])
                                monthcount = int(info['monthcount'])
                                month = int(info['month'])
                                currentMonth = datetime.datetime.now().month
                                startdateinfo=ecouponContract.getStartDate().split("-")
                                enddateinfo=ecouponContract.getExpireDate().split("-")
                                startDateformat= datetime.datetime(int(startdateinfo[0]), int(startdateinfo[1]), int(startdateinfo[2]))
                                endDateformat= datetime.datetime(int(enddateinfo[0]), int(enddateinfo[1]), int(enddateinfo[2]))
                                diff = endDateformat-startDateformat 
                                couponcurrentcount=int(ecouponContract.getTotalCoupon())
                                currentcouponprice=int(ecouponContract.getPrice())
                                datys=diff.days
                                print(currentMonth)
                                print(datys)
                                if(currentMonth==month):
                                        if(monthcount<=5 and (couponcount+couponcurrentcount)<=100 and (currentcouponprice+couponprice)<=500 ):
                                                if(datys>2 and datys<7):
                                                         response = True;
                                else:
                                        if(couponcurrentcount<=100 and currentcouponprice<=500 ):
                                                 if(datys>2 and datys<7):
                                                        response = True;

                                break;
                        else:
                                currentMonth = datetime.datetime.now().month
                                startdateinfo=ecouponContract.getStartDate().split("-")
                                enddateinfo=ecouponContract.getExpireDate().split("-")
                                startDateformat= datetime.datetime(int(startdateinfo[0]), int(startdateinfo[1]), int(startdateinfo[2]))
                                endDateformat= datetime.datetime(int(enddateinfo[0]), int(enddateinfo[1]), int(enddateinfo[2]))
                                diff = endDateformat-startDateformat 
                                couponcurrentcount=int(ecouponContract.getTotalCoupon())
                                currentcouponprice=int(ecouponContract.getPrice())
                                datys=diff.days
                                print(currentMonth)
                                print(datys)
                                if(couponcurrentcount<=100 and currentcouponprice<=500 ):
                                                 if(datys>2 and datys<7):
                                                        response = True;

                                break;

                return response
       
        def updateRecord(self,providerId, couponDetails):
                respone=False
                data=couponDetails.split("signature")
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
                        print(data)
                        self.couponissueRecord.append({"CouponUserId":providerId, 'previous_hash': data['previous_hash'], 'proof': data['proof'], 'timestamp': data['timestamp']})
                        print(self.couponissueRecord)
                        with open('couponissueRecord.pkl', 'wb') as f:
                                pickle.dump(self.couponissueRecord, f)
                        respone = True
                return respone


app = Flask(__name__)

blockchain = Blockchain()
import hashlib
def getCerificate(patientId):
        result = hashlib.sha256(patientId.encode())
        return result.hexdigest()
   
# importing the random module
import random

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/')
def home():
        sitekey = "6Lc0otYiAAAAANXmCZpohxVuCVitsYpxwgWtQ1wf"
        return render_template('./login.html',sitekey=sitekey)
@app.route('/index')
def index():
        sitekey = "6Lc0otYiAAAAANXmCZpohxVuCVitsYpxwgWtQ1wf"
        return render_template('./login.html',sitekey=sitekey)
@app.route('/register')
def register():
        sitekey = "6Lc0otYiAAAAANXmCZpohxVuCVitsYpxwgWtQ1wf"
        return render_template('./register.html',sitekey=sitekey)

@app.route('/provider')
def provider():
	return render_template('./provider.html')
@app.route('/customer')
def customer():
	return render_template('./customer.html')
@app.route('/coupon')
def coupon():
	return render_template('./coupon.html')

@app.route('/userUpgrade')
def userUpgrade():
	return render_template('./userUpgrade.html')
@app.route('/amountCredit')
def amountCredit():
	return render_template('./amountCredit.html')


@app.route('/product')
def product():
	return render_template('./product.html')
@app.route('/purchaseProduct')
def purchaseProduct():
        sql='select * from  productinfo'
        result=recoredselect(sql)
        return render_template('./purchaseProduct.html',data=result)

@app.route('/viewallproduct')
def viewallproduct():
        ids=session['id']
        sql='select * from  productinfo where uid="%s"' % \
        (ids)
        result=recoredselect(sql)
        return render_template('./viewallproduct.html',data=result)


@app.route('/accountinfo')
def accountinfo():
        ids=session['id']
        sql='select * from  accountcreation where id="%s"' % \
        (ids)
        result=recoredselect(sql)
        return render_template('./accountinfo.html',data=result)

@app.route('/ecouponinfo')
def ecouponinfo():
        ids=session['id']
        sql='select * from  ecoupon where uid="%s"' % \
        (ids)
        result=recoredselect(sql)
        return render_template('./ecouponinfo.html',data=result)

@app.route('/viewledger')
def viewledger():
        ids=session['id']
        couponUseRecord =[]
        if(os.path.exists('couponUseRecord.pkl')):
                with open('couponUseRecord.pkl', 'rb') as f:
                        couponUseRecord = pickle.load(f)
        sql='SELECT * FROM ecoupon WHERE uid="%s"'% \
                (ids)
        result2=recoredselect(sql)
        datainfo=[]
        for inde,i in enumerate(result2):
                        datainfo.append((str(i[0])))
        print(datainfo)
        return render_template('viewledger.html',data=couponUseRecord,infolist=datainfo)

@app.route('/purchasecart/<string:id>', methods=["GET", "POST"])
def purchasecart(id):
        ids=session['id']
        purchasestatus=0
        sql1='insert into carditem(uid, pid,purchasestatus) values("%s","%s","%s")' % \
             (ids,id,purchasestatus)
        print(sql1)
        inserquery(sql1)
        sql='SELECT * FROM carditem AS a INNER JOIN productinfo AS b ON a.pid=b.id where a.uid="%s" and a.purchasestatus="%s"' % \
             (ids,purchasestatus)
        result=recoredselect(sql)
        return render_template('./purchaseProductfinal.html',data=result)

@app.route('/cartitem', methods=["GET", "POST"])
def cartitem():
        ids=session['id']
        purchasestatus=0
       
        sql='SELECT * FROM carditem AS a INNER JOIN productinfo AS b ON a.pid=b.id where a.uid="%s" and a.purchasestatus="%s"' % \
             (ids,purchasestatus)
        result=recoredselect(sql)
        return render_template('./purchaseProductfinal.html',data=result)


@app.route('/userupgradedata',methods = ["GET","POST"])
def userupgradedata():
         usertype = request.form["usertype"]
         ids=session['id']
         detection=100
         message="Account upgrade Sucessfully"
         flag=True
         typeinfo=session['usertype']
         if(typeinfo=="Normal"):
                if(usertype=="Elite"):
                        detection=200
                        session['usertype']="Elite"
                else:
                        detection=100
                        session['usertype']="Premium" 
         elif(typeinfo=="Premium"):
               if(usertype=="Elite"):
                        detection=100 
                        session['usertype']="Elite" 
         else:
                flag=False
                message="Cannot be upgrade"
         if(flag==False):
                return render_template('customer.html',mess=message)

         sql1='update accountcreation set  usertype="%s" , amount=amount-"%d" where id="%s"' % \
             (usertype,detection,ids)     
         print(sql1)
         inserquery(sql1)
         message="User update amount Sucess"
         return render_template('customer.html',mess=message)

@app.route('/amountCreditdata',methods = ["GET","POST"])
def amountCreditdata():
        amount = int(request.form["amount"])
        ids=session['id']

        sql1='update accountcreation set  amount=amount+"%d"  where id="%s"' % \
             (amount,ids)     
        print(sql1)
        
        inserquery(sql1)
        message="User Upgrade Sucess"
        return render_template('customer.html',mess=message)

@app.route('/accountcreation',methods = ["GET","POST"])
def accountcreation():
        name = request.form["name"]
        sitekey = "6Lc0otYiAAAAANXmCZpohxVuCVitsYpxwgWtQ1wf" 
        email = request.form["email"]
        typeselect = request.form["role"]
        
        uname = request.form["username"]
        password = request.form["password"]
        usertype="Normal"
        amount=1000

        sql='select * from  accountcreation where username="%s" ' % \
             (uname)
        result=recoredselect(sql)
        message=None
        status=0
        captcha_response = request.form['g-recaptcha-response']
        capchaverify=False
        if is_human(captcha_response):
            capchaverify = True
        if(capchaverify):
                if(len(result)==0):
                        walletaddress=getCerificate(uname)
                        createwallet=CreateWallet.WalletContract(walletaddress)
                        fileName= "WalletContract/"+uname+".wallet"
                        with open(fileName, 'wb') as handle:
                                pickle.dump(createwallet, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        sql1='insert into accountcreation(name, email,username,password,role,walletaddress,usertype,amount) values("%s","%s","%s", "%s","%s","%s","%s","%d")' % \
                (name,email,uname,password,typeselect,walletaddress,usertype,amount)
                        print(sql1)
                        inserquery(sql1)
                        roleType="Member"
                        sql1='insert into wallet(walletaddress, wallettype,keydetails) values("%s","%s","%s")' % \
                (walletaddress,roleType,fileName)
                        print(sql1)
                        inserquery(sql1)
                        message="Account Cretion Sucessfully"
                else:
                        message="Account Already Exist"
                        
                        return render_template('./register.html',sitekey=sitekey,mess=message)
        else:
                return render_template('./register.html',sitekey=sitekey,mess="Incorrect Captcha")

                
       
     
        return render_template('login.html',mess=message,sitekey=sitekey)

def is_human(captcha_response):
    """ Validating recaptcha response from google server.
        Returns True captcha test passed for the submitted form 
        else returns False.
    """
    secret = "6Lc0otYiAAAAACUIBmbENKjCAPD-S6pvtB4Vyprw"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


@app.route('/loginverification',methods = ["GET","POST"])
def loginverification():
        
        uname = request.form["username"]
        sitekey = "6Lc0otYiAAAAANXmCZpohxVuCVitsYpxwgWtQ1wf"
        password = request.form["password"]
        typeselect = request.form["role"]
        sql='select * from  accountcreation where username="%s" and role="%s" and password="%s"'   % \
             (uname,typeselect,password)
        result=recoredselect(sql)
        print(result)
        message=None
        status=0
        captcha_response = request.form['g-recaptcha-response']
        capchaverify=False
        if is_human(captcha_response):
            capchaverify = True
        if(capchaverify):
       
                if(len(result)==0 ):
                        return render_template('login.html',sitekey=sitekey,mess="User Not Exist")
                else:
                        session['id'] = result[0][0]
                        session['usertype'] = result[0][7]
                        
                        if(typeselect=="Customer"):
                                return render_template('customer.html')
                        else:
                                return render_template('provider.html') 
        else:
                return render_template('login.html',sitekey=sitekey,mess="InValid Captcha")
                         
        return render_template('register.html', mess="Invalid Account")
#coupon Isssue
import datetime;
import time;
@app.route('/ecouponissue',methods = ["GET","POST"])
def ecouponissue():
        ids=session['id']
        name = request.form["name"]
        price = request.form["price"]
        totalCoupon = request.form["totalcoupon"]
        percentage = request.form["percentage"]
        description=request.form["description"]
        startDate = request.form["startDate"]
        expireDate = request.form["expireDate"]
        ct =  time.time()
        ct=str(ct)
        walletecouponaddress=getCerificate(ct)
        createwallet=CreateWallet.WalletContract(walletecouponaddress)
        couponContract=ECouponContract(walletecouponaddress,name,price,percentage,totalCoupon,description,startDate,expireDate)
        msg="E-Coupon Issue!"+str(ids)

        msg = bytes(msg, 'utf-8')
        msgEncrypted = Encryption.cipher.encrypt(msg)
        print("Encrypted message:\n", msgEncrypted)
        secret = b'1234'
        computedSig = hmac.new(secret, msg, digestmod=hashlib.sha3_512).digest()
        senddata=msgEncrypted.decode('utf-8')+"signature"+computedSig.decode('latin-1')
        cont = ECouponIssueContract()
        if(cont.execContract(ids,senddata,couponContract)):
                fileName= "WalletContract/"+ct+".wallet"
                with open(fileName, 'wb') as handle:
                        pickle.dump(createwallet, handle, protocol=pickle.HIGHEST_PROTOCOL)
                fileNameCoupon= "CouponContract/"+ct+".wallet"
                with open(fileNameCoupon, 'wb') as handle:
                        pickle.dump(couponContract, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        
                sql1='insert into ecoupon(uid, date,name,couponcount,price,percentage,validitydate,counponAddress,contractCoupon,intialcouponcount) values("%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s")' % \
                (ids,startDate,name,totalCoupon,price,percentage,expireDate,walletecouponaddress,fileNameCoupon,totalCoupon)
                print(sql1)
                inserquery(sql1)
                roleType="Coupon"
                sql1='insert into wallet(walletaddress, wallettype,keydetails) values("%s","%s","%s")' % \
                (walletecouponaddress,roleType,fileName)
                print(sql1)
                inserquery(sql1)
                message="Coupon Contract Deployed Sucessfully"
                return render_template('provider.html',mess=message)
        message="Coupon Contract Deployment Failed"
        return render_template('provider.html',mess=message)
#product details Add
@app.route('/productinfo',methods = ["GET","POST"])
def productinfo():
        ids=session['id']
        name = request.form["name"]
        price = request.form["price"]
       
        description=request.form["description"]
        imageurl = request.files['fileimage']
        value = name+"_"+str(randint(0,90))+".jpg"
        imageurl.save("static\\product\\"+value)

        sql1='insert into productinfo(uid, pname,price,description,imageurl) values("%s","%s","%s", "%s","%s")' % \
             (ids,name,price,description,value)
        print(sql1)
        inserquery(sql1)
        
        message="Product information sucessfully added" 
        return render_template('provider.html',mess=message)

#Coupon Download
@app.route('/getCouponList',methods = ["GET","POST"])
def getCouponList():

        typeinfo=session['usertype']
        ids=session['id']
        sql='SELECT * FROM ecoupon WHERE DATE<=CAST(CURRENT_TIMESTAMP AS DATE) AND validitydate >=CAST(CURRENT_TIMESTAMP AS DATE) AND percentage<=10 AND couponcount>0 ORDER BY CAST(price AS INT) DESC'

        if(typeinfo=="Elite"):
                sql='SELECT * FROM ecoupon WHERE DATE<=CAST(CURRENT_TIMESTAMP AS DATE) AND validitydate >=CAST(CURRENT_TIMESTAMP AS DATE)  AND couponcount>0 ORDER BY CAST(percentage AS INT) DESC'
        elif(typeinfo=="Premium"):
                sql='SELECT * FROM ecoupon WHERE DATE<=CAST(CURRENT_TIMESTAMP AS DATE) AND validitydate >=CAST(CURRENT_TIMESTAMP AS DATE) AND percentage<=30 AND couponcount>0 ORDER BY CAST(price AS INT) DESC'
        result1=recoredselect(sql)
        sql='SELECT * FROM  couponaccess AS a INNER JOIN  ecoupon AS b ON a.counponAddress=b.id  WHERE b.validitydate>=CAST(CURRENT_TIMESTAMP AS DATE) AND a.uid="%s"' % \
             (ids)
        st = int(round(time.time() * 1000))
        result2=recoredselect(sql)
        datainfo=[]
        for inde,i in enumerate(result2):
                        datainfo.append(int(i[2]))
        print(datainfo)
       
        
        return render_template('couponlist.html',data=result1,infolist=datainfo)

@app.route('/download/<string:id>', methods=["GET", "POST"])
def download(id):
        ids=session['id']
        price=0
        couponaddress=0
        
        sql='SELECT * FROM ecoupon WHERE id="%s"'% \
                (id)
        result=recoredselect(sql)
        if(len(result)>0):
                price=result[0][5]
                couponaddress=result[0][8]
        amount=int(price)
        couponStatus="Download"
        sql1='update accountcreation set  amount=amount-"%d"  where id="%s"' % \
             (amount,ids)     
        print(sql1)
        infile = open(couponaddress,'rb')
        contract = pickle.load(infile)
        totalcoupon=int(contract.getTotalCoupon())
        contract.setTotalCoupon(totalcoupon-1)
        infile.close()
        with open(couponaddress, 'wb') as handle:
                 pickle.dump(contract, handle, protocol=pickle.HIGHEST_PROTOCOL)        
        inserquery(sql1)
        sql1='update ecoupon set  couponcount=couponcount-1  where id="%s"' % \
             (id)     
        print(sql1)
        inserquery(sql1)

        sql1='insert into couponaccess(uid, counponAddress,status) values("%s","%s","%s")' % \
             (ids,id,couponStatus)     
        print(sql1)
        inserquery(sql1)
        return render_template('customer.html',mess="Coupon Download Sucessfully")

#Coupon Use:
@app.route('/couponuse/<string:id>',methods = ["GET","POST"])
def couponuse(id):
        ids=session['id']
        sql='SELECT * FROM carditem WHERE id="%s"'% \
                (id)
        pid=0
        result=recoredselect(sql)
        if(len(result)>0):
                pid=int(result[0][2])
        
        session['couponuseproductId'] = pid
        session['couponuseproductcartId'] = id

        couponStatus="Download"
        sql='SELECT * FROM  couponaccess AS a INNER JOIN  ecoupon AS b ON a.counponAddress=b.id  WHERE a.status="Download" AND b.validitydate>=CAST(CURRENT_TIMESTAMP AS DATE) AND a.uid="%s"' % \
             (ids)
        result=recoredselect(sql)
       
        return render_template('couponuse.html',data=result)

@app.route('/usecoupon/<string:id>',methods = ["GET","POST"])
def usecoupon(id):
        st = int(round(time.time() * 1000))
        ids=session['id']
        productid=session['couponuseproductId']
        cartid=session['couponuseproductcartId']
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
        print(result)
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
                        sql1='update accountcreation set   amount="%d" where id="%s"' % \
                        (remain,ids)   
                        inserquery(sql1)
                        sql1='update carditem set purchasestatus=1 where id="%s"' % \
                        (cartid)   
                        inserquery(sql1)
                        sql1='update couponaccess set status="Purchase" where uid="%s" and counponAddress="%s"' % \
                        (ids,couponId)   
                        inserquery(sql1)
                        et = int(round(time.time() * 1000))
                        elapsed_time = et - st
                        sql1='insert into performance(name, result) values("%s","%s")' % \
                        ("ContractVerificationHmac",elapsed_time)
                        inserquery(sql1)  
                        print('Contract Processing Time:', elapsed_time, 'milliseconds')
                        return render_template('customer.html',data="Sucessfully purchased : Processing Time"+str(elapsed_time)+"milliseconds")
                else:
                        et = int(round(time.time() * 1000))
                        elapsed_time = et - st
                        sql1='insert into performance(name, result) values("%s","%s")' % \
                        ("ContractVerificationHmac",elapsed_time)
                        inserquery(sql1)
                        print('Contract Processing Time:', elapsed_time, 'milliseconds')
                        return render_template('customer.html',data="Insufficient Balance Need paid Amount: "+str(remain))
        et = int(round(time.time() * 1000))
        elapsed_time = et - st
        print('Contract Processing Time:', elapsed_time, 'milliseconds')
        return render_template('customer.html',data="Purchase Contract Failed : Processing Time"+str(elapsed_time)+"milliseconds")


@app.route('/getCouponDownloadList',methods = ["GET","POST"])
def getCouponDownloadList():
        ids=session['id']
        couponStatus="Download"
        sql='SELECT * FROM  couponaccess AS a INNER JOIN  ecoupon AS b ON a.counponAddress=b.id  WHERE a.status="Download" AND b.validitydate>=CAST(CURRENT_TIMESTAMP AS DATE) AND a.uid="%s"' % \
             (ids)
        result=recoredselect(sql)
        return render_template('couponDownloadlist.html',data=result)

@app.route('/giftCoupon/<string:id>', methods=["GET", "POST"])
def giftCoupon(id):
        session['giftcouponId'] = id
        sql='select * from  couponaccess where id="%s"'   % \
             (id)
        result=recoredselect(sql)
        print(result)
        if(len(result)>0):
               session['giftcouponaddressId'] = result[0][2]
        
        return render_template('gift.html')

@app.route('/gift',methods = ["GET","POST"])
def gift():
        ids=session['id']
        giftuid = request.form["name"]
        giftcoupon=session['giftcouponId']
        giftcouponaddressId=session['giftcouponaddressId']
        couponStatus="Download"
        sql='select * from  accountcreation where walletaddress="%s"'   % \
             (giftuid)
        result=recoredselect(sql)
        print(result)
        message=None
        status=0
        if(len(result)==0):
                message="Wallet Address Not Exist"
                return render_template('customer.html',mess=message)
        else:
                giftuid = result[0][0]

        sql1='insert into couponaccess(uid, counponAddress,status) values("%s","%s","%s")' % \
             (giftuid,giftcouponaddressId,couponStatus)     
        print(sql1)
        couponStatus="Gift"
        inserquery(sql1)
        sql1='update couponaccess set  giftAddress="%s",status="%s"  where id="%s"' % \
             (giftuid,couponStatus,giftcoupon)     
        print(sql1)
        
        inserquery(sql1)
        message="Coupon Gifted to User"
        return render_template('customer.html',mess=message)
if __name__ == '__main__':
       app.debug = True
       app.run()

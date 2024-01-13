class ECouponContract:
    def __init__(self, walletAddress,couponName,price,percentage,totalCoupon,description,startDate,expireDate):
        self.walletAddress=walletAddress
        self.couponName=couponName
        self.price=price
        self.totalCoupon=totalCoupon
        self.percentage=percentage
        self.description=description
        self.startDate=startDate
        self.expireDate=expireDate
 
    def getWalletAddress(self):
        return self.walletAddress
    def getCouponName(self):
        return self.couponName
    def getPrice(self):
        return self.price
    def getTotalCoupon(self):
        return self.totalCoupon
    def getDescription(self):
        return self.description
    def getStartDate(self):
        return self.startDate
    def getExpireDate(self):
        return self.expireDate
    def getPercentage(self):
        return self.percentage
    def setTotalCoupon(self,couponCount):
        self.totalCoupon=couponCount
    

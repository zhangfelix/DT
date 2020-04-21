import tqsdk
from config_se import simAccoutName,simAccoutPassWord
api = tqsdk.TqApi(tqsdk.TqAccount("快期模拟",simAccoutName,simAccoutPassWord))
print("账户资金：/n")
print(api.get_account())
api.close()
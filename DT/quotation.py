"""
todo
"""
import sys
from tqsdk import TqApi, TargetPosTask, TqAccount
from tqsdk.tafunc import ma
from tqsdk import BacktestFinished
from datetime import date, datetime
from tqsdk import TqApi, TqSim, TqBacktest
from config_se import config_se
from strategy import Strategy

def main(argv=None):
    """
    测试脚本内容
    """
    if argv is None:
        argv = sys.argv
    # acc = TqAccount("快期模拟", config_se['simAccoutName'], \
    #     config_se['simAccoutName'])
    acc = TqSim()
    api = TqApi(acc)

    # try:
        # 执行策略方法
    kline = api.get_kline_serial("SHFE.cu1903", 7*24*60*60)
    for i in range(200):
        kline.iloc[i, 0] = datetime.fromtimestamp(kline.iloc[i, 0]/1000000000)

    print(kline.iloc[-20:-1,:])
        # Strategy(api, "xxx").aberration()
    api.close()
    # except BacktestFinished:
    #     print(acc.trade_log)

if  __name__ == "__main__":
    # sys.exit(main())
    main()

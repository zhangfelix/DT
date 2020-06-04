"""
todo
"""
import sys
from tqsdk import TqApi, TargetPosTask, TqAccount
from tqsdk.tafunc import ma
from tqsdk import BacktestFinished
from datetime import date
from tqsdk import TqApi, TqSim, TqBacktest
from config_se import config_se
from aberration import aberration

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

    try:
        # 执行策略方法
        aberration(api, "xxx")
        api.close()
    except BacktestFinished:
        print(acc.trade_log)
if  __name__ == "__main__":
    sys.exit(main())

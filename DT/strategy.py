'''
策略函数
'''
from tqsdk import TqApi, TargetPosTask
from tqsdk.ta import BOLL, ATR, MA

HOUR = 60*60
DAY = 24*HOUR
WEEK = 7*DAY
class Strategy():
    '''
    策略类，用于存储各种策略方法
    '''
    def __init__(self, api=TqApi(), symbol=None):
        self.api = api
        self.symbol = symbol
    def jesse_livermore(self):
        '''
        杰西·利弗莫尔策略
        '''
        pass
    def trend_line(self, kline_level="day", atr_n=14, MA_n=40):
        '''
        趋势线策略
        '''
        # profit_space_switch = {
        #     "day":lambda n: ATR(self.api.get_kline_serial(self.symbol, 60*60*24), n),
        #     "hour":lambda n: ATR(self.api.get_kline_serial(self.symbol, 60*60), n)
        # }
        # loss_space_switch = {
        #     "day":lambda n: ATR(self.api.get_kline_serial(self.symbol, 60*60), n),
        #     "hour":lambda n: ATR(self.api.get_kline_serial(self.symbol, 5*60), n)
        # }
        # loss_space = loss_space_switch[self.kline_level](atr_n)
        # profit_space = profit_space_switch[self.kline_level](atr_n)
        trend = 0 # 1 上升趋势，0 震荡， -1 下降趋势
        quote = self.api.get_quote(self.symbol)
        target = TargetPosTask(self.api, self.symbol)

        if kline_level == "day":
            loss_atr_period = 60*60
            profit_atr_period = 24*60*60
            trend_period = 24*60*60
            trend_kline = self.api.get_kline_serial(self.symbol, trend_period)
        elif kline_level == "week":
            loss_atr_period = 60*60
            profit_atr_period = 7*24*60*60
            trend_period = 24*60*60

        loss_space = ATR(self.api.get_kline_serial(self.symbol, loss_atr_period), atr_n)
        profit_space = ATR(self.api.get_kline_serial(self.symbol, profit_atr_period), atr_n)
        if trend_kline.iloc[-1].close > MA(trend_kline, 40).iloc[-1]+2*ATR(trend_kline, atr_n):
            trend = 1
        while True:
            pass



    def aberration(self):
        '''
        Aberration策略 (难度：初级)
        参考: https://www.shinnytech.com/blog/aberration/
        注: 该示例策略仅用于功能示范, 实盘时请根据自己的策略/经验进行修改
        '''
        # 获取合约信息
        api = self.api
        symbol = self.symbol
        quote = api.get_quote(symbol)
        klines = api.get_kline_serial(symbol, 60 * 60 * 24)
        position = api.get_position(symbol)
        target_pos = TargetPosTask(api, symbol)
        # 使用BOLL指标计算中轨、上轨和下轨，其中26为周期N  ，2为参数p
        def boll_line(klines):
            boll = BOLL(klines, 26, 2)
            midline = boll["mid"].iloc[-1]
            topline = boll["top"].iloc[-1]
            bottomline = boll["bottom"].iloc[-1]
            print("策略运行，中轨：%.2f，上轨为:%.2f，下轨为:%.2f" % (midline, topline, bottomline))
            return midline, topline, bottomline
        midline, topline, bottomline = boll_line(klines)
        while True:
            api.wait_update()
            # 每次生成新的K线时重新计算BOLL指标
            if api.is_changing(klines.iloc[-1], "datetime"):
                midline, topline, bottomline = boll_line(klines)
            # 每次最新价发生变化时进行判断
            if api.is_changing(quote, "last_price"):
                # 判断开仓条件
                if position.pos_long == 0 and position.pos_short == 0:
                    # 如果最新价大于上轨，K线上穿上轨，开多仓
                    if quote.last_price > topline:
                        print("K线上穿上轨，开多仓")
                        target_pos.set_target_volume(20)
                    # 如果最新价小于轨，K线下穿下轨，开空仓
                    elif quote.last_price < bottomline:
                        print("K线下穿下轨，开空仓")
                        target_pos.set_target_volume(-20)
                    else:
                        print("当前最新价%.2f,未穿上轨或下轨，不开仓" % quote.last_price)
                # 在多头情况下，空仓条件
                elif position.pos_long > 0:
                    # 如果最新价低于中线，多头清仓离场
                    if quote.last_price < midline:
                        print("最新价低于中线，多头清仓离场")
                        target_pos.set_target_volume(0)
                    else:
                        print("当前多仓，未穿越中线，仓位无变化")
                # 在空头情况下，空仓条件
                elif position.pos_short > 0:
                    # 如果最新价高于中线，空头清仓离场
                    if quote.last_price > midline:
                        print("最新价高于中线，空头清仓离场")
                        target_pos.set_target_volume(0)
                    else:
                        print("当前空仓，未穿越中线，仓位无变化")

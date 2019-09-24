# -*- coding：utf-8 -*-
# @Time  : 2019/8/27 10:05
# @Author: huzongquan
# @File  : 测试项目.py
# @Describe :this is describe

class NewAbi(object):
    def __init__(self):
        super().__init__()
        accesskey = getApikey(keyname=MXC_PLG_USDT_AK)
        secretkey = getApikey(keyname=MXC_PLG_USDT_SK)
        accesskey2 = getApikey(keyname='')
        secretkey2 = getApikey(keyname='')
        #
        self.market = Mxc(accesskey, secretkey)
        # 对冲 gate
        self.mirror_market = Okex(accesskey2, secretkey2)
        self.id = 'mxc-plg-usdt'
        self.name = 'mxc-plg-usdt'
        self.enable = True  # 运行/停止，默认为true
        self.symbol_con = PLG  # 目标币种，如plg
        self.anchor_con = USDT  # 锚定币种，如usdt
        self.enable_disb_asks = True  # 是否允许布卖单 深度，默认是
        self.enable_disb_bids = True  # 是否允许布买单 深度 默认是
        self.disb_level = 15  # 布单深度，默认10
        self.disb_min_amount = 1900  # 50  # 布单，单个档位最小下单数量 50
        self.disb_max_amount = 2100  # 80  # 布单，单个档位最大下单数量 100
        self.disb_outside = 20  # 布单起始点，默认盘口5%之外
        self.disb_step = 1  # 布单的间距，默认依次递减或递进1%

        # ------------布单补丁相关--------------------
        self.patch_ask_start = None  # 插入卖单，价格起始点
        self.patch_ask_end = None  # 插入卖单，价格结束点
        self.patch_bid_start = None  # 插入买单，价格结束点
        self.patch_bid_end = None  # 插入买单，价格结束点
        self.patch_distance = 15  # 补丁的安全距离，小于此范围自动撤单
        self.patch_interval = 1  # 插单的间隔，默认为1%
        # --------------对冲相关------------------
        self.index_copy_start = 2  # 复制起始点
        self.index_copy_end = 12  # 复制结束点
        self.min_copy_amount = 500  # 复制数量下限
        self.max_copy_amount = 5000  # 复制数量上线
        self.ratio_copy = 0.3  # 复制比例，默认30%进行复制深度
        self.default_hold = None  # 初始化底仓之和
        self.hedge_offset = 10000  # 触发对冲的底仓变化阀值
        self.old_dis_buff = []  # 上一次布单的列表
        self.new_dis_buff = []  # 本次布单的列表
        # --------刷量相关--------------#
        self.enable_mm = True
        self.mm_prob_ask = 0.3  # 主卖概率，如0.5(需要与主买概率和为1)
        self.mm_prob_bid = 0.7  # 主买概率,如0.5,(需要与主卖概率和为1)
        self.mm_cycle = 20  # 平均自成交的基本周期（秒）
        self.mm_min_amount = 0  # 自动成交 数额最小值
        self.mm_max_amount = 0  # 自动成交 数额最大值
        self.mm_min_limit = 8  # 自动成交usdt数额最小值
        self.mm_max_limit = 20  # 自动成交 usdt数额最大值
        self.mm_algorithm = 8  # K线算法，默认为8
        self.mm_night = 1  # 夜晚成交量占比，默认为白天的1/10
        self.precision = 0.000001  # 档位的精度（一般无需更改）
        self.digits = int(math.fabs(math.log10(self.precision)))  # 精度 位数（由档位进度决定，无需设置）
        # ---------------其他参数，非公开-------------
        self.log_head = f'[{self.market.NAME}:{self.symbol_con.upper()}_{self.anchor_con.upper()}]'
        self.last_price = None


    def _run_cancel(self):
        if not self.enable: return
        print('this is _run_cancel')
        my_orders = self.market.get_all_order(self.symbol_con, self.anchor_con, side="all")
        if not my_orders: return
        if len(my_orders) > 4 * self.disb_level:
            self.market.cancel_all(self.symbol_con, self.anchor_con)
        current_depth = self.market.get_depth(self.symbol_con, self.anchor_con, precision=self.precision)
        if not current_depth: return
        if not current_depth.asks: return
        if not current_depth.bids: return
        # 卖一价格
        ask_1_price = float(current_depth.asks[0].get('price'))
        # 买一价格
        bid_1_price = float(current_depth.bids[0].get('price'))
        need_cancel_ids = []
        for order in my_orders:
            # 超过控制边界 大于最大卖
            # if order.side == 'ask' and float(order.price) >= vask_last_price:
            #     result.append(order.oid)
            # 把卖一上的单子册掉
            if order.side == 'ask' and float(order.price) < ask_1_price * (1 + self.disb_outside * 0.01):
                need_cancel_ids.append(order.oid)
            # 不作买一
            if order.side == 'bid' and float(order.price) > bid_1_price * (1 - self.disb_outside * 0.01):
                need_cancel_ids.append(order.oid)
            # 超过买单边界，太小了
            # if order.side == 'bid' and float(order.price) <= vbid_last_price:
            #     result.append(order.oid)
            # 布单补丁的删除逻辑，不为空 且 价格在预定范围之内，且 价格已经超过安全范围，那么删除
            if self.patch_ask_start and self.patch_ask_end and order.side == 'ask' and (
                    self.patch_ask_start < float(order.price) < self.patch_ask_end):
                if float(order.price) < ask_1_price * (1 + self.patch_distance * 0.01):
                    need_cancel_ids.append(order.oid)
            if self.patch_bid_start and self.patch_bid_end and order.side == 'bid' and (
                    self.patch_bid_start < float(order.price) < self.patch_bid_end):
                if float(order.price) < bid_1_price * (1 - self.patch_distance * 0.01):
                    need_cancel_ids.append(order.oid)

        for oid in set(need_cancel_ids):
            if not oid: continue
            cano = self.market.cancel_order(self.symbol_con, self.anchor_con, oid)
            print(cano)
    def hedge(self):
        """
        对冲核心逻辑
        :return:
        """
        print('hedge~~')
        # print("对冲卖出价格{} 对冲买入价格：{}".format(best_bid, best_ask))
        balance = self.market.get_assets(self.symbol_con)
        if not balance: return
        # 当前的底仓token
        current_hold = float(balance[0]['total'])
        # 把启动时候的底仓作为默认底仓
        if not self.default_hold:
            self.default_hold = current_hold
            return
        # 当前资产偏差
        current_offset = current_hold - self.default_hold
        # 偏差是否超过阀值
        flag = abs(current_offset) >= self.hedge_offset
        print(f'{self.log_head}余额偏差= {current_offset} 是否对冲:{flag}')
        # 如果超过阀值，开始对冲
        if not flag: return
        # 对冲前撤销镜像交易所订单
        self.mirror_market.cancel_all(self.symbol_con, self.anchor_con)
        # 获取镜像交易所深度数据
        source_depth = self.mirror_market.get_depth(self.symbol_con, self.anchor_con, precision=self.precision)
        if not source_depth: return
        if not source_depth.asks: return
        if not source_depth.bids: return
        if source_depth is None: return
        print(source_depth.asks[0])
        print(source_depth.bids[0])
        # 将盘口价格作为对冲价格
        best_bid = round(float(source_depth.bids[0].get('price')), 6)
        best_ask = round(float(source_depth.asks[0].get('price')), 6)
        # 对冲数量（记得取绝对值）
        order_amount = round(abs(current_offset), 2)

        if current_offset > 0:
            # token余额变多了，卖出订单
            print('hedge sell,', best_bid, order_amount)

            result = self.mirror_market.sell(symbol=self.symbol_con, anchor=self.anchor_con,
                                             price=float_to_str(best_bid),
                                             amount=float_to_str(order_amount))
            log.info(
                f'{self.log_head}  当前底仓{current_hold} 默认底仓{self.default_hold} 对冲卖出订单{best_bid} {order_amount} {result}')
            if result and result.success:
                # 如果对冲成功，那么当前的底仓成为默认底仓
                self.default_hold = current_hold
        else:
            # 余额变少了，买入订单
            print('hedge buy,', best_ask, order_amount)
            result = self.mirror_market.buy(symbol=self.symbol_con, anchor=self.anchor_con,
                                            price=float_to_str(best_ask),
                                            amount=float_to_str(order_amount))
            log.info(
                f'{self.log_head} 当前底仓{current_hold} 默认底仓{self.default_hold} 对冲买入订单{best_ask} {order_amount} {result}')
            if result and result.success:
                # 如果对冲成功，那么当前的底仓成为默认底仓
                self.default_hold = current_hold
    def copy_other_deepth(self):
        """
        复制其他交易所的深度数据
        :return:
        """
        print('copy_other_deepth～～～')
        if not self.enable: return
        depth = self.mirror_market.get_depth(self.symbol_con, self.anchor_con, precision=self.precision)
        # print(depth)
        if not depth: return
        if not depth.asks: return
        if not depth.bids: return
        # 核心算法-深度复制包含精度合并
        target_asks, target_bids = copy_depth(depth=depth, digits=self.digits,
                                              index_copy_start=self.index_copy_start,
                                              index_copy_end=self.index_copy_end,
                                              ratio_copy=self.ratio_copy,
                                              min_copy_amount=self.min_copy_amount,
                                              max_copy_amount=self.max_copy_amount,
                                              amount_digest=2)
        print('target_asks', target_asks)
        print('target_bids', target_bids)
        # 每次布单前，把new buff清空
        self.new_dis_buff.clear()
        # 进行挂单
        if self.enable_disb_asks:
            self._handle_create_orders(target_asks, side='ask')
        if self.enable_disb_bids:
            self._handle_create_orders(target_bids, side='bid')
        print('new buff', self.new_dis_buff)
        print('old buff', self.old_dis_buff)
        #   每次布单完成后，先把上一次的布单列表清除掉，实际清除
        # can = self.market.cancel_multi(self.symbol_con, self.anchor_con, self.old_dis_buff)
        # print(f'can multi={can}')
        for oid in self.old_dis_buff:
            c = self.market.cancel_order(self.symbol_con, self.anchor_con, str(oid))
            time.sleep(0.1)
            print(f'cancel {c}')
        #   再手动清空old buff
        self.old_dis_buff.clear()
        #     将手动本次新的布单ids 转移到old buff,并清空new buff,注意赋值 拷贝！！！傻逼python
        self.old_dis_buff = self.new_dis_buff.copy()
        self.new_dis_buff.clear()
        # print('new buff end', self.new_dis_buff)
        # print('old buff end ', self.old_dis_buff)
    def _handle_create_orders(self, orders: list, side, need_appen_to_buff=True):
        """

        :param orders: 准备下单的列表，包含{'price':1.0001,'amount':9.1212}
        :param side:  方向，只有 ask 和bid两种
        :param need_appen_to_buff: 是否加入枪毙名单，默认下正常布单需要加入，补丁不加入
        """
        assert side in ("ask", "bid"), "Invalid side"
        for o in orders:
            if not o:
                continue
            if side == "ask":
                # 卖出订单

                result = self.market.sell(symbol=self.symbol_con, anchor=self.anchor_con,
                                          price=float_to_str(o.get('price')),
                                          amount=float_to_str(o.get('amount')))
                print(f"sell {o.get('price')} {o.get('amount')} {result}")
                if result and result.success and need_appen_to_buff:
                    self.new_dis_buff.append(result.data)
                # print(result)
            else:
                # 买入订单
                # print('buy,', str(o.get('price')), o.get('amount'))
                result = self.market.buy(symbol=self.symbol_con, anchor=self.anchor_con,
                                         price=float_to_str(o.get('price')),
                                         amount=float_to_str(o.get('amount')))
                print(f"buy {o.get('price')} {o.get('amount')} {result}")
                if result and result.success and need_appen_to_buff:
                    self.new_dis_buff.append(result.data)


    def _run_mkline(self):
        """
        刷量任务
        :return:
        """
        if not self.enable or not self.enable_mm: return
        print('MAKE LINE run~~~~~')
        # 获取当前深度
        current_depth = self.market.get_depth(symbol=self.symbol_con, anchor=self.anchor_con,
                                              precision=self.precision)
        print('current depth {}'.format(current_depth is None))
        if not current_depth or not current_depth.asks or not current_depth.bids:
            return
        # 买卖一价格
        p_a = float(current_depth.asks[0].get('price'))
        p_b = float(current_depth.bids[0].get('price'))
        # 刷量核心算法，计算下单价格
        target = mka.make_line_8(p_a, p_b, digits=self.digits, cycle=1, min_space=3, suf=0.001,
                                 last_price=self.last_price)
        print('target', target)
        if target < 0:
            return
        self.last_price = target
        auto_order_price = target
        # 计算下单数量
        min_a = self.mm_min_amount
        max_a = self.mm_max_amount
        if self.mm_min_limit != 0 and self.mm_max_limit != 0:
            min_a = round(self.mm_min_limit / auto_order_price, 2)
            max_a = round(self.mm_max_limit / auto_order_price, 2)
        amount_auto = mka.get_auto_amount2(min_a, max_a, digits=1, night=self.mm_night)
        # flag:主买还是主卖
        flag = np.random.choice([True, False], p=[self.mm_prob_bid, self.mm_prob_ask])  ##蜜汁bug？？？？
        if IS_DEBUG:
            print('price={} amount={}'.format(float_to_str(auto_order_price), float_to_str(amount_auto)))
            return
        log.info(f'{self.log_head}盘口:ask1={p_a} bid1={p_b},目标价格={auto_order_price},目标数量={amount_auto}')
        # 下单，划K线
        if flag:
            result_auto_sell = self.market.sell(symbol=self.symbol_con, anchor=self.anchor_con,
                                                price=float_to_str(auto_order_price),
                                                amount=float_to_str(amount_auto))
            log.info(f'{self.log_head} 卖出 价格{auto_order_price} 数量:{amount_auto} 状态：{result_auto_sell}')
            if result_auto_sell and result_auto_sell.success:
                result_auto_buy = self.market.buy(symbol=self.symbol_con, anchor=self.anchor_con,
                                                  price=float_to_str(auto_order_price),
                                                  amount=float_to_str(amount_auto))
                log.info(f'{self.log_head} 买入 价格{auto_order_price} 数量:{amount_auto} 状态：{result_auto_buy}')
                if (not result_auto_buy) or (not result_auto_buy.success):
                    time.sleep(0.1)
                    self.market.cancel_order(self.symbol_con, self.anchor_con, result_auto_sell.data)

        else:
            result_auto_buy = self.market.buy(symbol=self.symbol_con, anchor=self.anchor_con,
                                              price=float_to_str(auto_order_price),
                                              amount=float_to_str(amount_auto))
            log.info(f'{self.log_head} 买入 价格{auto_order_price} 数量:{amount_auto} 状态：{result_auto_buy}')
            if result_auto_buy and result_auto_buy.success:
                result_auto_sell = self.market.sell(symbol=self.symbol_con, anchor=self.anchor_con,
                                                    price=float_to_str(auto_order_price),
                                                    amount=float_to_str(amount_auto))

                log.info(f'{self.log_head}卖出 价格{auto_order_price} 数量:{amount_auto} 状态：{result_auto_sell}')
                if (not result_auto_sell) or (not result_auto_sell.success):
                    time.sleep(0.1)
                    self.market.cancel_order(self.symbol_con, self.anchor_con, result_auto_buy.data)
    def _run_distri(self):
        if not self.enable: return
        if (not self.enable_disb_asks) and (not self.enable_disb_bids): return
        print('this is mkling _run_distri～～')
        current_depth = self.market.get_depth(self.symbol_con, self.anchor_con, precision=self.precision)
        if not current_depth: return
        if not current_depth.asks: return
        if not current_depth.bids: return
        # 卖一价格
        ask_1_price = float(current_depth.asks[0].get('price'))
        # 买一价格
        bid_1_price = float(current_depth.bids[0].get('price'))
        print('ask1={},bid1={}'.format(ask_1_price, bid_1_price))
        print(ask_1_price, bid_1_price)
        # 构建虚拟订单深度,根据卖一和买一价格
        conf_ask = {'side': 'asks',
                    'level': self.disb_level,
                    'precision': self.precision,
                    'min_amount': self.disb_min_amount,
                    'max_amount': self.disb_max_amount,
                    'outside': self.disb_outside,
                    'step': self.disb_step,
                    'min_digist': 1
                    }
        conf_bid = {'side': 'bids',
                    'level': self.disb_level,
                    'precision': self.precision,
                    'min_amount': self.disb_min_amount,
                    'max_amount': self.disb_max_amount,
                    'outside': self.disb_outside,
                    'step': self.disb_step,
                    'min_digist': 1
                    }

        virtual_depth_asks = creat_virtual_depth(current_depth.asks, **conf_ask)
        virtual_depth_bids = creat_virtual_depth(current_depth.bids, **conf_bid)
        target_asks = virtual_depth_asks
        target_bids = virtual_depth_bids
        print('target-ask=', target_asks)
        print('target-bid=', target_bids)

        if IS_DEBUG: return
        # 清空新容器，准备填充新的布单id
        self.new_dis_buff.clear()
        #  批量 创建下单-构建深度 ，并
        if self.enable_disb_asks:
            self._handle_create_orders(target_asks, side='ask')
        if self.enable_disb_bids:
            self._handle_create_orders(target_bids, side='bid')
        # 每次布单完成后，先把上一次的布单进行物理清除
        for oid in self.old_dis_buff:
            c = self.market.cancel_order(self.symbol_con, self.anchor_con, str(oid))
            time.sleep(0.05)  # 奇怪的撤单限制
            print(f'clear old order {c} {oid}')
        # 再手动清空old buff
        self.old_dis_buff.clear()
        # 将手动本次新的布单ids 转移到old buff,并清空new buff，注意拷贝
        # self.old_dis_buff = self.new_dis_buff.copy()
        self.old_dis_buff = copy.copy(self.new_dis_buff)
        self.new_dis_buff.clear()

    def run(self):
        # 初始化清空所有订单
        print(f'{self.log_head} Hello Bug~')
        schedule.every(6).seconds.do(self._run_cancel)
        # 自成交任务
        schedule.every(self.mm_cycle).to(self.mm_cycle + 10).seconds.do(self._run_mkline)
        # 对冲任务
        schedule.every(5).seconds.do(self.hedge)
        # 深度复制任务
        schedule.every(61).seconds.do(self.copy_other_deepth)
        schedule.every(41).seconds.do(self._run_distri)
        while True:
            schedule.run_pending()
            time.sleep(0.1)
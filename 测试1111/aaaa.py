# -*- coding：utf-8 -*-
# @Time  : 2019/9/20 16:49
# @Author: huzongquan
# @File  : aaaa.py
# @Describe :this is describe
import time


def firstblood(self):
    print(f'开始打点.....')
    flag = True
    while flag:
        s = self.market.sell(self.symbol_con, self.anchor_con, price='0.01', amount='10')
        b = self.market.buy(self.symbol_con, self.anchor_con, price='0.01', amount='10')
        if s and s.success and b and b.success:
            flag = False
            print('打点结束，开始压单......')
            while True:
                s = self.market.sell(self.symbol_con, self.anchor_con, price='0.03', amount='1700000')
                m = self.market.sell(self.symbol_con, self.anchor_con, price='0.04', amount='2500000')
                if s and s.success and m and m.success:
                    print(f'压单成功......')
                    break
                time.sleep(0.5)
            break
        time.sleep(0.1)

def test1():
    flag = True
    while flag:
        s = 10
        b = 20
        print(111)
        time.sleep(1)
        if s == 10 and b == 20 :
            s = 7
            b =1
            # flag = False
            while True:

                print(333)
                time.sleep(1)
                if s == 7 and b == 10:
                    print(222222)
                    break
                time.sleep(1)

            break

    print(flag)
# test1()
class tess:
    def __init__(self):
        self.a = 1
    def make(self):
        self.a = 2
        for i in range(10):
            print(i)
            time.sleep(1)
            if i == 8:
                break

        return False
    def show(self):
        print(self.a)
if __name__ == '__main__':
    a = tess()
    s = a.make()
    if s == False:
     a.show()

# -*- coding：utf-8 -*-
# @Time  : 2019/10/9 16:16
# @Author: huzongquan
# @File  : matplotlib_test.py
# @Describe :this is describe
import time

import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

x = np.arange(15)

y = np.random.randint(10, 15, size=15)

y[6] = 30

# plt.plot(x, y)
# plt.show()

import math
# print(math.pi / 3600)

hour = time.localtime().tm_hour
mini = time.localtime().tm_min
seco = time.localtime().tm_sec
t = 3600 * hour + 60 * mini + seco
print(t)
x = (0.5 * math.sin(t * math.pi / 3600) + 0.5) / 1
plt.plot(t,x)
plt.show()
# print((t * math.pi / 3600 + seco))

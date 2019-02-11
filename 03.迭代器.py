"""
迭代
    迭代是重复反馈过程的活动，其目的通常是为了逼近所需目标或结果。
    每一次对过程的重复称为一次“迭代”，而每一次迭代得到的结果会作为下一次迭代的初始值。
可迭代对象
    能用for循环遍历的都是可迭代对象
    可以使用isinstance(obj, Iterable)检测
p
"""
from collections import Iterable, Iterator

list00 = [1, 2, 3]
tuple00 = (1, 2, 3)
set00 = {1, 2, 3}
dict00 = {1: 1, 2: 2, 3: 3}
str00 = "123"
int00 = 123
bool00 = True
com00 = 123 + 45j
generator00 = (x for x in range(10))
float00 = 1.1

print(isinstance(list00, Iterable))
print(isinstance(tuple00, Iterable))
print(isinstance(set00, Iterable))
print(isinstance(dict00, Iterable))
print(isinstance(str00, Iterable))
print(isinstance(int00, Iterable))
print(isinstance(bool00, Iterable))
print(isinstance(com00, Iterable))
print(isinstance(generator00, Iterable))
print(isinstance(float00, Iterable))

print("*" * 20)

print(isinstance(list00, Iterator))
print(isinstance(tuple00, Iterator))
print(isinstance(set00, Iterator))
print(isinstance(dict00, Iterator))
print(isinstance(str00, Iterator))
print(isinstance(int00, Iterator))
print(isinstance(bool00, Iterator))
print(isinstance(com00, Iterator))
print(isinstance(generator00, Iterator))
print(isinstance(float00, Iterator))

print("*" * 20)

list00 = iter(list00)
print(list00)
print(isinstance(list00, Iterator))
tuple00 = iter(tuple00)
print(tuple00)
print(isinstance(tuple00, Iterator))
set00 = iter(set00)
print(set00)
print(isinstance(set00, Iterator))

"""
故人西辞富士康
为学技术去蓝翔
蓝翔毕业包分配
尼玛还是富士康
"""

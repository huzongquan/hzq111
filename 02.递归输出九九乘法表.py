"""
递归 :
    在函数内部调用本函数
1、创建函数：get_result(num),必须传入一个参数
2、判断num的值，如果大于1就执行递归，
    2.1  如果等于1，就输出1 * 1 = 1
    2.2  如果不等于1，执行递归，循环输出从1到该数字的乘法
         print("%d * %d = %d" % (i, num, i * num), end="\t")
"""


def get_result(num):
    if num > 1:
        get_result(num - 1)
        for i in range(1, num + 1):
            print("%d * %d = %d" % (i, num, i * num), end="\t")
        print()
    else:
        print("1 * 1 = 1")


# get_result(9)

"""
递归计算(0 - 100)偶数累加
"""


def get_sum(num):
    if num > 0:
        result = num + get_sum(num - 2)
        return result
    else:
        return 0


# print(get_sum(100))

"""
递归遍历列表
"""
list00 = ["a", "b", "c", "d", "e", "f", "g"]


def get_item(i):
    if i > 0:
        result = list00[i] + get_item(i - 1)
        return result
    else:
        return list00[i]


print(get_item(len(list00) - 1))

"""
代码思路：
1.读取所有歌词内容，readlines()---> list
2.遍历得到的内容--》[01:48.00][00:24.00]怀著冷却了的心窝飘远方
3.想办法移除 [ ] ,得到一个列表，内容为[" ", "01:48.00","00:24.00"," ","怀著冷却了的心窝飘远方"]
4.创建字典
5.取出列表["", "01:48.00","00:24.00","","怀著冷却了的心窝飘远方"]的内容放入字典，key=时间，value=歌词
6,.排序输出
"""
# 创建流对象
file = open("海阔天空.lrc", mode="r", encoding="utf-8")

# 读取所有歌词内容
lrc_list = file.readlines()
# 创建字典，存放时间和歌词
lrc_dict = {}
# 遍历得到的内容
for lrc_item in lrc_list:
    # 分割元素，得到时间和歌词组成的列表
    lrc_item_list = lrc_item.replace("[", "").strip().split("]")
    # 遍历lrc_item_list,取出时间和歌词放入字典
    print(lrc_item_list)
    for i in range(len(lrc_item_list) - 1):
        # value=lrc_item_list[-1],其他的都当做key
        lrc_dict[lrc_item_list[i]] = lrc_item_list[-1]

# 遍历这个字典，按照key的顺序输出所有内容
for key in sorted(lrc_dict.keys()):
    print(key, ":", lrc_dict[key])
file.close()

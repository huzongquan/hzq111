class test():
    def __init__(self, *args):
        self.name = '张三'
        self.age = 0

    def test1(self):
        print(self.name, self.age)


a = test()
a.test1()

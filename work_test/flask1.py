import sys

def test1():
    print('aaaa')
def test2(params):
    print(params)
    param = dict(params)
    a = param.get("a")
    print(a)
    b = param.get("b")
    print(b)
if __name__ == '__main__':
    test1()
    params = sys.argv[1]

    test2(params)


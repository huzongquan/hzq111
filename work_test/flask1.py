import sys

def test1():
    print('aaaa')
def test2(params):
    print(params)
if __name__ == '__main__':
    test1()
    params = sys.argv[2]
    test2(params)


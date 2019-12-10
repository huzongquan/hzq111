import sys

def test1():
    print('aaaa')
def test2(params):
    print(params.get('a'))
    print(params.get('b'))

if __name__ == '__main__':
    test1()
    params = sys.argv[1]
    test2(params)


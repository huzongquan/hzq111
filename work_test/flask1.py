import sys

def test1():
    print('aaaa')
def test2(params):
    s = params.loads()
    print(s.get('a'))
if __name__ == '__main__':
    test1()
    params = sys.argv[1]
    test2(params)


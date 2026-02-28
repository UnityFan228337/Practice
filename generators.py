def squares(N):
    current = 0
    while current <= N:
        yield current**2
        current += 1


def evens(n):
    current = 0
    while current <= n:
        yield current
        current += 2

def threeandfour(n):
    current = 0
    while current <= n:
        yield current
        current += 12

def squaresfor(a, b):
    for i in range(a, b+1):
        print(i*i)
        yield i*i

def tozero(n):
    while n != 0:
        yield n
        n -= 1
    
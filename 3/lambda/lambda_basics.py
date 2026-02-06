"""

syntax
lambda arguments : expression

"""

def myfunc(n):
  return lambda a : a * n

x = lambda a : a + 10
print(x(5))


x = lambda a, b : a * b
print(x(5, 6))




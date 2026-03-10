#map(func, array) make an array of elemnts by return values
def myfunc(n):
  return len(n)

x = map(myfunc, ('apple', 'banana', 'cherry'))


#filter(func, array) if func return true, it added to the array
ages = [5, 12, 17, 18, 24, 32]

def myFunc(x):
  if x < 18:
    return False
  else:
    return True

adults = filter(myFunc, ages)

for x in adults:
  print(x)
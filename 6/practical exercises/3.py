import functools

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


from functools import reduce
import operator

numbers = [1, 2, 3, 4, 5]

# Using a lambda function
sum_of_elements = reduce(lambda x, y: x + y, numbers)
print(sum_of_elements)  # Output: 15 


#enumerate() make an array of tuples [(0, something), (1, next)]

x = ('apple', 'banana', 'cherry')
y = enumerate(x)

print(list(y))


#zip(arr1, arr2) allows iterate two arrays at the same time

a = ("John", "Charles", "Mike")
b = ("Jenny", "Christy", "Monica")

x = zip(a, b)

#use the tuple() function to display a readable version of the result:

print(list(x))
for c, d in zip(a, b):
    print(c, d)

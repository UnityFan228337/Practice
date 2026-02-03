"""
for something 



"""

#walking by the every element in the array

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)


#through string
for x in "banana":
  print(x)

#from 0 to 6(not included) 0 1 2 3 4 5
for x in range(6):
  print(x)

#from 2 to 6 2 3 4 5
for x in range(2, 6):
  print(x)

#from 2 to 30, with step 3             2 5 8 11 14 17 20 23 26 29  
for x in range(2, 30, 3):
  print(x)


#else using whem loop is end
for x in range(6):
  print(x)
else:
  print("output has finished")

#nested for in for
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for x in matrix:
  for y in x:
    print(y)

#pass - if you want do nothing
for x in range(6):
  pass



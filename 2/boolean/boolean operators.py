#arithmetic
print(10+5) # = 15 addition
print(10-5) # = 5 subbstraction
print(10*5) # = 50 multiplication
print(10/5) # = 2 division
print(10%5) # = 0 remainder after division
print(10**5) # = 100000 power
print(10//5) # = 2 division, without remainder

#assigment operators
x = 0
x += 5 # x = 5
x -= 3 # x = 2
x *= 4 # x = 8
x /= 2 # x = 4
x %= 3 # x = 1
x //= 3 # x = 0
x += 3 # x = 3
x **= 2 # x = 9



#logical
x = True
y = False
print(x and y) # True and false. Return false
print(x or y) # True or false. Return true
print(not x) # Not true. Return false


#identify
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z) # z is x, that way x is z. Return True
print(x is y) # x EQUAL y, but y is not x, and x is not y. Return false

#membership
x = ["test", "exe", "may"]
y = "may"
print(y in x) # in the array x we have the elemnt that equal y. Return true
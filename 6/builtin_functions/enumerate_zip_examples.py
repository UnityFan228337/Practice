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

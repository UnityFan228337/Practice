class MyClass1:
    a = 5
    print(a)
#print(a)#cause error because x in the CLASS and it do not in the out code


class MyClass2:
    global b
    b = 6
    print(b)
print(b) #will work because y declared GLOBAL and you can use it


c = 7
class MyClass3:
    print(c) # will work because z declared before and out of class, and it automatically become global


# class MyClass4:
#     print(d) # will not work because z delcared after
# d = 7


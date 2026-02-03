#return false
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

#return true
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#checking is correct type
x = 200
print(isinstance(x, int))
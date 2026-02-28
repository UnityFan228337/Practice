#json syntax
# {"name":"John"}
import json

x = '{"name": "John", "age": 30, "city": "New York"}'
y = json.loads(x) #make from x(json code) to dictionary

# print(f"{x} is a {type(x)}")
# print(f"{y} is a {type(y)}")


# open("jsonexample.json", "w").write(x)
# print(open("jsonexample.json", "r").read())



#print letter by letter
inp = open("C:\\Users\\Lenovo\\Desktop\\Practice\\4\\json\\jsonexample.json", "r").read()
for i in inp:
    print(i)

#print string by string
inp = open("C:\\Users\\Lenovo\\Desktop\\Practice\\4\\json\\jsonexample.json", "r").read()
x = json.loads(inp)
for keys, values in x.items():
    print(f"{keys}: {values}")
    
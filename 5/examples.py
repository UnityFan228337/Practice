import re
import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)


txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)


txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)


txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)

txt = "The rain in Spain"
x = re.sub("\s", "9", txt, 2)
print(x)

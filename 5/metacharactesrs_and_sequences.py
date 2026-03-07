import re 
x = "aaaa b bbfb 5143215 bb abb aux-test"
#[]
y = re.findall("[a-b]", x) #finding all "a"

#.
y = re.findall("aux.test", x) #finding "aux-test" with any char

#^
y = re.search("^a", x) #finding line that starts with a


#$
y = re.search("t$", x) #finding line that ends with t

#*
y = re.findall("b*", x) #finding 0 or more b

#+
y = re.findall("b+", x) #finding 1 or more b

#?
y = re.findall("b?", x) #finding 0 or 1 b

#{}
y = re.findall("b{2}", x) #finding exactly 2 b


#|
y = re.findall("a|b", x) #finding a or b

#()
y = re.findall("a(b*)", x) #finding a followed by 0 or more b, and capturing the b's


#\d
y = re.findall(r"\d*", x) #finding digits

#\w
y = re.findall(r"\w*", x) #finding word characters

#\b
y = re.findall(r"\b\w+\b", x) #finding whole words

#\s
y = re.findall(r"\s", x) #finding spaces characters


#\Z
y = re.search(r"test\Z", x) #finding line that ends with test


#\A
y = re.search(r"\Aaaaa", x) #finding line that starts with aaaa


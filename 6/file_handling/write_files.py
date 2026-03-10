file = open(r"6\test.txt", "w")#if the file doesn't exist, it will be created. If it exists, it will be overwritten.
#file = open(r"6\test.txt", "a")#if the file doesn't exist, it will be created. If it exists, new content will be added to the end of the file.
#file = open(r"6\test.txt", "r+")#if the file doesn't exist, it will be created. If it exists, you can read and write to the file.
#file = open(r"6\test.txt", "x")#if the file doesn't exist, it will be created. If it exists, an error will be raised.
file.write("Hello, World!\n")#write a string to the file. The "\n" adds a new line after the text.
file.close()

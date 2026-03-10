#types of modes:
#"r" - read (default)
#"w" - write
#"a" - append
#"r+" - read and write
#also we can specify the file type:
#"t" - text (default)
#"b" - binary (e.g., "rb" for reading binary files)

file = open(r"6\test.txt", "r")
#or
#with open(r"6\test.txt", "r") as file:
    #do something with the file

content = file.read()#return all lines like one string
#content = file.readline()#return one line at a time
#content = file.readlines()#return all lines as a list of strings


file.close()#need for optimizing memory usage and preventing data loss, especially when writing to files.

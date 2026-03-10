import shutil, os

f = open(r"6\practical exercises\forthefirst.txt", "a+")
f.write("some text \n Some text \n SOME TEXT")
print(f.read())
some_lines = ["next", "next next", "next next next"]
for i in some_lines:
    f.write(i + "\n")
os.makedirs(r"6\practical exercises\copy")
shutil.copy(r"6\practical exercises\forthefirst.txt", r"6\practical exercises\copy\forthefirst.txt")
f.close()
input("Press Enter for delete")
os.remove(r"6\practical exercises\forthefirst.txt")
shutil.rmtree(r"6\practical exercises\copy")
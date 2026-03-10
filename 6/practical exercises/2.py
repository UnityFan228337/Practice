import shutil, os

# os.makedirs(r"6\practical exercises\forsecondtask\createdincodedir")
l = os.listdir(r"6\practical exercises")
for i in l: print(i, end="\n")

extension = input()
if "." not in extension:
    extension = "." + extension
for i in l:
    if extension in i:
        print(i)

shutil.move(r"6\practical exercises\test.txt", r"6\practical exercises\forsecondtask")
shutil.copy(r"6\practical exercises\forsecondtask\test.txt", r"6\practical exercises\test.txt")
import os
import shutil

os.remove(r"6\test.txt")#delete the file

os.rmdir("myfolder")#delete the folder, but it must be empty. If it contains files or subfolders, an error will be raised.
#shutil.rmtree("myfolder")#delete the folder and all its contents, including files and subfolders. Use with caution, as it will permanently delete everything in the specified folder.

shutil.copy(r"6\test.txt", r"6\test_copy.txt")#copy the file to a new location. If the destination file already exists, it will be overwritten.
shutil.copy2(r"6\test.txt", r"6\test_copy2.txt")#copy the file to a new location, preserving metadata (e.g., file permissions, timestamps). If the destination file already exists, it will be overwritten.
shutil.copytree("myfolder", "myfolder_copy")#copy the entire folder and its contents to a new location. If the destination folder already exists, an error will be raised.

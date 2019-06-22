import os
import sys

input_path = sys.argv[1]

i = 0
for dir_path, subdir_list, file_list in os.walk(input_path):
    for fname in file_list:
        full_path = os.path.join(dir_path, fname)
        os.rename(full_path, dir_path + str(i) + '.png')
        i += 1

# python rename.py hit/

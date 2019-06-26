import os
import sys
import time

input_path = sys.argv[1]

i = 0
for dir_path, subdir_list, file_list in os.walk(input_path):
    for fname in file_list:
        full_path = os.path.join(dir_path, fname)
        os.rename(full_path, dir_path + str(time.time()) + '.png')
        time.sleep(0.0515)
        i += 1

# python renamets.py hit/

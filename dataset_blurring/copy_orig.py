"""
For images that were not correctly blurred (object to blur out of the boxes of the automatic blurring), it copies the original image 
by relating the wrongly blurred image name to the original image and copy the original in another folder
"""

import os
from os import listdir
from os.path import isfile, join
import shutil

in_dir="new"
onlyfiles = [in_dir+"/"+f for f in listdir(in_dir) if isfile(join(in_dir, f)) and f.endswith("png") and f.startswith("mixed-31-01")]
# print(onlyfiles)
base_pth=[os.path.basename(file).replace('_blurred',"") for file in onlyfiles]
# print(old_pth)
orig_dir="orig"
orig_pth=[orig_dir+"/"+file for file in base_pth]
check_exist=[isfile(f) for f in orig_pth]
# print((check_exist))
# print(any(check_exist))
# print(orig_pth)
out_dir="manual"
out_pth=[out_dir+"/"+file for file in base_pth]
# print(out_pth)
if any(check_exist) and len(orig_pth)==len(out_pth):
    for i in range(len(orig_pth)):
        shutil.copyfile(orig_pth[i], out_pth[i])


in_dir="new"
onlyfiles = [in_dir+"/"+f for f in listdir(in_dir) if isfile(join(in_dir, f)) and f.endswith("png") and f.startswith("mixed-03-02")]
# print(onlyfiles)
base_pth=[os.path.basename(file).replace('_blurred',"") for file in onlyfiles]
# print(old_pth)
orig_dir="orig"
orig_pth=[orig_dir+"/"+file for file in base_pth]
check_exist=[isfile(f) for f in orig_pth]
# print((check_exist))
# print(any(check_exist))
# print(orig_pth)
out_dir="manual"
out_pth=[out_dir+"/"+file for file in base_pth]
# print(out_pth)
if any(check_exist) and len(orig_pth)==len(out_pth):
    for i in range(len(orig_pth)):
        shutil.copyfile(orig_pth[i], out_pth[i])
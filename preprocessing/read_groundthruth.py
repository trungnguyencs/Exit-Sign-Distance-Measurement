# For python 3.5+ you can use:
# from pathlib import Path
# for path in Path('.').rglob('*.png'):
#     print(path)
#     print(path.name)

import fnmatch
import os
import shutil

JPG_OUTPUT_DIR = '../data/groundtruth_exit_sign_cleaned/imgs/'
PNG_OUTPUT_DIR = '../data/groundtruth_exit_sign_cleaned/masks/'
TXT_OUTPUT_DIR = '../data/groundtruth_exit_sign_cleaned/camera_orientations/'

def match_file_type(root, filenames, type, lst):
  for filename in fnmatch.filter(filenames, '*.' + type):
    lst.append(os.path.join(root, filename))
  return lst

def copy_imgs(lst, output_dir):
  for i, src in enumerate(lst):
    new_name = '_'.join(src.split('/')[-4:])
    print(str(i) + ' ' + new_name)
    shutil.copy(src, output_dir + new_name)

def copy_txt(lst, output_dir):
  for i, src in enumerate(lst):
    new_name = src.split('/')[-1]
    print(str(i) + ' ' + new_name)
    shutil.copy(src, output_dir + new_name)

if __name__ == '__main__':
  jpg_list, png_list, txt_list = [], [], []
  for root, dirnames, filenames in os.walk('./groundtruth_exit_sign/'):
    match_file_type(root, filenames, 'jpg', jpg_list)
    match_file_type(root, filenames, 'png', png_list)
    match_file_type(root, filenames, 'txt', txt_list)
  # copy_imgs(jpg_list, JPG_OUTPUT_DIR)
  # copy_imgs(png_list, PNG_OUTPUT_DIR)
  # copy_txt(txt_list, TXT_OUTPUT_DIR)
  
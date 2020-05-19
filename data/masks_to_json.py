import cv2, json
import os, fnmatch
import numpy as np

MASK_PATH = './groundtruth_exit_sign_cleaned/masks/'
JSON_OUTPUT = './groundtruth_852.json'

def get_file_list(path):
  """
  Get the file name list of all png images in the folder
  """
  file_list = []
  for root, dirnames, filenames in os.walk(path):
    for filename in fnmatch.filter(filenames, '*.png'):
      file_list.append(filename)
  return file_list

def extract_corner(img):
  """
  Extract 4 corners of the mask using Harris corner detector 
  """
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  dst = cv2.cornerHarris(gray,5,3,0.04)
  ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
  dst = np.uint8(dst)
  ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
  corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)[1:]
  # img[dst>0.1*dst.max()]=[0,0,255]
  return corners.tolist()

def visualize_corners(corners, img):
  """
  Draw the 4 corners
  """
  for i in range(len(corners)):
      cv2.circle(img, (int(corners[i,0]), int(corners[i,1])), 7, (0,255,0), 2)
  cv2.imshow('image', cv2.resize(img, (672, 504)))
  cv2.waitKey(10000)

def write_to_json(arr, json_file_name):
  """
  Write the quadrilateral array to a json output file
  """
  with open(json_file_name, "w") as outfile: 
    json_obj = json.dumps(arr, default=lambda x: x.__dict__, indent=4, sort_keys=True)
    outfile.write(json_obj)

class Quadrilateral(object):
  def __init__(self, mask_id, vertices_2D):
    img_arr = mask_id.split('_')
    img_arr[2] = 'imgs'
    img_arr[-1] = 'jpg'
    self.mask_id = mask_id
    self.img_id = '_'.join(img_arr)
    self.vertices_2D = vertices_2D

if __name__ == '__main__':
  file_list = get_file_list(MASK_PATH)
  quadrilateral_arr = []
  for i, filename in enumerate(file_list):
    img = cv2.imread(MASK_PATH + filename)
    corners = extract_corner(img)
  # visualize_corners(corners, img)
    if len(corners) == 4:
      quadrilateral_arr.append(Quadrilateral(filename, corners))
      print(str(i) + ' ' + filename)
  write_to_json(quadrilateral_arr.sort(key=lambda x:x.mask_id), JSON_OUTPUT)


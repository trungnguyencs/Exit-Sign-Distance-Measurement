import json
import numpy as np
from matplotlib import pyplot as plt
import cv2

# SENSOR_WIDTH_MM = 3.5
# F_MM = 28
# F_PX = F_MM * IMG_WIDTH_PX / SENSOR_WIDTH_MM
IMG_WIDTH_PX = 360
IMG_HEIGHT_PX = 640
F_PX = 536
OBJ_WIDTH = 0.32 #in meters
OBJ_HEIGHT = 0.20
DEFAULT_VERTICES = [(0,OBJ_HEIGHT),(OBJ_WIDTH,OBJ_HEIGHT),(OBJ_WIDTH,0),(0,0)]
# DEFAULT_VERTICES = [(-OBJ_WIDTH/2,OBJ_HEIGHT/2),(OBJ_WIDTH/2,OBJ_HEIGHT/2),\
#                     (OBJ_WIDTH/2,-OBJ_HEIGHT/2),(-OBJ_WIDTH/2,-OBJ_HEIGHT/2)]

K = np.array([[536, 0  , 180], \
              [0,   536, 320], \
              [0,   0,   1  ]], dtype=np.float32)

JSON_INPUT = 'quadrilateral-1807.json'
JSON_OUTPUT = 'parallelogram-1787.json'

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Parallelogram(object):
  def __init__(self, id, url, p1, p2, p3, p4):
    """
    A parallelogram is defined by two lines: DC and DA
    """
    self.id = id
    self.url = url
    self.D, self.C, self.B, self.A = p1, p2, p3, p4
    self.long_edge = self.find_len(self.D, self.C)
    self.short_edge = self.find_len(self.D, self.A)
    self.angle = self.find_angle(self.A, self.D, self.C)

    self.distance_meter = OBJ_WIDTH * F_PX / self.long_edge
    
  def find_len(self, p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5

  def find_angle(self, A, D, C):
    angle1 = np.arctan2(A.y - D.y, A.x - D.x)
    angle2 = np.arctan2(C.y - D.y, C.x - D.x)
    return abs(angle1 - angle2)

def create_parallelograms(data):
  parallelogram_arr = []
  for i in range(len(data)):
    id = data[i]['External ID']
    url = data[i]['Labeled Data']
    try:
      pts = data[i]['Label']['EXIT_sign'][0]['geometry']
      p1 = Point(pts[0]['x'], pts[0]['y'])
      p2 = Point(pts[1]['x'], pts[1]['y'])
      p3 = Point(pts[2]['x'], pts[2]['y'])
      p4 = Point(pts[3]['x'], pts[3]['y'])
      parallelogram_arr.append(Parallelogram(id, url, p1, p2, p3, p4))
    except:
      continue
  return parallelogram_arr

def arr_to_json_file(arr, json_file_name):
  with open(json_file_name, "w") as outfile: 
    json_obj = json.dumps(arr, default=lambda x: x.__dict__, indent=4, sort_keys=True)
    outfile.write(json_obj)

def find_pinhole_distance(parallelogram_arr):
  distance_meter = [obj.distance_meter for obj in parallelogram_arr]
  min_distance, max_distance = min(distance_meter), max(distance_meter)
  for obj in parallelogram_arr:
    if obj.distance_meter == min_distance:
      print('Min: ' + str(obj.distance_meter))
      print(obj.id)
      print(obj.url)
    if obj.distance_meter == max_distance:
      print('Max: ' + str(obj.distance_meter))
      print(obj.id)
      print(obj.url)
  return distance_meter

def plot_distance_meter_histogram(distance_meter):
  plt.hist(distance_meter, rwidth=0.8, bins=50) 
  plt.xlabel('Distance (in meter)')
  plt.title('Histogram of distances calculated by pinhole model')
  plt.show()

with open(JSON_INPUT) as f:
  data = json.load(f)
parallelogram_arr = create_parallelograms(data)
# arr_to_json_file(parallelogram_arr, JSON_OUTPUT)
# distance_meter = find_pinhole_distance(parallelogram_arr)
# plot_distance_meter_histogram(distance_meter)

def print_point(pt):
  print(str(pt.D.x) + ' ' + str(pt.D.y) + ' | ' \
  + str(pt.C.x) + ' ' + str(pt.C.y) + ' | ' \
  + str(pt.B.x) + ' ' + str(pt.B.y) + ' | ' \
  + str(pt.A.x) + ' ' + str(pt.A.y))

# for pt in parallelogram_arr:
#   print_point(pt)

def find_homography(pts_src, pts_dst):
  pts_src = np.array(pts_src, dtype=np.float32)
  pts_dst = np.array(pts_dst, dtype=np.float32)
  print(pts_src)
  print(pts_dst)
  # H, status = cv2.findHomography(pts_src, pts_dst)
  H = cv2.getPerspectiveTransform(pts_src, pts_dst)
  return H

def find_R_t(H, K):
  num, Rs, Ts, Ns  = cv2.decomposeHomographyMat(H, K)
  return (num, Rs, Ts, Ns)

pt = parallelogram_arr[-1]
print(pt.url)
pts_src = [(pt.A.x, pt.A.y), (pt.B.x, pt.B.y), (pt.C.x, pt.C.y), (pt.D.x, pt.D.y)]
H = find_homography(pts_src, DEFAULT_VERTICES)
print('H: '); print(H)
print('---------------------------------------------------')
num, Rs, Ts, Ns = cv2.decomposeHomographyMat(H, K)
print('num: '); print(num)
print('Rs: '); print(Rs)
print('Ts: '); print(Ts)
print('Ns: '); print(Ns)


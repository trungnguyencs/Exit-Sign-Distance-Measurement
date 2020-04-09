
import json
import numpy as np
from matplotlib import pyplot as plt

IMG_WIDTH_PX = 360
SENSOR_WIDTH_MM = 3.5
F_MM = 28
F_PX = F_MM * IMG_WIDTH_PX / SENSOR_WIDTH_MM
F_PX = 536
OBJ_WIDTH_M = 0.32

JSON_INPUT = 'quadrilateral-1807.json'
JSON_OUTPUT = 'parallelogram-1787.json'

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Parallelogram(object):
  def __init__(self, id, url, p1, p2, p3, p4):
    """
    A quadrilateral is defined by two lines: p2p1 and p2p3
    """
    self.id = id
    self.url = url
    self.p1, self.p2, self.p3, self.p4 = p1, p2, p3, p4
    self.long_edge = self.find_len(p1, p2)
    self.short_edge = self.find_len(p1, p3)
    self.angle = self.find_angle(p1, p2, p3)

    self.distance_meter = OBJ_WIDTH_M * F_PX / self.long_edge
    
  def find_len(self, p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5

  def find_angle(self, p1, p2, p3):
    angle1 = np.arctan2(p3.y - p2.y, p3.x - p2.x)
    angle2 = np.arctan2(p1.y - p2.y, p1.x - p2.x)
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

def plot_distance_meter_histogram(distance_meter):
  plt.hist(distance_meter, rwidth=0.8, bins=50) 
  plt.xlabel('Distance (in meter)')
  plt.title('Histogram of distances calculated by pinhole model')
  plt.show()

with open(JSON_INPUT) as f:
  data = json.load(f)
parallelogram_arr = create_parallelograms(data)
# arr_to_json_file(parallelogram_arr, JSON_OUTPUT)
distance_meter = [obj.distance_meter for obj in parallelogram_arr]
# plot_distance_meter_histogram(distance_meter)
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



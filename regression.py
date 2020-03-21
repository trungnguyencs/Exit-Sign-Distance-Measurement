
import json
import numpy as np
import urllib

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Parallelogram(object):
  def __init__(self, id, pt1, pt2, pt3, pt4):
    """
    A quadrilateral is defined by two lines: p1p2 and p1p3
    """
    self.id = id
    self.p1, self.p2, self.p3, self.p4 = p1, p2, p3, p4
    self.long_edge = self.find_len(p1, p2)
    self.short_edge = self.find_len(p1, p3)
    self.angle = self.find_angle(p1, p2, p3)
    
  def find_len(self, p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5

  def find_angle(self, p1, p2, p3):
    angle1 = np.arctan2(p3.y - p1.y, p3.x - p1.x)
    angle2 = np.arctan2(p2.y - p1.y, p2.x - p1.x)
    return abs(angle1 - angle2)

def read_data(file):
  
  parallelogram_arr = []
  for i in range(len(data)):
    id = data[i]['External ID']
    pts = data[i]['Label']['EXIT_sign'][0]['geometry']
    print(id)
    print(pts)

def retrieve_img(data, folder):
  for i in range(len(data)):
    id = data[i]['External ID']
    urllib.urlretrieve("http://www.gunnerkrigg.com//comics/00000001.jpg", folder + id)

with open('quadrilateral-1807.json') as f:
  data = json.load(f)

retrieve_img(data, './imgs/')
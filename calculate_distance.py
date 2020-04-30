import json, cv2
import numpy as np
from matplotlib import pyplot as plt
from pnp import PNP

# SENSOR_WIDTH_MM = 3.5
# F_MM = 28
# F_PX = F_MM * IMG_WIDTH_PX / SENSOR_WIDTH_MM
IMG_WIDTH_PX = 360
IMG_HEIGHT_PX = 640
F_PX = 536
OBJ_WIDTH = 0.320 #in meters

JSON_INPUT = 'quadrilateral-raw-1807.json'
JSON_OUTPUT = 'quadrilateral-distance-1787.json'

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Quadrilateral(object):
  def __init__(self, id, url, pts):
    """
    A quadrilateral is defined by 4 points:
    - A: upper left
    - B: upper right
    - C: lower right
    - D: lower left
    vertices_2D: [A,B,C,D]
    url: url to download the original image
    """
    (A, B, C, D) = pts
    self.id = id
    self.url = url
    self.vertices_2D = [(A.x, A.y),(B.x,B.y),(C.x,C.y),(D.x,D.y)]
    # self.angle = self.find_angle(A, B, D)
    self.pinhole_distance = self.find_pinhole_distance(A, B, C, D)

    self.R_vec, self.T_vec = self.find_R_t(self.vertices_2D)
    self.homography_distance = self.find_homography_distance(self.T_vec)
    self.projected_vertices_2D = self.project_2D(self.R_vec, self.T_vec)

  def find_angle(self, A, B, D):
    """
    Calculate the angle between AB and AD (arctan2 guarantees < 90 degree)
    """
    angle1 = np.arctan2(B.y - A.y, B.x - A.x)
    angle2 = np.arctan2(D.y - A.y, D.x - A.x)
    return abs(angle1 - angle2)

  def find_pinhole_distance(self, A, B, C, D):
    """
    Estimate the distance to the sign estimated by the relationship between
    the longer edge in the image and the actual length of the exit sign
    """
    long_edge = ((A.x - B.x)**2 + (A.y - B.y)**2)**0.5
    return OBJ_WIDTH * F_PX / long_edge

  def find_R_t(self, vertices_2D):
    """
    Calculate R_vec and T_vec by PNP method - check file pnp.py
    """
    pnp = PNP()
    R_vec, T_vec = pnp.find_R_t(vertices_2D)
    return R_vec.tolist(), T_vec.tolist()

  def find_homography_distance(self, T_vec):
    """
    Calculate the distance to the exit sign as the magnitude of the traslational T_vector
    """
    pnp = PNP()
    homography_distance = pnp.calculate_distance_from_T(T_vec)
    return np.asscalar(homography_distance)

  def project_2D(self, R_vec, T_vec):
    """
    Project the 3D exit sign coodinates back to 2D given the computed Extrinsic vectors
    """
    pnp = PNP()
    projected_vertices_2D = pnp.project_to_2D(R_vec, T_vec)
    return projected_vertices_2D.tolist()

class Processing(object):
  def create_quadrilateral_arr(self, data):
    """
    Create an array of quadrilateral objects from the input data json object
    """
    quadrilateral_arr = []
    for i in range(len(data)):
      id = data[i]['External ID']
      url = data[i]['Labeled Data']
      try:
        pts = data[i]['Label']['EXIT_sign'][0]['geometry']
        p1 = Point(pts[0]['x'], pts[0]['y'])
        p2 = Point(pts[1]['x'], pts[1]['y'])
        p3 = Point(pts[2]['x'], pts[2]['y'])
        p4 = Point(pts[3]['x'], pts[3]['y'])
        pts = self.rearrange_pts(p1, p2, p3, p4)     # Rearrange the point in A B C D order
        quadrilateral_arr.append(Quadrilateral(id, url, pts))
      except:
        continue
    return quadrilateral_arr

  def rearrange_pts(self, p1, p2, p3, p4):
    """
    From 4 corner points, put them in A B C D order of a quadrilateral
    """
    arr = [p1, p2, p3, p4]
    arr.sort(key=lambda p: (p.x, p.y))
    # A and D will have smaller x, B and C will have larger x
    (A, D) = (arr[0], arr[1]) if arr[0].y < arr[1].y else (arr[1], arr[0])
    (B, C) = (arr[2], arr[3]) if arr[2].y < arr[3].y else (arr[3], arr[2])
    return (A, B, C, D)

  def write_to_json(self, arr, json_file_name):
    """
    Write the quadrilateral array to a json output file
    """
    with open(json_file_name, "w") as outfile: 
      json_obj = json.dumps(arr, default=lambda x: x.__dict__, indent=4, sort_keys=True)
      outfile.write(json_obj)

  def find_distance_stats(self, quadrilateral_arr, distance_arr, model):
    min_distance, max_distance = min(distance_arr), max(distance_arr)
    for obj in quadrilateral_arr:
      if model == 'pinhole':
        if obj.pinhole_distance == min_distance:
          print('Min pinhole distance: ' + str(obj.pinhole_distance))
          print('Image name: ' + obj.id)
          print('URL: ' + obj.url)
          print('-----------------------------------')
        if obj.pinhole_distance == max_distance:
          print('Max pinhole distance: ' + str(obj.pinhole_distance))
          print('Image name: ' + obj.id)
          print('URL: ' + obj.url)
      elif model == 'homography':
        if obj.homography_distance == min_distance:
          print('Min homography distance: ' + str(obj.homography_distance))
          print(obj.id)
          print(obj.url)
          print('-----------------------------------')
        if obj.homography_distance == max_distance:
          print('Max: ' + str(obj.homography_distance))
          print('Image name: ' + obj.id)
          print('URL: ' + obj.url)     

  def plot_histogram(self, arr):
    plt.hist(arr, rwidth=0.8, bins=50) 
    plt.xlabel('Distance (in meter)')
    plt.title('Histogram of distances')
    plt.show()

  def print_an_example(self, quadrilateral):
    """
    Printing the processing results for quadrilateral index i
    """
    print("2D coordinates of the testing point: ")
    print(quadrilateral.vertices_2D)
    print('R_vec: '); 
    print(quadrilateral.R_vec)
    print('T_vec: '); 
    print(quadrilateral.T_vec)
    print('Calculated distance from T_vector: '); 
    print(quadrilateral.homography_distance)
    print('Pinhole distance: '); 
    print(quadrilateral.pinhole_distance)

def main():
  with open(JSON_INPUT) as f:
    data = json.load(f)
  P = Processing()
  quadrilateral_arr = P.create_quadrilateral_arr(data)
  P.write_to_json(quadrilateral_arr, JSON_OUTPUT)
  
  print('***********************************************************************')
  pinhole_distance_arr = [obj.pinhole_distance for obj in quadrilateral_arr]
  P.find_distance_stats(quadrilateral_arr, pinhole_distance_arr, model='pinhole')
  P.plot_histogram(pinhole_distance_arr)

  print('***********************************************************************')
  homography_distance_arr = [obj.homography_distance for obj in quadrilateral_arr]
  P.find_distance_stats(quadrilateral_arr, homography_distance_arr, model='homography')
  P.plot_histogram(homography_distance_arr)

  print('***********************************************************************')
  P.print_an_example(quadrilateral_arr[0])

if __name__== "__main__":
  main()
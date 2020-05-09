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
    vertices_2D: in [A,B,C,D] order
    url: url to download the original image
    """
    (A, B, C, D) = pts
    self.id = id
    self.url = url
    self.vertices_2D = [[A.x, A.y],[B.x,B.y],[C.x,C.y],[D.x,D.y]]
    # self.angle = self.find_angle(A, B, D)
    self.pinhole_distance = self.find_pinhole_distance(A, B, C, D)

    self.R_vec, self.T_vec = self.find_R_t(self.vertices_2D)
    self.homography_distance = self.find_homography_distance(self.T_vec)
    self.projected_vertices_2D = self.project_2D(self.R_vec, self.T_vec)
    self.x_err, self.y_err = self.find_projection_err(self.vertices_2D, self.projected_vertices_2D)

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

  def find_projection_err(self, vertices_2D, projected_vertices_2D):
    """
    Calculate the average error (in pixels) between the labeled vertices and the 
    projected vertices of a quadrilateral
    """
    vertices_2D = np.array(vertices_2D)
    projected_vertices_2D = np.array(projected_vertices_2D)
    err = np.sum(np.abs(vertices_2D - projected_vertices_2D), axis=0)/len(vertices_2D)
    return err.tolist()


import json, cv2
import numpy as np
from matplotlib import pyplot as plt
from pnp import PNP

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

    self.R_vec, self.T_vec = self.find_R_t(self.vertices_2D)
    self.distance = self.find_distance(self.T_vec)
    self.projected_vertices_2D = self.project_2D(self.R_vec, self.T_vec)
    self.x_err, self.y_err = self.find_projection_err(self.vertices_2D, self.projected_vertices_2D)

  def find_R_t(self, vertices_2D):
    """
    Calculate R_vec and T_vec by PNP method - check file pnp.py
    """
    pnp = PNP()
    R_vec, T_vec = pnp.find_R_t(vertices_2D)
    return R_vec.tolist(), T_vec.tolist()

  def find_distance(self, T_vec):
    """
    Calculate the distance to the exit sign as the magnitude of the traslational T_vector
    """
    pnp = PNP()
    distance = pnp.calculate_distance_from_T(T_vec)
    return np.asscalar(distance)

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


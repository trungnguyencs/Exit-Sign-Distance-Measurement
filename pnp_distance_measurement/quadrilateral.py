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
    vertices_2D: in [A,B,C,D] order that maches the exit sign
    url: url to download the original image
    """
    (A, B, C, D) = self.rearrange_pts(pts)
    self.id = id
    self.url = url
    self.vertices_2D = [[A.x, A.y],[B.x,B.y],[C.x,C.y],[D.x,D.y]]

    self.R_vec, self.T_vec = self.find_R_t(self.vertices_2D)
    self.distance = self.find_distance(self.T_vec)
    self.projected_vertices_2D = self.project_2D(self.R_vec, self.T_vec)
    self.x_err, self.y_err = self.find_projection_err(self.vertices_2D, self.projected_vertices_2D)

  def rearrange_pts(self, pts):
    """
    From 4 corner points of random order, put them in A B C D order of a quadrilateral
    A -------- B
    |          |
    D -------- C
    or if it's like this
    A -- B                B -- C
    |    |                |    |
    |    | then rotate to |    |
    |    |                |    |
    D -- C                A -- D
    """
    arr = list(pts)
    arr.sort(key=lambda p: (p.x, p.y))
    # A and D will have smaller x, B and C will have larger x
    (A, D) = (arr[0], arr[1]) if arr[0].y < arr[1].y else (arr[1], arr[0])
    (B, C) = (arr[2], arr[3]) if arr[2].y < arr[3].y else (arr[3], arr[2])
    pts = self.rotate_vertical_quadrilateral(A,B,C,D)
    return pts

  def rotate_vertical_quadrilateral(self,A,B,C,D):
    """
    If the quadrilateral is vertical, then return the 90 degree rotate right order
    so that it matches the exit sign
    """
    def euclidean_distance(ptA, ptB):
      return ((ptA.x - ptB.x)**2 + (ptA.y - ptB.y)**2)**0.5

    if euclidean_distance(A, B) < euclidean_distance(A, D):
      return (D,A,B,C)
    return (A,B,C,D)

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


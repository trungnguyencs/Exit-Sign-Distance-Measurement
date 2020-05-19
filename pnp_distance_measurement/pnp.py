import cv2
import numpy as np
import conf

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Quadrilateral(object):
  def __init__(self, id, pts):
    """
    vertices_2D: in [A,B,C,D] order that maches the exit sign
    url: url to download the original image
    """
    (A, B, C, D) = self.rearrange_pts(pts)
    self.id = id
    self.vertices_2D = [[A.x, A.y],[B.x,B.y],[C.x,C.y],[D.x,D.y]]

    self.R_vec, self.T_vec = self.find_R_t(self.vertices_2D)
    self.distance = self.find_distance(self.T_vec)
    self.projected_vertices_2D = self.project_2D(self.R_vec, self.T_vec, conf.DEFAULT_VERTICES_3D)
    
    self.projected_normal_vec = self.project_2D(self.R_vec, self.T_vec, conf.DEFAULT_NORMAL_VECTOR_3D)
    self.projected_parallel_vertices_2D = self.project_2D(self.R_vec, self.T_vec, conf.PARALLEL_VERTICES_3D)
    
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

  def find_R_t(self, pts_2D):
    """
    Find R vector and T vector from input 2D image points using PNP algorithm
    Solve PNP docs: 
    https://docs.opencv.org/3.0-beta/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#solvepnp
    """
    pts_2D = np.array(pts_2D, dtype=np.float32)
    ret, R_vec, T_vec = cv2.solvePnP(conf.DEFAULT_VERTICES_3D, pts_2D, conf.K, conf.DIST_COEFFS)
    return R_vec.tolist(), T_vec.tolist()

  def find_distance(self, T_vec):
    """
    Calculate the distance to the exit sign as the magnitude of the traslational T_vector
    """
    distance = np.sqrt(np.sum(np.array(T_vec) ** 2))
    return np.asscalar(distance)

  def project_2D(self, R_vec, T_vec, pts_3D):
    """
    Project the 3D exit sign coodinates back to 2D given the computed Extrinsic vectors
    """
    pts_2D, jacobian = cv2.projectPoints(pts_3D, np.array(R_vec), np.array(T_vec), conf.K, conf.DIST_COEFFS)
    projected_vertices_2D = np.reshape(pts_2D, (-1,2))
    return np.int32(projected_vertices_2D).tolist()

  def find_projection_err(self, vertices_2D, projected_vertices_2D):
    """
    Calculate the average error (in pixels) between the labeled vertices and the 
    projected vertices of a quadrilateral
    """
    vertices_2D = np.array(vertices_2D)
    projected_vertices_2D = np.array(projected_vertices_2D)
    err = np.sum(np.abs(vertices_2D - projected_vertices_2D), axis=0)/len(vertices_2D)
    return err.tolist()


import numpy as np
import cv2

OBJ_WIDTH = 0.320 # Sign width = 0.32m 
OBJ_HEIGHT = 0.200 # Sign height = 0.20m
DEFAULT_PTS_3D = np.array([[0,         0,          0], [OBJ_WIDTH, 0,          0], \
                           [OBJ_WIDTH, OBJ_HEIGHT, 0], [0,         OBJ_HEIGHT, 0]], dtype=np.float32)
K = np.array([[536, 0  , 180], \
              [0,   536, 320], \
              [0,   0,   1  ]], dtype=np.float32)
DIST_COEFFS = np.array([0, 0, 0, 0], dtype=np.float32)

class PNP(object):
  def find_R_t(self, pts_2D):
    """
    Find R matrix and T vector from input 2D image points using PNP algorithm
    """
    pts_2D = np.array(pts_2D, dtype=np.float32)
    # H, status = cv2.findHomography(pts_2D, pts_3D)
    # H = cv2.getPerspectiveTransform(pts_2D, pts_3D)
    # num, Rs, Ts, Ns  = cv2.decomposeHomographyMat(H, K)

    # Solve PNP docs: 
    # https://docs.opencv.org/3.0-beta/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#solvepnp
    ret, R_vec, T_vec = cv2.solvePnP(DEFAULT_PTS_3D, pts_2D, K, DIST_COEFFS)
    # R_mat, _ = cv2.Rodrigues(R_vec)
    return R_vec, T_vec

  def calculate_distance_from_T(self, T_vec):
    """
    Distance is the magnidute of the T vector
    """
    return np.sqrt(np.sum(np.array(T_vec) ** 2))

  def project_to_2D(self, R_vec, T_vec):
    """
    Project the 3D exit sign coodinates to 2D given the computed Extrinsic vectors
    """
    pts_2D, jacobian = cv2.projectPoints(DEFAULT_PTS_3D, np.array(R_vec), np.array(T_vec), K, DIST_COEFFS)
    return np.reshape(pts_2D, (-1,2))

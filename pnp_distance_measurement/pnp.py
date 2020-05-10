import numpy as np
import cv2

# Camera matrix of exit sign data
# OBJ_WIDTH = 0.335 # Sign width in meters 
# OBJ_HEIGHT = 0.195 # Sign height in meters
# K = np.array([[536, 0,   180], \
#               [0,   536, 320], \
#               [0,   0,   1  ]], dtype=np.float32)
# DIST_COEFFS = np.array([0, 0, 0, 0], dtype=np.float32)

# Camera matrix of debugging data, original 4032x3024
OBJ_WIDTH = 32.0 * 0.0254
OBJ_HEIGHT = 19.0 * 0.0254
K = np.array([[3280.1416389452497, 0.0,                2051.308838596682 ], \
              [0.0,                3298.877562243612,  1457.0395478396988], \
              [0.0,                0.0,                1.0               ]], dtype=np.float32)
DIST_COEFFS = np.array([0.3584224308304239, -3.2316961497984638, -0.0020241077395336247, \
                        0.005125810383911658, 9.145486487494859], dtype=np.float32)

# Camera matrix of debugging data, resized 1008x756
# OBJ_WIDTH = 32.0 * 0.0254
# OBJ_HEIGHT = 19.0 * 0.0254
# K = np.array([[819.7375674224452,  0.0,                512.6162509923176 ], \
#               [0.0,                824.4628650025569,  363.63539991910477], \
#               [0.0,                0.0,                1.0               ]], dtype=np.float32)
# DIST_COEFFS = np.array([0.3625525153631118, -3.2679279813000974, -0.0021839532687696257, \
#                         0.005111306480977345, 9.299685322344486], dtype=np.float32)

DEFAULT_PTS_3D = np.array([[0,         0,          0], [OBJ_WIDTH, 0,          0], \
                           [OBJ_WIDTH, OBJ_HEIGHT, 0], [0,         OBJ_HEIGHT, 0]], dtype=np.float32)

class PNP(object):
  def find_R_t(self, pts_2D):
    """
    Find R vector and T vector from input 2D image points using PNP algorithm
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

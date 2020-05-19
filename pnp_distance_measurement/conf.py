import numpy as np

model = 'groundtruth_1920x1440_iPhone8'
# model = 'main_360x640'
# model = 'street_4032x3024_iPhone8s'
# model = 'street_1008x756_iPhone8s'

if model == 'groundtruth_1920x1440_iPhone8':
  # Groundthruth data set, img size 1920x1440
  JSON_INPUT = '../data/json/groundtruth-830.json'
  JSON_OUTPUT = '../data/json/groundtruth-results-830.json'
  JSON_FLAG = 'from reading imgs'
  IMG_PATH = '../data/groundtruth_exit_sign_cleaned/imgs/'

  OBJ_WIDTH = 0.335 # Sign width in meters 
  OBJ_HEIGHT = 0.195 # Sign height in meters
  K = np.array([[1602, 0,    1920//2], \
                [0,    1602, 1440//2], \
                [0,    0,    1      ]], dtype=np.float32)
  DIST_COEFFS = np.array([0, 0, 0, 0], dtype=np.float32)

elif model == 'main_360x640':
  # Main data set, img size 360x640
  JSON_INPUT = '../data/json/quadrilateral-raw-1807.json'
  JSON_OUTPUT = '../data/json/quadrilateral-results-1787.json'
  JSON_FLAG = 'from labelbox'
  IMG_PATH = '../data/exit_sign/'
  LABEL = 'EXIT_sign'

  OBJ_WIDTH = 0.335 # Sign width in meters 
  OBJ_HEIGHT = 0.195 # Sign height in meters
  K = np.array([[536,  0,    360//2], \
                [0,    536,  640//2], \
                [0,    0,    1     ]], dtype=np.float32)
  DIST_COEFFS = np.array([0, 0, 0, 0], dtype=np.float32)

elif model == 'street_4032x3024_iPhone8s':
  # Street data set, iPhone 8s, img size 4032x3024
  JSON_INPUT = '../data/json/street-raw-4032x3024.json'
  JSON_OUTPUT = '../data/json/street-results-4032x3024.json'
  JSON_FLAG = 'from labelbox'
  IMG_PATH = '../data/street_4032x3024/'
  LABEL = 'rectangle'

  OBJ_WIDTH = 32.0 * 0.0254
  OBJ_HEIGHT = 19.0 * 0.0254
  K = np.array([[3280.1416389452497, 0.0,                2051.308838596682 ], \
                [0.0,                3298.877562243612,  1457.0395478396988], \
                [0.0,                0.0,                1.0               ]], dtype=np.float32)
  DIST_COEFFS = np.array([0.3584224308304239, -3.2316961497984638, -0.0020241077395336247, \
                          0.005125810383911658, 9.145486487494859], dtype=np.float32)

elif model == 'street_1008x756_iPhone8s':
  # Street data set, iPhone 8s, img resized 1008x756
  JSON_INPUT = '../data/json/street-raw-1008x756.json'
  JSON_OUTPUT = '../data/json/street-results-1008x756.json'
  JSON_FLAG = 'from labelbox'
  IMG_PATH = '../data/street_1008x756/'
  LABEL = 'rectangle'

  OBJ_WIDTH = 32.0 * 0.0254
  OBJ_HEIGHT = 19.0 * 0.0254
  K = np.array([[819.7375674224452,  0.0,                512.6162509923176 ], \
                [0.0,                824.4628650025569,  363.63539991910477], \
                [0.0,                0.0,                1.0               ]], dtype=np.float32)
  DIST_COEFFS = np.array([0.3625525153631118, -3.2679279813000974, -0.0021839532687696257, \
                          0.005111306480977345, 9.299685322344486], dtype=np.float32)

DEFAULT_VERTICES_3D = np.array([[0,         0,          0], [OBJ_WIDTH, 0,          0], \
                                [OBJ_WIDTH, OBJ_HEIGHT, 0], [0,         OBJ_HEIGHT, 0]], dtype=np.float32)
DEFAULT_NORMAL_VECTOR_3D = np.array([[OBJ_WIDTH/2, OBJ_HEIGHT/2, 0         ],\
                                     [OBJ_WIDTH/2, OBJ_HEIGHT/2, OBJ_WIDTH ]], dtype=np.float32)
PARALLEL_VERTICES_3D = np.array([[0,         0,          OBJ_WIDTH], [OBJ_WIDTH, 0,          OBJ_WIDTH], \
                                 [OBJ_WIDTH, OBJ_HEIGHT, OBJ_WIDTH], [0,         OBJ_HEIGHT, OBJ_WIDTH]], dtype=np.float32)



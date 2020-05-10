import cv2
import glob

images = glob.glob(r'./to_resize/*.jpg')
OUTPUT_FOLDER = './resized/calib'
SCALE_PERCENT = 0.25
count = 1

images.sort()
for fname in images:
  img = cv2.imread(fname)
  w = int(img.shape[1] * SCALE_PERCENT)
  h = int(img.shape[0] * SCALE_PERCENT)
  resized = cv2.resize(img, (w, h), interpolation = cv2.INTER_AREA)
  output_name = OUTPUT_FOLDER + str(count).zfill(2) + '.jpg'
  print(output_name)
  cv2.imwrite(output_name, resized)
  count += 1

import json
from multiprocessing.dummy import Pool as ThreadPool
from urllib import urlretrieve
# from urllib.request import urlretrieve

IMG_PATH = './data/imgs/'
# LABEL_PATH = './data/labels/'

def get_list(data):
  success, failed = [], []
  for i in range(len(data)):
    id = data[i]['External ID']
    img_url = data[i]['Labeled Data']
    try:
      label_url = data[i]['Masks']['EXIT_sign']
      success.append((id, img_url, label_url))
    except:
      failed.append((id, img_url))
  return success, failed

def get_url(id, img_url, label_url):
  urlretrieve(img_url, IMG_PATH + id)
  # urlretrieve(label_url, LABEL_PATH + id)

with open('quadrilateral-1807.json') as f:
  data = json.load(f)
success, failed = get_list(data)

print('Success count ' + str(len(success)))
print('Failure count ' + str(len(failed)))

for i in range(0, len(success)):
  (id, img_url, label_url) = success[i]
  get_url(id, img_url, label_url)
  print(str(i) + ' ' + id)

# pool = ThreadPool(100)
# results = pool.starmap(get_url, zip(success.values(), success.keys()))


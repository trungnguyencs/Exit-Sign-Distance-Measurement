import json
import urllib

def retrieve_imgs(data, folder):
  for i in range(len(data)):
    id = data[i]['External ID']
    url = data[i]['Labeled Data']
    print(id)
    urllib.urlretrieve(url, folder + id)

def retrieve_labels(data, img_path, label_path):
  for i in range(len(data)):
    try:
      id = data[i]['External ID']
      url = data[i]['Masks']['EXIT_sign']
      print(str(i) + id)
      urllib.urlretrieve(url, folder + id)
      urllib.urlretrieve(url, folder + id)
    except:
      continue

with open('quadrilateral-1807.json') as f:
  data = json.load(f)
retrieve_labels(data, './data/imgs/', './data/labels/')
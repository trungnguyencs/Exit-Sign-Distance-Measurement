import json
import urllib

def retrieve_imgs(data, folder):
  for i in range(len(data)):
    id = data[i]['External ID']
    url = data[i]['Labeled Data']
    urllib.urlretrieve(url, folder + id)

def retrieve_labels(data, folder):
  for i in range(len(data)):
    id = data[i]['External ID']
    url = data[i]['Masks']['EXIT_sign']
    urllib.urlretrieve(url, folder + id)

with open('quadrilateral-1807.json') as f:
  data = json.load(f)
retrieve_imgs(data, './data/imgs/')
retrieve_labels(data, './data/labels/')
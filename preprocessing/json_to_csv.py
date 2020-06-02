import pandas as pd 
import json

# INPUT_JSON = '../data/json/quadrilateral-results-1787.json'
# OUTPUT = '../data/csv/quadrilateral-1787.csv'
# INPUT_JSON = '../data/json/groundtruth-results-830.json'
# OUTPUT = '../data/csv/groundtruth-830.csv'
# INPUT_JSON = '../data/json/street-results-4032x3024.json'
# OUTPUT = '../data/csv/street-4032x3024.csv'
INPUT_JSON = '../data/json/street-results-1008x756.json'
OUTPUT = '../data/csv/street-1008x756.csv'

with open(INPUT_JSON) as f:
  data = json.load(f)

csv_data = []
for item in data:
    row = {}
    row['filename'] = item['id']
    row['width'] = item['img_size'][0]
    row['height'] = item['img_size'][1]
    row['xmin'] = min(item['vertices_2D'][0][0], item['vertices_2D'][1][0],\
                      item['vertices_2D'][2][0], item['vertices_2D'][3][0])
    row['ymin'] = min(item['vertices_2D'][0][1], item['vertices_2D'][1][1],\
                      item['vertices_2D'][2][1], item['vertices_2D'][3][1])    
    row['xmax'] = max(item['vertices_2D'][0][0], item['vertices_2D'][1][0],\
                      item['vertices_2D'][2][0], item['vertices_2D'][3][0])    
    row['ymax'] = max(item['vertices_2D'][0][1], item['vertices_2D'][1][1],\
                      item['vertices_2D'][2][1], item['vertices_2D'][3][1])   
    row['distance'] = item['distance']
    row['class'] = 'Exit_sign'
    csv_data.append(row)
    
df = pd.DataFrame(csv_data)
df.to_csv(OUTPUT, index=False) 
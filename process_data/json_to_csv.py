import pandas as pd 

INPUT_JSON = '../results/json_results/groundtruth-results-830.json'
OUTPUT = '../data/csv/label-1787.csv'

df = pd.read_json(INPUT_JSON)
print(df.head(5))

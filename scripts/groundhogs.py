"""Convert raw_data/groundhogs.json into a csv file we can read.

The data is all pretty simple except the nested `predictions` field which we
must unnets

Data is from: https://groundhog-day.com/api
"""
import json
import csv
import copy
import datetime as dt

with open('./raw_data/groundhogs.json') as f:
  data = json.load(f)['groundhogs']

# get the fieldnames
fieldnames = copy.deepcopy(data[0]) # copy
fieldnames.update(fieldnames.pop('predictions')[0])
fieldnames['early_spring'] = fieldnames.pop('year')
fieldnames = list(fieldnames.keys())

GEN = './gen/groundhogs.csv'
with open(GEN, 'w') as f:
  writer = csv.DictWriter(f, fieldnames=fieldnames)
  writer.writeheader()
  for d in data:
    predictions = d.pop('predictions')
    for p in predictions:
      date = dt.date(int(p.pop('year')), 2, 2)
      p['early_spring'] = str(date)
      d.update(p)
      writer.writerow(d)

print('Generated', GEN)

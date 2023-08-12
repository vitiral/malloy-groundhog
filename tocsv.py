"""Convert data/groundhogs.json into a csv file we can read.

The data is all pretty simple except the nested `predictions` field which we
must unnets

"""
import json
import csv
import copy


with open('./data/groundhogs.json') as f:
  data = json.load(f)['groundhogs']


# get the fieldnames
fieldnames = copy.deepcopy(data[0]) # copy
fieldnames.update(fieldnames.pop('predictions')[0])
fieldnames['the_day'] = fieldnames.pop('year')
fieldnames = list(fieldnames.keys())

with open('./data/groundhogs.csv', 'w') as f:
  writer = csv.DictWriter(f, fieldnames=fieldnames)
  writer.writeheader()
  for d in data:
    predictions = d.pop('predictions')
    for p in predictions:
      p['the_day'] = '{}-02-02'.format(p.pop('year'))
      d.update(p)
      print(d)
      writer.writerow(d)

print(fieldnames)

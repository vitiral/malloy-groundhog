from pprint import pprint as pp
import csv

EXAMPLE = '''
0101270001  51.90  54.20  63.90  72.90  80.90  88.70  91.40  90.60  86.40  74.90  62.90  52.60
0101270002  52.10  55.20  63.10  73.10  81.30  89.30  91.50  90.80  86.80  75.40  62.20  53.50
0101270003  52.30  55.10  63.20  73.20  81.10  89.10  91.40  90.70  86.10  75.50  62.00  53.50
0101270004  52.10  54.90  62.30  73.00  81.40  89.00  91.10  90.90  85.30  75.10  61.80  53.20
'''

# https://www.ncei.noaa.gov/pub/data/cirs/climdiv/divisional-readme.txt
STATE_CODES = '''
01 Alabama
02 Arizona
03 Arkansas
04 California
05 Colorado
06 Connecticut
07 Delaware
08 Florida
09 Georgia
10 Idaho
11 Illinois
12 Indiana
13 Iowa
14 Kansas
15 Kentucky
16 Louisiana
17 Maine
18 Maryland
19 Massachusetts
20 Michigan
21 Minnesota
22 Mississippi
23 Missouri
24 Montana
25 Nebraska
26 Nevada
27 New Hampshire
28 New Jersey
29 New Mexico
30 New York
31 North Carolina
32 North Dakota
33 Ohio
34 Oklahoma
35 Oregon
36 Pennsylvania
37 Rhode Island
38 South Carolina
39 South Dakota
40 Tennessee
41 Texas
42 Utah
43 Vermont
44 Virginia
45 Washington
46 West Virginia
47 Wisconsin
48 Wyoming
50 Alaska
'''

states = {}
for state in STATE_CODES.strip().split('\n'):
  code, state = state.split(' ', 1)
  states[code] = state

# https://www.ncei.noaa.gov/pub/data/cirs/climdiv/divisional-readme.txt
CODES = {'02': 'avg_temp', '27': 'max_temp', '28': 'min_temp'}

def extract_meta(el):
  return {
      'state': states[el[0:2]],
      'division': el[2:4],
      'raw_code': el[4:6],
      'raw_year': el[6:10],
  }

def fix_year(year):
  if year.startswith('00'):
    return '20' + year[2:]
  return year

def split_row(row_str):
  meta_months = row_str.split()
  rows = []
  meta = extract_meta(meta_months[0])
  for i in range(1, 13):
    row = dict(meta)
    row['date'] = '{}-{}-01'.format(fix_year(row['raw_year']), f'{i:>02}')
    raw_code = row['raw_code']
    tmp_col = CODES[raw_code]
    row[tmp_col] = float(meta_months[i])
    rows.append(row)
  return rows

def noa_rows(lines):
  rows = []
  for l in lines:
    rows.extend(split_row(l))
  return rows

fieldnames =  [
  'date',
  'state',
  'max_temp',
  'division',
  'raw_code',
  'raw_year',
]


GEN = './gen/noa.csv'
with open(GEN, 'w') as f, open('./raw_data/noaa.txt') as raw:
  w = csv.DictWriter(f, fieldnames=fieldnames)
  w.writeheader()
  # rows = noa_rows(EXAMPLE.strip().split('\n'))
  rows = noa_rows(raw)
  rows.sort(key=lambda d: (d['date'], d['state']) )
  for row in rows:
    w.writerow(row)

print('Generated', GEN)

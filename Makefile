

gen: gen_groundhogs gen_noaa

gen_groundhogs: scripts/groundhogs.py raw_data/groundhogs.json
	python3 scripts/groundhogs.py

gen_noaa: scripts/groundhogs.py raw_data/groundhogs.json
	python3 scripts/noaa.py


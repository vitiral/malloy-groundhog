

gen: scripts/groundhogs.py data/groundhogs.json
	python3 scripts/groundhogs.py
	python3 scripts/noaa.py


"""Builds the offline atlas Res/atlas.db from the GeoNames list of places with
500 or more inhabitants (cities500), with country and region names.

    python3 tools/build_atlas.py              # downloads from download.geonames.org
    python3 tools/build_atlas.py --from DIR   # uses cities500.zip, countryInfo.txt and
                                              # admin1CodesASCII.txt already in DIR

GeoNames data is licensed under CC BY 4.0 (https://www.geonames.org)."""

import io
import os
import sys
import sqlite3
import zipfile
import argparse
import datetime
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import atlas	# noqa: E402

URL = 'https://download.geonames.org/export/dump/'
FILES = ('cities500.zip', 'countryInfo.txt', 'admin1CodesASCII.txt')


def fetch(name, src):
	if src:
		with open(os.path.join(src, name), 'rb') as f:
			return f.read()
	print('downloading', URL+name)
	with urllib.request.urlopen(URL+name) as r:
		return r.read()


def lines(data):
	for line in io.TextIOWrapper(io.BytesIO(data), encoding='utf-8'):
		if not line.startswith('#'):
			yield line.rstrip('\n').split('\t')


def build(src, out):
	data = {name: fetch(name, src) for name in FILES}
	countries = {f[0]: f[4] for f in lines(data['countryInfo.txt']) if len(f) > 4}
	regions = {f[0]: f[1] for f in lines(data['admin1CodesASCII.txt']) if len(f) > 1}
	with zipfile.ZipFile(io.BytesIO(data['cities500.zip'])) as z:
		cities = z.read('cities500.txt')

	tmp = out+'.tmp'
	if os.path.exists(tmp):
		os.remove(tmp)
	db = sqlite3.connect(tmp)
	db.executescript('''
		CREATE TABLE places (id INTEGER PRIMARY KEY, name TEXT, lat REAL, lon REAL, cc TEXT,
			country TEXT, admin1 TEXT, ckey TEXT, akey TEXT, alt INTEGER, tz TEXT, pop INTEGER);
		CREATE TABLE names (key TEXT, id INTEGER, PRIMARY KEY (key, id)) WITHOUT ROWID;
		CREATE TABLE info (key TEXT PRIMARY KEY, value TEXT);''')
	num = 0
	for f in lines(cities):
		gid, name, ascii, alternates, lat, lon = f[0], f[1], f[2], f[3], float(f[4]), float(f[5])
		cc, admin1, pop, elev, dem, tz = f[8], f[10], int(f[14] or 0), f[15], f[16], f[17]
		if not tz:
			continue
		alt = int(elev) if elev else (int(dem) if dem and int(dem) > -9999 else 0)
		country = countries.get(cc, cc)
		region = regions.get(cc+'.'+admin1, '')
		db.execute('INSERT INTO places VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
			(int(gid), name, lat, lon, cc, country, region, atlas.normalize(country), atlas.normalize(region), alt, tz, pop))
		keys = {atlas.normalize(n) for n in [name, ascii]+alternates.split(',') if n and len(n) <= 60}
		db.executemany('INSERT INTO names VALUES (?,?)', [(k, int(gid)) for k in keys if k])
		num += 1
	db.execute('CREATE INDEX places_lat ON places (lat)')
	db.executemany('INSERT INTO info VALUES (?,?)', [
		('source', 'GeoNames cities500, '+URL+' (CC BY 4.0)'),
		('built', datetime.date.today().isoformat()),
		('places', str(num))])
	db.commit()
	db.execute('VACUUM')
	db.close()
	os.replace(tmp, out)
	print('%s: %d places' % (out, num))


def main():
	ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
	ap.add_argument('--from', dest='src', help='folder with the GeoNames files (default: download them)')
	ap.add_argument('--out', default=os.path.join(ROOT, atlas.FILENAME))
	args = ap.parse_args()
	build(args.src, args.out)


if __name__ == '__main__':
	main()

# Compares two refdump.py outputs numerically.
#   python3 refcompare.py reference.json[.gz] port.json [--rtol 1e-9] [--max 50]

import re
import sys
import gzip
import json
import argparse


def load(path):
	opener = gzip.open if path.endswith('.gz') else open
	with opener(path, 'rt', encoding='utf-8') as f:
		return json.load(f)


def isnum(v):
	return isinstance(v, (int, float)) and not isinstance(v, bool)


# FixedStars.mixed maps sorted stars back to options.fixedstars iteration order,
# which differs between Py2 (hash order) and Py3 (insertion order) for the
# built-in defaults (all unselected). Saved option files keep their pickled Py2
# order, and pdfixedstarssel is indexed consistently with it, so this is not a behavior change.
IGNORE = [r'/fixedstars/mixed\[']


def compare(a, b, path, diffs, rtol, atol):
	if any(re.search(p, path) for p in IGNORE):
		return
	if isnum(a) and isnum(b):
		if abs(a-b) > max(atol, rtol*max(abs(a), abs(b))):
			diffs.append((path, a, b))
	elif isinstance(a, dict) and isinstance(b, dict):
		for k in sorted(set(a) | set(b)):
			if k not in a or k not in b:
				diffs.append((path+'/'+k, a.get(k, '<missing>'), b.get(k, '<missing>')))
			else:
				compare(a[k], b[k], path+'/'+k, diffs, rtol, atol)
	elif isinstance(a, list) and isinstance(b, list):
		if len(a) != len(b):
			diffs.append((path+'#len', len(a), len(b)))
		for i, (x, y) in enumerate(zip(a, b)):
			compare(x, y, '%s[%d]' % (path, i), diffs, rtol, atol)
	elif a != b:
		diffs.append((path, a, b))


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('reference')
	ap.add_argument('port')
	ap.add_argument('--rtol', type=float, default=1e-9)
	ap.add_argument('--atol', type=float, default=1e-9)
	ap.add_argument('--max', type=int, default=50)
	args = ap.parse_args()

	ref, port = load(args.reference), load(args.port)
	failed = 0
	for case in sorted(set(ref) | set(port)):
		diffs = []
		compare(ref.get(case, '<missing>'), port.get(case, '<missing>'), '', diffs, args.rtol, args.atol)
		if diffs:
			failed += 1
			print('FAIL %s (%d differences)' % (case, len(diffs)))
			for p, a, b in diffs[:args.max]:
				print('    %s: %r != %r' % (p, str(a)[:200], str(b)[:200]))

	print('%d/%d cases differ' % (failed, len(set(ref) | set(port))))
	sys.exit(1 if failed else 0)


if __name__ == '__main__':
	main()

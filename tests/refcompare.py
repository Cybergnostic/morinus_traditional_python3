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


# Primary directions are sorted by arc; two directions whose arcs agree to the
# last bits of a double are ordered by rounding noise, which differs between C
# compilers (gcc and MSVC). Such ties are compared without regard to order.
def align_ties(a, b, tol):
	if len(a) != len(b) or not all(isinstance(x, dict) and isnum(x.get('arc')) for x in a + b):
		return b
	ident = lambda x: tuple((k, v) for k, v in sorted(x.items()) if not isinstance(v, float))
	b = list(b)
	i = 0
	while i < len(b):
		j = i + 1
		while j < len(b) and abs(b[j]['arc'] - b[i]['arc']) <= tol:
			j += 1
		order = [ident(x) for x in a[i:j]]
		run = b[i:j]
		if sorted(order) == sorted(ident(y) for y in run):
			b[i:j] = sorted(run, key=lambda y: order.index(ident(y)))
		i = j
	return b


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
		b = align_ties(a, b, atol)
		for i, (x, y) in enumerate(zip(a, b)):
			compare(x, y, '%s[%d]' % (path, i), diffs, rtol, atol)
	elif a != b:
		diffs.append((path, a, b))


# Differences that are deliberate fixes of Morinus 6.2 bugs, so the reference
# (made with Morinus 6.2) is kept as it was: (case prefix, path suffix, value
# in the reference, accepted values now, the fix)
FIXES = (
	('transits/', '/pltretr', '-1', ('0', '1'), 'retrograde transits were never marked (commit 139c2c6)'),
)


def fixed(case, path, a, b):
	for prefix, suffix, old, new, why in FIXES:
		if case.startswith(prefix) and path.endswith(suffix) and str(a) == old and str(b) in new:
			return why
	return None


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
		fixes = [(p, a, b, fixed(case, p, a, b)) for p, a, b in diffs]
		for p, a, b, why in fixes:
			if why:
				print('fixed %s%s: %r -> %r (%s)' % (case, p, a, b, why))
		diffs = [(p, a, b) for p, a, b, why in fixes if not why]
		if diffs:
			failed += 1
			print('FAIL %s (%d differences)' % (case, len(diffs)))
			for p, a, b in diffs[:args.max]:
				print('    %s: %r != %r' % (p, str(a)[:200], str(b)[:200]))

	print('%d/%d cases differ' % (failed, len(set(ref) | set(port))))
	sys.exit(1 if failed else 0)


if __name__ == '__main__':
	main()

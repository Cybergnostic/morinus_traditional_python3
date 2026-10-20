"""Checks the results of guismoke.py for continuous integration: fails on any error
except the known ones of the original program, and reports clipped controls as
warnings (GitHub shows ::warning:: lines as annotations).

    python3 tests/check_smoke.py <outdir>/guismoke.json
"""

import sys
import json

# bugs of the original program that are kept (README, Known issues)
KNOWN = [
	('print2file', 'saving Campanian primary directions as text'),
]


def main():
	with open(sys.argv[1], encoding='utf-8') as f:
		res = json.load(f)
	new = []
	for e in res.get('errors', []):
		known = next((why for text, why in KNOWN if text in e['traceback']), None)
		if known:
			print('known: %s (%s)' % (e['step'], known))
		else:
			new.append(e)
	for c in res.get('clipped', []):
		print('::warning::clipped %s in %s: "%s" is %s, needs %s' % (c['control'], c['window'], c['text'], c['size'], c['needs']))
	for e in new:
		print('::error::%s / %s' % (e['step'], e['where']))
		print(e['traceback'])
	print('%d errors (%d known), %d clipped controls' % (len(res.get('errors', [])), len(res.get('errors', [])) - len(new), len(res.get('clipped', []))))
	sys.exit(1 if new else 0)


if __name__ == '__main__':
	main()

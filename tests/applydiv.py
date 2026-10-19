# Applies guismoke.py --trace-div results: rewrites '/' to '//' at division
# sites that only ever saw two ints (which floor-divided under Python 2).
# Sites that saw both ints and floats are reported for manual review.
#   python3 applydiv.py <morinus-dir> <guismoke.json> [...]

import os
import ast
import sys
import json


def main():
	mdir = sys.argv[1]
	sites = {}
	for fn in sys.argv[2:]:
		for site, kinds in json.load(open(fn)).get('divsites', {}).items():
			sites.setdefault(site, set()).update(kinds)

	byfile = {}
	for site, kinds in sites.items():
		fname, line, col = site.rsplit(':', 2)
		if kinds == {'int'}:
			byfile.setdefault(fname, set()).add((int(line), int(col)))
		elif 'int' in kinds:
			print('MIXED (review by hand): %s' % site)

	total = 0
	for fname, locs in sorted(byfile.items()):
		path = os.path.join(mdir, fname)
		src = open(path, encoding='utf-8').read()
		lines = src.split('\n')
		edits = []
		for node in ast.walk(ast.parse(src)):
			if isinstance(node, (ast.BinOp, ast.AugAssign)) and isinstance(node.op, ast.Div) and (node.lineno, node.col_offset) in locs:
				left = node.left if isinstance(node, ast.BinOp) else node.target
				l, c = left.end_lineno, left.end_col_offset
				# find the operator after the left operand (skipping spaces, closing parens, line breaks)
				while True:
					text = lines[l-1]
					while c < len(text) and text[c] in ' \t)':
						c += 1
					if c < len(text):
						break
					l, c = l+1, 0
				assert text[c] == '/' and text[c+1:c+2] != '/', (fname, node.lineno, text)
				edits.append((l, c))
		for l, c in sorted(edits, reverse=True):
			lines[l-1] = lines[l-1][:c]+'//'+lines[l-1][c+1:]
		open(path, 'w', encoding='utf-8').write('\n'.join(lines))
		total += len(edits)
		print('%s: %d' % (fname, len(edits)))
	print('%d divisions changed to //' % total)


if __name__ == '__main__':
	main()

"""Merges lots into a Morinus settings folder: the existing lots stay first and in
order (lot 1 is Fortune; topical almutens refer to lots by number), then the
Solar Fire lots are appended unless the same lot already exists: the same formula under the same name (ignoring diacritics, case,
punctuation and parenthesised source notes). Different lots that share a
formula (e.g. "Tacka zivota" and "Deca (Hermes)") are all kept, since the
sources give them different meanings. References to other lots are compared by
the formula they point to, not by number. A new lot whose name matches an
existing lot with another formula gets a source tag, e.g. "Razvod (SF)".
New lots are added unticked, so the Lots table shows what it did before until
you tick them.

    python3 tools/merge_lots.py --arp file.arp [--dry-run]
"""

import argparse
import os
import re
import sys
import unicodedata

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
os.chdir(ROOT)

import options	# noqa: E402
import arp_lots	# noqa: E402
from lots import Lots as L	# noqa: E402

def key(lots, i, seen=()):
    """Comparable formula of lot i (0-based), with references replaced by the referenced formula."""
    if i in seen:
        raise ValueError('circular lot references')
    name, codes, refordegs, reverse = lots[i][:4]
    terms = []
    for c, r in zip(codes, refordegs):
        if c in (L.REF, L.REFLORD):
            terms.append((c, key(lots, r-1, seen+(i,))))
        elif c in (L.DEG, L.DEGLORD):
            terms.append((c, r))
        else:
            terms.append((c,))
    return (tuple(terms), bool(reverse))


def norm(name):
    name = name.replace('đ', 'dj').replace('Đ', 'Dj')
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower().replace('herm.', 'hermes')
    return re.sub(r'[^a-z0-9]', '', name)


def base(name):
    return norm(re.sub(r'\(.*?\)', '', name))


def same_name(a, b):
    return norm(a) == norm(b) or base(a) == base(b)


def unique_name(name, names, tag):
    """Adds a source tag if the name is taken."""
    taken = any(norm(name) == norm(n) for n in names)
    if not taken:
        return name
    n = '%s (%s)' % (name, tag)
    k = 2
    while n in names:
        n = '%s (%s %d)' % (name, tag, k)
        k += 1
    return n


def add(merged, visible, new, tag, report):
    """Appends lots from one source; new is a list of lots numbered 1.. among themselves.
    Returns the mapping from their numbers to merged numbers."""
    keys = {}
    for i in range(len(merged)):
        keys.setdefault(key(merged, i), []).append(i+1)
    names = set(l[0] for l in merged)
    mapping = {}
    for n, lot in enumerate(new, 1):
        name, codes, refordegs, reverse = lot[:4]
        refordegs = tuple(mapping[r] if c in (L.REF, L.REFLORD) else r for c, r in zip(codes, refordegs))
        candidate = merged+[[name, tuple(codes), refordegs, bool(reverse)]]
        k = key(candidate, len(merged))
        same = [m for m in keys.get(k, []) if same_name(merged[m-1][0], name)]
        if same:
            mapping[n] = same[0]
            report.append('  = %-28s same as %d. %s' % (name, same[0], merged[same[0]-1][0]))
            continue
        name = unique_name(name, names, tag)
        merged.append([name, tuple(codes), refordegs, bool(reverse)])
        visible.append(False)
        names.add(name)
        mapping[n] = len(merged)
        keys.setdefault(k, []).append(len(merged))
        report.append('  + %-28s %d.' % (name, len(merged)))
    return mapping


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--arp', required=True, help='Solar Fire Arabic parts file')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    o = options.Options()
    merged = [list(l[:4]) for l in o.lots]
    visible = list(o.lotsvisible)
    report = ['Existing: %d lots' % len(merged)]
    converted, ref, notes = arp_lots.convert(arp_lots.read_arp(args.arp))
    report.append('Solar Fire (%s): %d lots' % (os.path.basename(args.arp), len(converted)))
    report += ['  note: '+n for n in notes]
    add(merged, visible, converted, 'SF', report)
    report.append('Result: %d lots (%d new)' % (len(merged), len(merged)-len(o.lots)))
    print('\n'.join(report))
    if not args.dry_run:
        o.lots = [tuple(l) for l in merged]	# as the lots dialog stores them
        o.lotsvisible = visible
        if not o.saveTopicalandLots():
            sys.exit(1)
        print('saved to', o.topicalandlotsopt)


if __name__ == '__main__':
    main()

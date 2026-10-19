"""Reads Solar Fire Arabic-parts files (.arp) into Morinus lot definitions.

Each .arp line is
    baseType,baseId,baseDeg, addType,addId,addDeg, subType,subId,subDeg, sect, "name", "short"
meaning  base + add - sub,  where sect is 0 (always), 1 (day formula) or 2 (night formula).
Term types: 0 fixed zodiacal degree (id = sign, 1 = Aries; deg = degrees into the sign),
1 body or angle, 2 ruler of a body's sign, 3 house cusp, 4 ruler of a house cusp,
5 another part of the file (id = its 1-based line number), 6 special point (5 = prenatal syzygy).

A day line and a night line with the same name whose night formula is the day
formula with the added and subtracted terms swapped become one Morinus lot that
reverses at night, which is how Morinus stores such lots.
"""

import csv
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lots import Lots	# noqa: E402

BODIES = {1: Lots.MOON, 3: Lots.SUN, 5: Lots.MERCURY, 6: Lots.VENUS, 7: Lots.MARS, 8: Lots.JUPITER, 9: Lots.SATURN,
          22: Lots.ASC, 23: Lots.MC, 39: Lots.DESC}
BODY_LORDS = {Lots.SATURN: Lots.SATURNLORD, Lots.JUPITER: Lots.JUPITERLORD, Lots.MARS: Lots.MARSLORD, Lots.SUN: Lots.SUNLORD,
              Lots.VENUS: Lots.VENUSLORD, Lots.MERCURY: Lots.MERCURYLORD, Lots.MOON: Lots.MOONLORD}


class ArpError(ValueError):
    pass


def read_arp(path):
    """Rows as (name, [(type, id, deg) x3], sect) in file order."""
    rows = []
    with open(path, newline='', encoding='latin-1') as f:
        for n, rec in enumerate(csv.reader(f), 1):
            if not rec:
                continue
            nums = [int(x) for x in rec[:10]]
            rows.append((rec[10], [tuple(nums[0:3]), tuple(nums[3:6]), tuple(nums[6:9])], nums[9]))
    return rows


def term(t, ref):
    """Morinus (code, refordeg) for one .arp term; ref maps .arp line numbers to Morinus lot numbers."""
    typ, ident, deg = t
    if typ == 0:
        return Lots.DEG, (ident-1)*30+deg
    if deg != 0:
        raise ArpError('degree offset on a non-degree term %r' % (t,))
    if typ == 1:
        if ident not in BODIES:
            raise ArpError('unknown body %d' % ident)
        return BODIES[ident], 0
    if typ == 2:
        if BODIES.get(ident) not in BODY_LORDS:
            raise ArpError('no sign ruler for body %d' % ident)
        return BODY_LORDS[BODIES[ident]], 0
    if typ == 3:
        return Lots.ASC+ident-1, 0
    if typ == 4:
        return Lots.ASCLORD+ident-1, 0
    if typ == 5:
        if ident not in ref:
            raise ArpError('reference to line %d, which is not an earlier part' % ident)
        return Lots.REF, ref[ident]
    if typ == 6 and ident == 5:
        return Lots.SYZ, 0
    raise ArpError('unsupported term %r' % (t,))


def convert(rows, first_number=1):
    """Morinus lots [name, (b, a, s), (rb, ra, rs), reverse_at_night] for .arp rows.

    first_number is the Morinus number the first converted lot will get, for
    references between lots. Returns (lots, ref, notes): ref maps .arp line
    numbers to Morinus lot numbers.
    """
    lots, ref, notes = [], {}, []
    used = set()
    for i, (name, terms, sect) in enumerate(rows):
        line = i+1
        if line in used:
            continue
        codes = [term(t, ref) for t in terms]
        reverse = False
        if sect == 1:
            # look for the matching night line
            for j in range(i+1, len(rows)):
                if rows[j][0] == name and rows[j][2] == 2:
                    night = rows[j][1]
                    kind = _pair_kind(rows, terms, night)
                    if kind == 'reversed':
                        reverse = True
                    elif kind == 'luminary':
                        codes = [_luminary_of_time(term(d, ref), d, n) for d, n in zip(terms, night)]
                    if kind is not None:
                        used.add(j+1)
                        ref[j+1] = first_number+len(lots)
                        sect = 0
                    else:
                        notes.append('%s: day and night formulas differ beyond reversal; kept as two lots' % name)
                    break
        elif sect == 2:
            name = name+' noć' if any(r[0] == name and r[2] == 1 for r in rows) else name
        if sect == 1:
            name = name+' dan'
        ref[line] = first_number+len(lots)
        lots.append([name, tuple(c for c, d in codes), tuple(d for c, d in codes), reverse])
    return lots, ref, notes


# Sun by day / Moon by night, as Solar Fire writes it with two lines
SUN_TERMS = {(1, 3, 0): (1, 1, 0), (2, 3, 0): (2, 1, 0)}


def _pair_kind(rows, day, night):
    """How a night line relates to its day line: 'reversed' (add and subtract swapped),
    'same' (identical; referenced parts may be the night line of the part the day
    line references), 'luminary' (Sun terms by day are Moon terms by night), or None."""
    def same(a, b):
        if a == b:
            return True
        if a[0] == 5 and b[0] == 5:
            ra, rb = rows[a[1]-1], rows[b[1]-1]
            return ra[0] == rb[0] and {ra[2], rb[2]} == {1, 2}
        return False
    if same(day[0], night[0]) and same(day[1], night[2]) and same(day[2], night[1]):
        return 'reversed'
    if all(same(d, n) for d, n in zip(day, night)):
        return 'same'
    if all(same(d, n) or SUN_TERMS.get(d) == n for d, n in zip(day, night)) and any(SUN_TERMS.get(d) == n for d, n in zip(day, night)):
        return 'luminary'
    return None


def _luminary_of_time(code, d, n):
    """Replaces a Sun / ruler-of-Sun term that becomes Moon / ruler-of-Moon at night by
    Morinus's luminary of the time (or its ruler)."""
    if SUN_TERMS.get(d) != n:
        return code
    return (Lots.LTI, 0) if d[0] == 1 else (Lots.LTILORD, 0)


if __name__ == '__main__':
    rows = read_arp(sys.argv[1])
    lots, ref, notes = convert(rows)
    for n, l in enumerate(lots, 1):
        print(n, l)
    print(len(rows), 'lines ->', len(lots), 'lots')
    for n in notes:
        print('NOTE', n)

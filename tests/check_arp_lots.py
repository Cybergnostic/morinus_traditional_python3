"""Checks tools/arp_lots.py: every Solar Fire line evaluated directly from its codes
must equal the lot Morinus computes from the converted definitions, for a day
and a night chart.
    python3 tests/check_arp_lots.py file.arp
"""

import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
os.chdir(ROOT)

import astrology	# noqa: E402
import chart	# noqa: E402
import options	# noqa: E402
import planets	# noqa: E402
import lots	# noqa: E402
import arp_lots	# noqa: E402

astrology.swe_set_ephe_path(os.path.join('SWEP', 'Ephem'))

P = planets.Planets
# domicile ruler of each sign, Aries..Pisces
RULERS = [P.MARS, P.VENUS, P.MERCURY, P.MOON, P.SUN, P.MERCURY, P.VENUS, P.MARS, P.JUPITER, P.SATURN, P.SATURN, P.JUPITER]
# Solar Fire body numbers
BODY = {1: P.MOON, 3: P.SUN, 5: P.MERCURY, 6: P.VENUS, 7: P.MARS, 8: P.JUPITER, 9: P.SATURN}


def direct(rows, ch, line):
    """Value of an .arp line straight from its codes (independent of the converter)."""
    name, terms, sect = rows[line-1]
    asc = ch.houses.ascmc[0]
    mc = ch.houses.ascmc[1]
    cusp = lambda n: {1: asc, 4: (mc+180.0) % 360.0, 7: (asc+180.0) % 360.0, 10: mc}.get(n, ch.houses.cusps[n])
    pl = lambda i: ch.planets.planets[i].data[planets.Planet.LON]
    ruler = lambda lon: pl(RULERS[int(lon // 30)])

    def val(t):
        typ, ident, deg = t
        if typ == 0:
            return (ident-1)*30.0+deg
        if typ == 1:
            return {22: asc, 23: mc, 39: (asc+180.0) % 360.0}.get(ident) if ident in (22, 23, 39) else pl(BODY[ident])
        if typ == 2:
            return ruler(pl(BODY[ident]))
        if typ == 3:
            return cusp(ident)
        if typ == 4:
            return ruler(cusp(ident))
        if typ == 5:
            return direct(rows, ch, ident)
        if typ == 6:
            return ch.syzygy.lon
        raise ValueError(t)
    b, a, s = (val(t) for t in terms)
    return (b+a-s) % 360.0


def check(path, ch, night):
    rows = arp_lots.read_arp(path)
    converted, ref, notes = arp_lots.convert(rows)
    o = ch.options
    o.lots = [list(l) for l in converted]
    o.lotsref = 0
    o.lotsusehouses = False
    abovehor = not night
    computed = lots.Lots(o.lots, ch.houses.ascmc, ch.planets, ch.houses, ch.houses.cusps, ch.syzygy, ch.time.ph.planetaryhour, o, abovehor, ch.ayanamsha)
    bad = 0
    for line, (name, terms, sect) in enumerate(rows, 1):
        if sect == (1 if night else 2):
            continue	# the other sect's line
        expected = direct(rows, ch, line)
        got = computed.lots[ref[line]-1][lots.Lots.LON]
        diff = abs((got-expected+180.0) % 360.0-180.0)
        if diff > 1e-9:
            bad += 1
            print('MISMATCH %s line %d %s: Solar Fire %.6f, Morinus %.6f' % ('night' if night else 'day', line, name, expected, got))
    return bad


def main():
    o = options.Options()
    place = chart.Place('Nis', 21, 54, 0, True, 43, 19, 0, True, 195)
    bad = 0
    for hour, night in ((14, False), (2, True)):
        t = chart.Time(1990, 3, 11, hour, 20, 0, False, chart.Time.GREGORIAN, chart.Time.ZONE, True, 1, 0, False, place)
        ch = chart.Chart('test', True, t, place, chart.Chart.RADIX, '', o)
        sun_up = ch.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].abovehorizon
        assert sun_up != night, 'test chart has the wrong sect'
        bad += check(sys.argv[1], ch, night)
    print('all .arp lines match' if bad == 0 else '%d mismatches' % bad)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()

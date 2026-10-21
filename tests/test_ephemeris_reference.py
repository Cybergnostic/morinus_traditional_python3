"""The ephemeris and lunation finders against published 2024 values, with the
real Swiss Ephemeris (skipped where the extension is not built)."""
import os
import unittest

try:
    import astrology
except ImportError:
    astrology = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jd(y, m, d, h, mi):
    return astrology.swe_julday(y, m, d, h + mi / 60.0, astrology.SE_GREG_CAL)


@unittest.skipIf(astrology is None, 'sweastrology extension not built')
class EphemerisReferenceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        astrology.swe_set_ephe_path(os.path.join(ROOT, 'SWEP', 'Ephem'))

    def assertNear(self, found, expected, minutes=3):
        self.assertLess(abs(found - expected) * 24 * 60, minutes, (found, expected))

    def test_stations_2024(self):
        import ephemerisdata
        import options
        data = ephemerisdata.year_from_swiss(2024, options.Options())
        stations = [(e.planet, e.detail, e.jd) for e in data.events if e.kind == 'Station']
        mercury = ephemerisdata.PLANETS.index('Mercury')
        saturn = ephemerisdata.PLANETS.index('Saturn')
        for planet, detail, when in ((mercury, 'Station direct', jd(2024, 1, 2, 3, 7)),
                                     (mercury, 'Station retrograde', jd(2024, 4, 1, 22, 14)),
                                     (mercury, 'Station direct', jd(2024, 4, 25, 12, 54)),
                                     (saturn, 'Station retrograde', jd(2024, 6, 29, 19, 7))):
            found = [t for p, d, t in stations if p == planet and d == detail and abs(t - when) < 1]
            self.assertEqual(len(found), 1, (ephemerisdata.PLANETS[planet], detail))
            self.assertNear(found[0], when)

    def test_ingress_2024(self):
        import ephemerisdata
        import options
        data = ephemerisdata.year_from_swiss(2024, options.Options())
        sun = ephemerisdata.PLANETS.index('Sun')
        aries = [e.jd for e in data.events if e.planet == sun and e.detail == 'Ingress Aries']
        self.assertEqual(len(aries), 1)
        self.assertNear(aries[0], jd(2024, 3, 20, 3, 6))	# March equinox

    def test_lunations_2024(self):
        import lunationnav
        events = lunationnav.find_events(jd(2024, 3, 25, 0, 0), lunationnav.ephemeris_sampler(), 30)
        expected = (('New Moon', jd(2024, 3, 10, 9, 0)), ('Full Moon', jd(2024, 3, 25, 7, 0)),
                    ('New Moon', jd(2024, 4, 8, 18, 21)), ('Full Moon', jd(2024, 4, 23, 23, 49)))
        for kind, when in expected:
            found = [t for t, k, s, m in events if k == kind and abs(t - when) < 1]
            self.assertEqual(len(found), 1, (kind, when))
            self.assertNear(found[0], when)
        # one event per lunation: about 29.5 days between events of a kind
        news = [t for t, k, s, m in events if k == 'New Moon']
        self.assertTrue(all(29 < b - a < 30 for a, b in zip(news, news[1:])), news)


if __name__ == '__main__':
    unittest.main()

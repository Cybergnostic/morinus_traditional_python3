"""The transit search finds Morinus's own exact transits (transits.Transits) over
a span of months: two transits of its sample chart in February 1583, as the
Exact transits table of Morinus 6 lists them."""
import os
import pickle
import unittest

try:
    import astrology
except ImportError:
    astrology = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@unittest.skipIf(astrology is None, 'sweastrology extension not built')
class TransitSearchTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import wx
        cls.app = wx.App(False)
        import chart
        import common
        import options
        common.common = common.Common()
        astrology.swe_set_ephe_path(os.path.join(ROOT, 'SWEP', 'Ephem'))
        with open(os.path.join(ROOT, 'Hors', 'Morinus.hor'), 'rb') as f:
            v = [pickle.load(f, encoding='utf-8') for _ in range(27)]
        (name, male, htype, bc, year, month, day, hour, minute, second, cal, zt, plus, zh, zm, dst,
         place, deglon, minlon, seclon, east, deglat, minlat, seclat, north, alt, notes) = v
        pl = chart.Place(place, deglon, minlon, seclon, east, deglat, minlat, seclat, north, alt)
        cls.radix = chart.Chart(name, male, chart.Time(year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, dst, pl),
                                pl, htype, notes, options.Options())

    def search(self, **kw):
        import transitsearch as ts
        args = dict(planets_=set(range(6)), aspects=set(range(5)), targets={t for t, label in ts.TARGETS})
        args.update(kw)
        return ts.search(self.radix, (1583, 2), (1583, 2), **args)

    def find(self, results, text):
        import transitsearch as ts
        return [(jd, tr) for jd, tr in results if ts.describe(tr) == text]

    def test_morinus_transits_of_february_1583(self):
        import transitsearch as ts
        results = self.search()
        for text, day, h, m, s in (('Jupiter enters Pisces', 3, 19, 56, 38), ('Mercury square the Ascendant', 5, 1, 49, 23)):
            found = self.find(results, text)
            self.assertEqual(len(found), 1, text)
            tr = found[0][1]
            self.assertEqual(tr.day, day)
            self.assertLess(abs(tr.time - (h + m / 60.0 + s / 3600.0)) * 3600, 2, text)
        self.assertEqual([jd for jd, tr in results], sorted(jd for jd, tr in results))

    def test_filters(self):
        import transitsearch as ts
        T = ts.transits.Transit
        only_sun = self.search(planets_={3}, aspects={0}, targets={T.PLANET, T.ASCMC})
        self.assertTrue(only_sun)
        self.assertTrue(all(tr.plt == 3 and tr.aspect == 0 and tr.objtype in (T.PLANET, T.ASCMC) for jd, tr in only_sun))
        ingresses = self.search(aspects=set(), targets={T.SIGN})
        self.assertTrue(self.find(ingresses, 'Jupiter enters Pisces'))


if __name__ == '__main__':
    unittest.main()

"""The traditional aspect matrix of a real chart judges whole-sign relations in
the chart's own zodiac (skipped where the extension is not built)."""
import os
import unittest

try:
    import astrology
except ImportError:
    astrology = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@unittest.skipIf(astrology is None, 'sweastrology extension not built')
class SiderealAspectMatrixTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        astrology.swe_set_ephe_path(os.path.join(ROOT, 'SWEP', 'Ephem'))
        import tradoptions
        cls.saved = tradoptions.values()
        tradoptions.set(dict(tradoptions.DEFAULTS))  # traditional preset

    @classmethod
    def tearDownClass(cls):
        import tradoptions
        tradoptions.set(cls.saved)

    def make(self, ayanamsha):
        import chart
        import options
        opts = options.Options()
        opts.ayanamsha = ayanamsha
        place = chart.Place('Budapest', 19, 3, 0, True, 47, 29, 0, True, 100)
        time = chart.Time(1990, 4, 21, 12, 0, 0, False, chart.Time.GREGORIAN,
                          chart.Time.GREENWICH, True, 0, 0, False, place)
        return chart.Chart('sidereal', True, time, place, chart.Chart.RADIX,
                           '', opts, False)

    def test_sign_relations_use_sidereal_signs(self):
        import traditional_aspects as ta
        chrt = self.make(2)  # Lahiri
        shift = chrt.ayanamsha
        self.assertGreater(shift, 20)
        lon = [p.data[0] for p in chrt.planets.planets[:7]]
        checked = 0
        for i in range(7):
            for j in range(i):
                cell = chrt.aspmatrix[i][j]
                expected = ta.evaluate(lon[i] - shift, lon[j] - shift,
                                       0, 0, ta.COURSE_ORBS[i], ta.COURSE_ORBS[j])
                self.assertEqual(cell.typ, expected.index if expected else -1,
                                 (ta.PLANETS[i], ta.PLANETS[j]))
                if ta.sign_configuration(lon[i], lon[j]) != \
                        ta.sign_configuration(lon[i] - shift, lon[j] - shift):
                    checked += 1
        # This date has pairs whose tropical and sidereal sign relations differ.
        self.assertGreater(checked, 0)

    def test_tropical_matrix_unchanged(self):
        import traditional_aspects as ta
        chrt = self.make(0)
        lon = [p.data[0] for p in chrt.planets.planets[:7]]
        for i in range(7):
            for j in range(i):
                expected = ta.evaluate(lon[i], lon[j], 0, 0,
                                       ta.COURSE_ORBS[i], ta.COURSE_ORBS[j])
                self.assertEqual(chrt.aspmatrix[i][j].typ,
                                 expected.index if expected else -1)


if __name__ == '__main__':
    unittest.main()

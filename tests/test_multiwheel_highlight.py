"""Unit tests for Morinus time-lord highlighting (no wx GUI required)."""
import unittest
from datetime import datetime
from types import SimpleNamespace

import firdaria
import multiwheel_highlight as highlight


def fake_radix(day=True, bonatti=False, birth=(2000, 1, 1)):
    opt = SimpleNamespace(isfirbonatti=bonatti)
    obj = SimpleNamespace(
        options=opt, abovehorizonwithorb=day, htype=0,
        time=SimpleNamespace(origyear=birth[0], origmonth=birth[1],
                             origday=birth[2], bc=False))
    obj.firdaria = firdaria.Firdaria(*birth, opt, day)
    return obj


class TimeLordHighlightTests(unittest.TestCase):
    def test_traditional_domicile_rulers(self):
        self.assertEqual(highlight.DOMICILE,
                         (2, 4, 5, 6, 3, 5, 4, 2, 1, 0, 0, 1))
        for sign, expected in enumerate(highlight.DOMICILE):
            sr = SimpleNamespace(
                houses=SimpleNamespace(ascmc=[sign * 30 + 10]),
                ayanamsha=0)
            self.assertEqual(highlight.solar_asc_ruler(sr), expected)

    def test_firdaria_day_major_and_sub_boundaries(self):
        natal = fake_radix()
        self.assertEqual(highlight.at_firdaria(
            natal, datetime(2000, 1, 1)), (3, 3))
        self.assertEqual(highlight.at_firdaria(
            natal, datetime(2002, 1, 1)), (3, 4))
        self.assertEqual(highlight.at_firdaria(
            natal, datetime(2010, 1, 1)), (4, 4))
        self.assertIsNone(highlight.at_firdaria(
            natal, datetime(1999, 12, 31)))

    def test_nocturnal_options_match_existing_morinus_order(self):
        biruni = fake_radix(day=False)
        bonatti = fake_radix(day=False, bonatti=True)
        # Bonatti puts the nodes between Mars and the Sun; Al-Biruni
        # places them at the end of the sequence.
        self.assertEqual(highlight.at_firdaria(
            biruni, datetime(2000, 1, 1))[0], 6)
        self.assertEqual(highlight.at_firdaria(
            bonatti, datetime(2000, 1, 1))[0], 6)
        self.assertEqual(highlight.at_firdaria(
            biruni, datetime(2040, 1, 1))[0], 3)
        self.assertEqual(highlight.at_firdaria(
            bonatti, datetime(2040, 1, 1))[0], 7)

    def test_node_major_has_no_subperiod(self):
        natal = fake_radix()
        self.assertEqual(highlight.at_firdaria(
            natal, datetime(2070, 1, 1)), (7, None))

    def test_solar_asc_and_house_use_own_chart(self):
        def make_chart(htype, asc, positions):
            cusps = (0.0,) + tuple(float(i * 30) for i in range(12))
            return SimpleNamespace(
                htype=htype, ayanamsha=0,
                houses=SimpleNamespace(ascmc=[asc], cusps=cusps),
                planets=SimpleNamespace(
                    planets=[SimpleNamespace(data=(x,)) for x in positions]))
        radix = make_chart(0, 4.0, [15.0] * 9)
        radix.options = SimpleNamespace(isfirbonatti=False)
        radix.time = SimpleNamespace(
            origyear=2000, origmonth=1, origday=1, bc=False)
        radix.abovehorizonwithorb = True
        radix.firdaria = firdaria.Firdaria(2000, 1, 1, radix.options, True)
        solar = make_chart(1, 189.0, [1.0, 1.0, 1.0, 1.0,
                                      192.0, 1.0, 1.0, 1.0, 1.0])
        marks = highlight.entries_for(
            radix, [solar, make_chart(4, 0.0, [1.0]*9)],
            datetime(2002, 1, 1))
        self.assertEqual([(m['ring'], m['planet'], m['role'])
                          for m in marks],
                         [(0, 3, 'major'), (0, 4, 'sub'),
                          (1, 4, 'solar_asc')])
        self.assertEqual(marks[-1]['house'], 7)
        self.assertIn('H7', marks[-1]['text'])

    def test_sidereal_solar_rulership(self):
        sr = SimpleNamespace(
            ayanamsha=25, houses=SimpleNamespace(ascmc=[30.0]))
        self.assertEqual(highlight.solar_asc_ruler(sr, False), 4)
        self.assertEqual(highlight.solar_asc_ruler(sr, True), 2)


if __name__ == '__main__':
    unittest.main()

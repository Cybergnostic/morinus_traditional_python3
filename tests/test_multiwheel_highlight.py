"""Pure tests for twelve-period course profections + Morinus Firdaria."""
import unittest
from datetime import datetime
from types import SimpleNamespace as NS

import firdaria
import multiwheel_highlight as h


def make_chart(kind=0, asc=0, name='Test', birth=(2000, 1, 1),
               day=True, biruni=True, ayan=0):
    opts = NS(isfirbonatti=not biruni)
    cusps = (0.0,) + tuple((asc // 30 * 30 + i * 30) % 360
                           for i in range(12))
    obj = NS(
        name=name, htype=kind, options=opts,
        abovehorizonwithorb=day,
        time=NS(origyear=birth[0], origmonth=birth[1],
                origday=birth[2], bc=False),
        houses=NS(ascmc=[asc], cusps=cusps),
        ayanamsha=ayan,
    )
    obj.firdaria = firdaria.Firdaria(*birth, opts, day)
    return obj


class ProfectionHighlightTests(unittest.TestCase):
    def test_twelve_traditional_sign_rulers(self):
        self.assertEqual(h.DOMICILE, (2, 4, 5, 6, 3, 5, 4, 2, 1, 0, 0, 1))
        self.assertEqual(set(h.SECTOR_COLOURS), {'annual', 'monthly'})
        self.assertEqual(set(h.ROLE_COLOURS),
                         {'annual', 'monthly', 'major', 'sub'})

    def test_annual_asc_and_age_cycle(self):
        radix = make_chart(asc=65)  # Gemini rising
        self.assertEqual(h.annual_profection(radix, 2000), (2, 5, 1, 0))
        self.assertEqual(h.annual_profection(radix, 2001), (3, 6, 2, 1))
        self.assertEqual(h.annual_profection(radix, 2012), (2, 5, 1, 12))
        self.assertEqual(h.annual_profection(radix, 1999), None)

    def test_sidereal_asc_sign(self):
        radix = make_chart(asc=30, ayan=25)
        self.assertEqual(h.annual_profection(radix, 2000, False)[0], 1)
        self.assertEqual(h.annual_profection(radix, 2000, True)[0], 0)

    def test_twelve_equal_intervals_and_exact_boundaries(self):
        start, end = 2500000.0, 2500365.2422
        duration = (end - start) / 12
        self.assertEqual(h.monthly_index(start, end, start - 15), 0)
        self.assertEqual(h.monthly_index(start, end, start), 0)
        self.assertEqual(h.monthly_index(start, end, start + duration * 0.95), 0)
        self.assertEqual(h.monthly_index(start, end, start + duration * 1.01), 1)
        self.assertEqual(h.monthly_index(start, end, start + duration * 7.01), 7)
        self.assertEqual(h.monthly_index(start, end, end - 0.1), 11)
        self.assertEqual(h.monthly_index(start, end, end), 11)
        self.assertEqual(h.monthly_index(start, start, start), None)

    def test_annual_sign_in_every_chart_monthly_only_sr_and_lr(self):
        radix = make_chart(asc=0)
        sr = make_chart(kind=1, asc=91)
        lr = make_chart(kind=2, asc=213)
        transit = make_chart(kind=4, asc=40)
        out = h.entries_for(radix, [sr, lr, transit],
                            datetime(2027, 5, 1), solar_year=2027,
                            solar_start_jd=2500000,
                            next_solar_jd=2500365.2422,
                            monthly_date_jd=2500092)
        self.assertEqual(out['annual_sign'], 3)  # 27 annual steps = Cancer
        self.assertEqual(out['month_index'], 3)
        self.assertEqual(out['monthly_sign'], 6)  # Libra
        self.assertEqual([a['ring'] for a in out['areas']
                          if a['role'] == 'annual'], [0, 1, 2, 3])
        self.assertEqual([a['ring'] for a in out['areas']
                          if a['role'] == 'monthly'], [1, 2])
        annual_marks = [m for m in out['marks'] if m['role'] == 'annual']
        self.assertEqual([m['planet'] for m in annual_marks], [6] * 4)
        month_marks = [m for m in out['marks'] if m['role'] == 'monthly']
        self.assertEqual([(m['ring'], m['planet']) for m in month_marks],
                         [(1, 4), (2, 4)])
        self.assertFalse(any(a['role'] in ('major', 'sub')
                             for a in out['areas']))
        self.assertFalse(any(a['role'] == 'solar_asc'
                             for a in out['areas'] + out['marks']))

    def test_month_one_coincidence_two_distinct_roles(self):
        radix = make_chart(asc=0)
        sr = make_chart(kind=1, asc=110)
        out = h.entries_for(radix, [sr], datetime(2012, 4, 1),
                            solar_year=2012, solar_start_jd=10,
                            next_solar_jd=375, monthly_date_jd=10)
        areas = [a for a in out['areas'] if a['ring'] == 1]
        self.assertEqual(areas[0]['sign'], areas[1]['sign'])
        self.assertEqual({a['role'] for a in areas}, {'annual', 'monthly'})
        self.assertEqual({m['role'] for m in out['marks'] if m['ring'] == 1
                          and m['planet'] == 2}, {'annual', 'monthly'})
        self.assertEqual([a['house'] for a in areas], [10, 10])

    def test_firdaria_follows_original_schedule(self):
        day = make_chart()
        self.assertEqual(h.at_firdaria(day, datetime(2000, 1, 1)), (3, 3))
        self.assertEqual(h.at_firdaria(day, datetime(2002, 1, 1)), (3, 4))
        self.assertEqual(h.at_firdaria(day, datetime(2010, 1, 1)), (4, 4))
        self.assertEqual(h.at_firdaria(day, datetime(2070, 1, 1)), (7, None))
        biruni = make_chart(day=False)
        bonatti = make_chart(day=False, biruni=False)
        self.assertEqual(h.at_firdaria(biruni, datetime(2040, 1, 1))[0], 3)
        self.assertEqual(h.at_firdaria(bonatti, datetime(2040, 1, 1))[0], 7)
        self.assertIsNone(h.at_firdaria(day, datetime(1999, 1, 1)))

    def test_firdaria_does_not_tint_occupied_planet_houses(self):
        radix = make_chart(asc=15)
        sr = make_chart(kind=1, asc=15)
        data = h.entries_for(radix, [sr], datetime(2010, 1, 2),
                             solar_year=2010, solar_start_jd=10,
                             next_solar_jd=375, monthly_date_jd=80)
        self.assertEqual({a['role'] for a in data['areas']},
                         {'annual', 'monthly'})
        self.assertIn('major', {m['role'] for m in data['marks']})
        self.assertIn('sub', {m['role'] for m in data['marks']})
        self.assertEqual(len(data['legend']), 4)

    def test_no_thirteenth_period(self):
        radix = make_chart(asc=0)
        sr = make_chart(kind=1)
        marks = h.entries_for(radix, [sr], datetime(2012, 12, 1),
                              solar_year=2012, solar_start_jd=0,
                              next_solar_jd=365.0,
                              monthly_date_jd=364.99)
        self.assertEqual(marks['month_index'], 11)
        self.assertEqual(marks['monthly_sign'], (marks['annual_sign'] + 11) % 12)


if __name__ == '__main__':
    unittest.main()

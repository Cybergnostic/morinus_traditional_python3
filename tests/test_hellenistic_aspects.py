"""A4: complete domicile witnessing and single-direction Chaldean rays."""
import unittest
from types import SimpleNamespace

from hellenistic_aspects import (
    analyze_aversions, analyze_rays, directed_ray, overcomes,
    signs_averse, domicile_witnessing, _reflections, SIGN_RULERS,
)
from traditional_aspects import PLANETS
from light_perfection import Connection


def chart(lons=None, speeds=None, asc=45, contacts=(), ayan=0):
    lons = lons if lons is not None else [5, 105, 273, 235, 195, 70, 300]
    speeds = speeds if speeds is not None else [0, 0, 1, .9, 1, 1, 12]
    planets = [SimpleNamespace(data=[lon, 0, 0, speed])
               for lon, speed in zip(lons, speeds)]
    matrix = [[SimpleNamespace(typ=-1) for _ in range(9)]
              for _ in range(9)]
    for first, second, kind in contacts:
        matrix[max(first, second)][min(first, second)].typ = kind
    return SimpleNamespace(
        planets=SimpleNamespace(planets=planets),
        houses=SimpleNamespace(ascmc=[asc]),
        options=SimpleNamespace(ayanamsha=1 if ayan else 0),
        ayanamsha=ayan, aspmatrix=matrix)


def domicile(rows, planet, sign):
    return next(r for r in rows if r.planet == planet and r.domicile == sign)


class DomicileWitnessingTests(unittest.TestCase):
    def test_aversion_second_sixth_eighth_twelfth(self):
        self.assertTrue(all(signs_averse(0, s) for s in (1, 5, 7, 11)))
        self.assertFalse(any(signs_averse(0, s)
                             for s in (0, 2, 3, 4, 6, 8, 9, 10)))

    def test_all_seven_planets_and_all_twelve_domiciles(self):
        rows = analyze_aversions(chart())
        self.assertEqual(len(rows), 12)
        self.assertEqual(set(row.planet for row in rows), set(PLANETS))
        self.assertEqual(len(set(row.domicile for row in rows)), 12)
        self.assertEqual(
            sorted((row.planet, row.domicile) for row in rows),
            sorted((SIGN_RULERS[i], sign) for i, sign in enumerate(
                ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn',
                 'Aquarius', 'Pisces'))))

    def test_ascendant_does_not_influence_domicile_table(self):
        a = analyze_aversions(chart(asc=15))
        b = analyze_aversions(chart(asc=280))
        self.assertEqual(a, b)
        self.assertFalse(any('Ascendant' in row.domicile
                             for row in a))

    def test_all_types_of_sign_witnessing(self):
        expected = {0: 'Co-presence', 2: 'Sextile', 3: 'Square',
                    4: 'Trine', 6: 'Opposition', 8: 'Trine',
                    9: 'Square', 10: 'Sextile',
                    1: 'Averse', 5: 'Averse', 7: 'Averse',
                    11: 'Averse'}
        for step, witness in expected.items():
            self.assertEqual(domicile_witnessing(0, step), witness)

    def test_witnessed_domiciles_have_aspect_and_not_aversion(self):
        rows = analyze_aversions(chart())
        self.assertEqual(domicile(rows, 'Mercury', 'Gemini').witnessing,
                         'Co-presence')
        self.assertEqual(domicile(rows, 'Mercury', 'Virgo').witnessing,
                         'Square')
        self.assertEqual(domicile(rows, 'Sun', 'Leo').witnessing, 'Square')
        for row in rows:
            if row.witnessing != 'Averse':
                self.assertEqual(row.status, 'Witnesses')
                self.assertFalse(row.mitigations)

    def test_venus_libra_to_taurus_is_mitigated_by_co_rulership(self):
        rows = analyze_aversions(chart())
        venus = domicile(rows, 'Venus', 'Taurus')
        self.assertEqual(venus.placement, 'Libra')
        self.assertEqual(venus.witnessing, 'Averse')
        self.assertEqual(venus.status, 'Mitigated')
        self.assertIn('Common domicile ruler: Venus', venus.mitigations)
        self.assertEqual(domicile(rows, 'Venus', 'Libra').status, 'Witnesses')

    def test_saturn_in_capricorn_to_aquarius_co_rulership(self):
        lons = [285, 105, 273, 235, 195, 70, 300]
        rows = analyze_aversions(chart(lons=lons))
        saturn = domicile(rows, 'Saturn', 'Aquarius')
        self.assertEqual(saturn.witnessing, 'Averse')
        self.assertEqual(saturn.status, 'Mitigated')
        self.assertIn('Common domicile ruler: Saturn', saturn.mitigations)
        self.assertEqual(domicile(rows, 'Saturn', 'Capricorn').witnessing,
                         'Co-presence')

    def test_antiscia_sign_and_degree_geometry_remains_separate(self):
        reflections = _reflections(14.25, 165.75)
        self.assertIn('Antiscia (sign)', reflections)
        self.assertIn('Antiscia (degree)', reflections)
        self.assertNotIn('Contra-antiscia (sign)', reflections)
        self.assertIn('Antiscia (sign)', _reflections(2, 150))
        self.assertNotIn('Antiscia (degree)', _reflections(2, 150))

    def test_contra_antiscia_sign_pair(self):
        self.assertIn('Contra-antiscia (sign)', _reflections(15, 345))

    def test_no_fabricated_degree_antiscion_to_sign_midpoint(self):
        lons = [5, 105, 273, 235, 195, 70, 300]
        rows = analyze_aversions(chart(lons=lons))
        for row in rows:
            self.assertFalse(any('(degree)' in method
                                 for method in row.mitigations))

    def test_only_verified_light_mitigates_domicile_aversion(self):
        # Jupiter in Cancer is averse to Sagittarius, occupied by Mars.
        lons = [5, 105, 245, 235, 195, 70, 300]
        ch = chart(lons=lons)
        make = lambda status: Connection(
            'Translation', 'Moon', 'Jupiter', 'Mars',
            'Sextile', 'Trine', status)
        unsupported = domicile(analyze_aversions(ch, [make('Candidate')]),
                               'Jupiter', 'Sagittarius')
        confirmed = domicile(analyze_aversions(ch, [make('Verified')]),
                             'Jupiter', 'Sagittarius')
        self.assertNotIn('Translation via Moon', unsupported.mitigations)
        self.assertIn('Translation via Moon', confirmed.mitigations)

    def test_sidereal_chart_adjusts_planet_sign_only(self):
        ch = chart(ayan=30)
        venus = domicile(analyze_aversions(ch), 'Venus', 'Taurus')
        self.assertEqual(venus.placement, 'Virgo')
        self.assertEqual(venus.witnessing, 'Trine')
        self.assertEqual(venus.status, 'Witnesses')


class DirectedRayTests(unittest.TestCase):
    def test_direction_is_from_named_faster_caster(self):
        self.assertEqual(directed_ray(0, 9), ('Square', 'Dexter'))
        self.assertEqual(directed_ray(9, 0), ('Square', 'Sinister'))
        self.assertEqual(directed_ray(0, 3), ('Square', 'Sinister'))
        self.assertIsNone(directed_ray(0, 6))

    def test_overcoming_from_ninth_tenth_eleventh(self):
        self.assertTrue(overcomes(9, 0))
        self.assertTrue(overcomes(8, 0))
        self.assertTrue(overcomes(10, 0))
        self.assertFalse(overcomes(0, 9))

    def test_only_one_ray_per_pair(self):
        rays = analyze_rays(chart())
        pairs = [frozenset((r.caster, r.target)) for r in rays]
        self.assertEqual(len(pairs), len(set(pairs)))
        self.assertLessEqual(len(rays), 21)
        self.assertTrue(all(PLANETS.index(r.caster) >
                            PLANETS.index(r.target) for r in rays))

    def test_jupiter_mars_uses_mars_even_when_jupiter_moves_faster_today(self):
        ch = chart(lons=[5, 105, 15, 235, 195, 70, 300],
                   speeds=[0, 5, .001, .9, 1, 1, 12],
                   contacts=[(1, 2, 2)])
        rays = [r for r in analyze_rays(ch)
                if {r.caster, r.target} == {'Jupiter', 'Mars'}]
        self.assertEqual(len(rays), 1)
        self.assertEqual((rays[0].caster, rays[0].target),
                         ('Mars', 'Jupiter'))
        self.assertEqual(rays[0].direction, 'Sinister')
        self.assertEqual(rays[0].aspect, 'Square')

    def test_mars_squares_and_overcomes_saturn(self):
        ch = chart(contacts=[(0, 2, 2)])
        rays = [r for r in analyze_rays(ch)
                if {r.caster, r.target} == {'Mars', 'Saturn'}]
        self.assertEqual(len(rays), 1)
        mars = rays[0]
        self.assertEqual(mars.caster, 'Mars')
        self.assertEqual(mars.target, 'Saturn')
        self.assertEqual(mars.direction, 'Sinister')
        self.assertEqual(mars.overcoming, 'Yes')
        self.assertEqual(mars.degree_orb, 2.0)
        self.assertTrue(mars.close_counter_ray)
        self.assertTrue(mars.aktinobolia)

    def test_no_aktinobolia_when_caster_separates(self):
        ch = chart(speeds=[0, 0, -1, .9, 1, 1, 12],
                   contacts=[(0, 2, 2)])
        mars = next(r for r in analyze_rays(ch) if r.caster == 'Mars'
                    and r.target == 'Saturn')
        self.assertTrue(mars.close_counter_ray)
        self.assertFalse(mars.aktinobolia)

    def test_sign_based_ray_outside_degree_orb(self):
        ch = chart(lons=[20, 105, 270, 235, 195, 70, 300])
        mars = next(r for r in analyze_rays(ch) if r.caster == 'Mars'
                    and r.target == 'Saturn')
        self.assertEqual(mars.overcoming, 'Yes')
        self.assertFalse(mars.in_orb)
        self.assertFalse(mars.aktinobolia)

    def test_averse_planet_pair_has_no_ray(self):
        ch = chart(lons=[5, 105, 273, 235, 165, 70, 300])
        rays = analyze_rays(ch)
        self.assertFalse(any({r.caster, r.target} == {'Saturn', 'Venus'}
                             for r in rays))


if __name__ == '__main__':
    unittest.main()

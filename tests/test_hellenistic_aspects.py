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

    def test_venus_libra_to_taurus_is_not_averse_by_co_rulership(self):
        rows = analyze_aversions(chart())
        venus = domicile(rows, 'Venus', 'Taurus')
        self.assertEqual(venus.placement, 'Libra')
        self.assertEqual(venus.witnessing, 'Averse')
        self.assertEqual(venus.status, 'Not averse')
        self.assertIn('Common domicile ruler: Venus', venus.mitigations)
        self.assertEqual(domicile(rows, 'Venus', 'Libra').status, 'Witnesses')

    def test_saturn_in_capricorn_to_aquarius_co_rulership(self):
        lons = [285, 105, 273, 235, 195, 70, 300]
        rows = analyze_aversions(chart(lons=lons))
        saturn = domicile(rows, 'Saturn', 'Aquarius')
        self.assertEqual(saturn.witnessing, 'Averse')
        self.assertEqual(saturn.status, 'Not averse')
        self.assertIn('Common domicile ruler: Saturn', saturn.mitigations)
        self.assertEqual(domicile(rows, 'Saturn', 'Capricorn').witnessing,
                         'Co-presence')

    def test_course_moon_examples_antiscia_and_contra_antiscia(self):
        # The Moon rules Cancer: in Gemini (antiscia) or in Sagittarius
        # (contra-antiscia) it is not averse; in Aquarius it is.
        for lon, status in ((75, 'Not averse'), (255, 'Not averse')):
            rows = analyze_aversions(chart(lons=[5, 105, 273, 235, 195, 70, lon]))
            self.assertEqual(domicile(rows, 'Moon', 'Cancer').status, status, lon)
        rows = analyze_aversions(chart(lons=[5, 105, 273, 235, 195, 70, 315],
                                       asc=130))
        moon = domicile(rows, 'Moon', 'Cancer')
        self.assertIn(moon.status, ('Averse', 'Mitigated'))
        self.assertFalse(any('antiscia' in m.lower() for m in moon.mitigations))

    def test_course_saturn_in_pisces_mediators(self):
        # Saturn in Pisces is averse to Aquarius. Venus (Taurus) and Jupiter
        # (Scorpio) see both Pisces and Aquarius; the Sun in Cancer does not
        # see Aquarius; Mars, Mercury and the Moon are averse to Pisces.
        lons = [345, 220, 130, 100, 40, 95, 140]
        saturn = domicile(analyze_aversions(chart(lons=lons, asc=130)),
                          'Saturn', 'Aquarius')
        self.assertEqual(saturn.status, 'Mitigated')
        self.assertEqual(set(saturn.mitigations),
                         {'Mediator: Jupiter', 'Mediator: Venus'})

    def test_cadent_and_combust_planets_cannot_mediate(self):
        lons = [345, 220, 130, 100, 40, 95, 140]
        # Ascendant in Gemini: Scorpio is the 6th, Taurus the 12th (cadent).
        saturn = domicile(analyze_aversions(chart(lons=lons, asc=70)),
                          'Saturn', 'Aquarius')
        self.assertEqual(saturn.status, 'Averse')
        # Venus combust 5 degrees from the Sun, which itself sees both signs.
        lons = [345, 160, 130, 45, 40, 95, 140]
        saturn = domicile(analyze_aversions(chart(lons=lons, asc=130)),
                          'Saturn', 'Aquarius')
        self.assertEqual(saturn.mitigations, ('Mediator: Sun',))

    def test_co_presence_does_not_mediate(self):
        # Jupiter in Pisces with Saturn sees Aquarius not at all, and
        # co-presence with the averse planet is not a Ptolemaic aspect.
        lons = [345, 350, 130, 100, 160, 95, 140]
        saturn = domicile(analyze_aversions(chart(lons=lons, asc=130)),
                          'Saturn', 'Aquarius')
        self.assertNotIn('Mediator: Jupiter', saturn.mitigations)

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
        # Jupiter in Leo is averse to Pisces (no sign link), occupied by Mars.
        lons = [100, 125, 345, 160, 175, 70, 300]
        ch = chart(lons=lons, asc=130)
        make = lambda status: Connection(
            'Translation', 'Moon', 'Jupiter', 'Mars',
            'Sextile', 'Trine', status)
        unsupported = domicile(analyze_aversions(ch, [make('Candidate')]),
                               'Jupiter', 'Pisces')
        confirmed = domicile(analyze_aversions(ch, [make('Verified')]),
                             'Jupiter', 'Pisces')
        self.assertEqual(unsupported.witnessing, 'Averse')
        self.assertNotIn('Translation via Moon', unsupported.mitigations)
        self.assertIn('Translation via Moon', confirmed.mitigations)
        self.assertEqual(confirmed.status, 'Mitigated')

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
        ch = chart()
        rays = analyze_rays(ch)
        pairs = [frozenset((r.caster, r.target)) for r in rays]
        self.assertEqual(len(pairs), len(set(pairs)))
        self.assertLessEqual(len(rays), 21)
        speed = {name: abs(p.data[3]) for name, p in
                 zip(PLANETS, ch.planets.planets)}
        self.assertTrue(all(speed[r.caster] >= speed[r.target] for r in rays))

    def test_caster_is_the_planet_actually_faster(self):
        # The course judges dexter/sinister from the applying, faster planet:
        # its actual speed, so Jupiter casts when Mars is nearly stationary.
        ch = chart(lons=[5, 105, 15, 235, 195, 70, 300],
                   speeds=[0, 5, .001, .9, 1, 1, 12],
                   contacts=[(1, 2, 2)])
        rays = [r for r in analyze_rays(ch)
                if {r.caster, r.target} == {'Jupiter', 'Mars'}]
        self.assertEqual(len(rays), 1)
        self.assertEqual((rays[0].caster, rays[0].target),
                         ('Jupiter', 'Mars'))
        self.assertEqual(rays[0].direction, 'Dexter')
        self.assertEqual(rays[0].aspect, 'Square')

    def test_course_dexter_and_sinister_examples(self):
        # Mercury in Aries applies to Saturn in Capricorn: dexter;
        # to Saturn in Cancer: sinister.
        self.assertEqual(directed_ray(0, 9), ('Square', 'Dexter'))
        self.assertEqual(directed_ray(0, 3), ('Square', 'Sinister'))

    def test_mars_squares_and_overcomes_saturn(self):
        ch = chart(contacts=[(0, 2, 2)])
        rays = [r for r in analyze_rays(ch)
                if {r.caster, r.target} == {'Mars', 'Saturn'}]
        self.assertEqual(len(rays), 1)
        mars = rays[0]
        self.assertEqual(mars.caster, 'Mars')
        self.assertEqual(mars.target, 'Saturn')
        self.assertEqual(mars.direction, 'Sinister')
        self.assertEqual(mars.overcoming, 'Mars')
        self.assertEqual(mars.degree_orb, 2.0)
        self.assertTrue(mars.aktinobolia)
        self.assertIn(mars.motion, ('Applying', 'Double application'))

    def test_slower_planet_overcoming_is_named(self):
        # Saturn in Capricorn is in the 10th sign from the Moon in Aries:
        # the row is still cast from the Moon, but Saturn overcomes.
        ch = chart(lons=[275, 105, 150, 235, 195, 70, 5],
                   speeds=[0, 0, 1, 1, 1, 1, 13], contacts=[(0, 6, 2)])
        row = next(r for r in analyze_rays(ch)
                   if {r.caster, r.target} == {'Moon', 'Saturn'})
        self.assertEqual((row.caster, row.target), ('Moon', 'Saturn'))
        self.assertEqual(row.direction, 'Dexter')
        self.assertEqual(row.overcoming, 'Saturn')
        self.assertFalse(row.aktinobolia)

    def test_every_ray_names_one_overcoming_planet(self):
        for row in analyze_rays(chart()):
            self.assertIn(row.overcoming, (row.caster, row.target))

    def test_aktinobolia_applying_or_separating(self):
        # Course: limited to three degrees, applying or separating.
        ch = chart(speeds=[0, 0, -1, .9, 1, 1, 12],
                   contacts=[(0, 2, 2)])
        mars = next(r for r in analyze_rays(ch) if r.caster == 'Mars'
                    and r.target == 'Saturn')
        self.assertTrue(mars.aktinobolia)
        self.assertEqual(mars.motion, 'Separating')

    def test_course_aktinobolia_mercury_saturn(self):
        # Saturn 15 Cancer, Mercury 14 Aries applying: Mercury overcomes
        # Saturn by a sinister square and is struck by Saturn's ray.
        ch = chart(lons=[105, 160, 200, 235, 300, 14, 50],
                   speeds=[0.03, .1, .5, 1, 1, 1.5, 13], contacts=[(0, 5, 2)])
        row = next(r for r in analyze_rays(ch)
                   if {r.caster, r.target} == {'Mercury', 'Saturn'})
        self.assertEqual((row.caster, row.direction), ('Mercury', 'Sinister'))
        self.assertEqual(row.overcoming, 'Mercury')
        self.assertTrue(row.aktinobolia)

    def test_no_aktinobolia_beyond_three_degrees_or_when_overcome(self):
        ch = chart(lons=[105, 160, 200, 235, 300, 10, 50],
                   speeds=[0.03, .1, .5, 1, 1, 1.5, 13], contacts=[(0, 5, 2)])
        row = next(r for r in analyze_rays(ch)
                   if {r.caster, r.target} == {'Mercury', 'Saturn'})
        self.assertFalse(row.aktinobolia)  # 5 degrees from exact
        # Saturn in Capricorn overcomes the Moon in Aries: no aktinobolia.
        ch = chart(lons=[275, 105, 150, 235, 195, 70, 5],
                   speeds=[0, 0, 1, 1, 1, 1, 13], contacts=[(0, 6, 2)])
        row = next(r for r in analyze_rays(ch)
                   if {r.caster, r.target} == {'Moon', 'Saturn'})
        self.assertFalse(row.aktinobolia)

    def test_sign_based_ray_outside_degree_orb(self):
        ch = chart(lons=[20, 105, 270, 235, 195, 70, 300])
        mars = next(r for r in analyze_rays(ch) if r.caster == 'Mars'
                    and r.target == 'Saturn')
        self.assertEqual(mars.overcoming, 'Mars')
        self.assertFalse(mars.in_orb)
        self.assertFalse(mars.aktinobolia)

    def test_averse_planet_pair_has_no_ray(self):
        ch = chart(lons=[5, 105, 273, 235, 165, 70, 300])
        rays = analyze_rays(ch)
        self.assertFalse(any({r.caster, r.target} == {'Saturn', 'Venus'}
                             for r in rays))


if __name__ == '__main__':
    unittest.main()

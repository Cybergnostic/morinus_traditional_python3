"""Planet-to-point regression tests: angles, Lots, strict/out-of-sign and A5."""
import unittest
from types import SimpleNamespace as NS

import point_aspects as p
from traditional_aspects import PLANETS


def opts(sidereal=False, sign_lots=False, visible=None):
    return NS(
        ayanamsha=1 if sidereal else 0,
        lotsusehouses=sign_lots,
        lotsvisible=[True, True] if visible is None else visible,
        orbs=[9.0] * 7)


def chart(longs, asc=0, mc=90, lot_positions=(( "Fortune", 60),("Spirit", 150)),
          speeds=None, shift=0):
    speeds = speeds or [0] * 7
    return NS(
        ayanamsha=shift,
        planets=NS(planets=[
            NS(data=[lon, 0, 0, speed]) for lon, speed in zip(longs, speeds)
        ]),
        houses=NS(ascmc=[asc, mc]),
        lots=NS(lots=[[name, None, None, None, lon] for name, lon in lot_positions]))


def config(**custom):
    data = dict(aspect_preset="traditional")
    data.update(custom)
    return data


class PointTests(unittest.TestCase):
    def test_angles_include_asc_and_mc_only(self):
        ch = chart([0] * 7)
        self.assertEqual([(a.name, a.longitude) for a in p.angles(ch, opts())],
                         [("ASC", 0), ("MC", 90)])
        rows = p.analyze_single(ch, "Angles", opts(), config())
        self.assertTrue(all(r.point in ("ASC", "MC") for r in rows))
        self.assertEqual(len(rows), 14)

    def test_sun_full_orb_accepts_15_rejects_16(self):
        # Points have no orb: the planet's own (full) orb applies.
        ch = chart([140, 140, 140, 15, 140, 140, 140])
        rows = p.analyze_single(ch, "Angles", opts(), config(),
                                planet_filter="Sun", point_filter="ASC")
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0].deviation, 15)
        ch.planets.planets[3].data[0] = 16
        self.assertEqual(p.analyze_single(ch, "Angles", opts(), config(),
                                          planet_filter="Sun",
                                          point_filter="ASC"), ())

    def test_custom_orb_is_used_in_full(self):
        ch = chart([140, 140, 140, 6, 140, 140, 140])
        vals = config(aspect_preset="custom")
        vals.update({"aspect_custom_" + planet.lower(): 6 for planet in PLANETS})
        self.assertEqual(len(p.analyze_single(ch, "Angles", opts(), vals,
                                              planet_filter="Sun",
                                              point_filter="ASC")), 1)
        ch.planets.planets[3].data[0] = 7
        self.assertEqual(p.analyze_single(ch, "Angles", opts(), vals,
                                          planet_filter="Sun",
                                          point_filter="ASC"), ())

    def test_three_degree_rule_across_sign_boundary(self):
        ch = chart([359] + [140] * 6, asc=1)
        across = p.analyze_single(
            ch, "Angles", opts(), config(), planet_filter="Saturn",
            point_filter="ASC")
        self.assertEqual(len(across), 1)
        self.assertTrue(across[0].out_of_sign)
        # 4 degrees across the boundary: no contact, although within 9.
        ch.planets.planets[0].data[0] = 357
        self.assertFalse(p.analyze_single(
            ch, "Angles", opts(), config(), planet_filter="Saturn",
            point_filter="ASC"))

    def test_lots_visibility_and_names(self):
        ch = chart([60] * 7)
        o = opts(visible=[True, False])
        lots = p.lots(ch, o)
        self.assertEqual([(v.name, v.longitude) for v in lots], [("Fortune", 60)])
        r = p.analyze_single(ch, "Lots", o, config())
        self.assertEqual(len(r), 7)
        self.assertTrue(all(x.point == "Fortune" for x in r))

    def test_sign_only_lots_have_no_fake_degree_orb(self):
        ch = chart([65] + [160] * 6, lot_positions=(("Fortune", 60),))
        r = p.analyze_single(ch, "Lots", opts(sign_lots=True), config(),
                             planet_filter="Saturn")
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].aspect, "Conjunction")
        self.assertIsNone(r[0].deviation)
        self.assertFalse(r[0].degree_based)
        self.assertEqual(r[0].motion, "By sign")

    def test_sidereal_angle_shifts_lot_does_not_double_shift(self):
        ch = chart([350] + [150] * 6, asc=350, mc=110,
                   lot_positions=(("Fortune", 330),), shift=20)
        o = opts(sidereal=True)
        self.assertAlmostEqual(p.angles(ch, o)[0].longitude, 330)
        self.assertAlmostEqual(p.lots(ch, o)[0].longitude, 330)
        a = p.analyze_single(ch, "Angles", o, config(),
                             planet_filter="Saturn", point_filter="ASC")
        lots = p.analyze_single(ch, "Lots", o, config(),
                                planet_filter="Saturn", point_filter="Fortune")
        self.assertEqual(len(a), 1)
        self.assertEqual(len(lots), 1)

    def test_single_moving_planet_status_no_point_speed(self):
        ch = chart([2] + [140] * 6, speeds=[-1] + [0] * 6)
        r = p.analyze_single(ch, "Angles", opts(), config(),
                             planet_filter="Saturn", point_filter="ASC")
        self.assertEqual(r[0].motion, "Applying")

    def test_cross_both_directions_and_only_planet_point(self):
        a = chart([0] + [140] * 6, asc=140, mc=270)
        b = chart([140] + [240] * 6, asc=0, mc=270)
        rows = p.analyze_cross(a, b, "Angles", opts(), config())
        ab = [r for r in rows if r.chart_of_planet == "A"
              and r.planet == "Saturn" and r.point == "ASC"]
        ba = [r for r in rows if r.chart_of_planet == "B"
              and r.planet == "Saturn" and r.point == "ASC"]
        self.assertEqual((len(ab), len(ba)), (1, 1))
        self.assertEqual((ab[0].chart_of_point, ba[0].chart_of_point),
                         ("B", "A"))
        self.assertTrue(all(r.chart_of_planet != r.chart_of_point
                            for r in rows))

    def test_cross_lots_use_own_chart_values(self):
        a = chart([0] + [140] * 6, lot_positions=(("Fortune", 140),))
        b = chart([140] + [240] * 6, lot_positions=(("Fortune", 0),))
        rows = p.analyze_cross(a, b, "Lots", opts(), config(),
                               planet_filter="Saturn", point_filter="Fortune")
        self.assertEqual(len(rows), 2)
        self.assertEqual(set((r.chart_of_planet, r.chart_of_point)
                             for r in rows), {("A", "B"), ("B", "A")})

    def test_cross_same_chart_object_rejected(self):
        a = chart([0] * 7)
        self.assertEqual(p.analyze_cross(a, a, "Angles", opts(), config()), ())

    def test_never_mutate_lots_or_planets(self):
        a = chart([0] * 7)
        b = chart([10] * 7)
        previous = tuple(tuple(x) for x in a.lots.lots)
        p.analyze_cross(a, b, "Lots", opts(), config())
        self.assertEqual(tuple(tuple(x) for x in a.lots.lots), previous)


if __name__ == "__main__":
    unittest.main()

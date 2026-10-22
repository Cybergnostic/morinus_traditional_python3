import math
import unittest

from wheel_primitives import (angle_longitudes, planet_band_radii,
                              polar_point, position_text,
                              paint_glyph, paint_position_text,
                              optical_text_center, planet_cluster_radii,
                              compact_planet_radii, radial_half_extent,
                              traditional_term_markers, traditional_decan_markers)


class SharedWheelPrimitivesTests(unittest.TestCase):
    def test_positions_match_morinus_truncation_and_split_labels(self):
        self.assertEqual(position_text(43 + 12.9 / 60, '°'), ('13°', "12'"))
        self.assertEqual(position_text(359 + 59.9 / 60, '°'), ('29°', "59'"))
        self.assertEqual(position_text(360.0, '°'), ('00°', "00'"))
        self.assertEqual(position_text(15.5, '°'), ('15°', "30'"))

    def test_ascendant_on_left_and_cardinal_directions(self):
        cx, cy = 100.0, 100.0
        self.assertAlmostEqual(polar_point(cx, cy, 72, 72, 50)[0], 50)
        self.assertAlmostEqual(polar_point(cx, cy, 72, 252, 50)[0], 150)
        x, y = polar_point(cx, cy, 72, 162, 50)
        self.assertAlmostEqual(x, 100, places=7)
        self.assertAlmostEqual(y, 150, places=7)

    def test_glyph_and_text_painters_match_legacy_pixel_centres(self):
        class FakeDraw:
            def __init__(self):
                self.calls = []
            def textbbox(self, xy, text, font=None):
                return (0, 0, 20, 10)
            def text(self, xy, text, fill=None, font=None):
                self.calls.append((xy, text, fill, font))
        painter = FakeDraw()
        paint_glyph(painter, (100, 80), 'P', 'font', 16, (3, 4, 5))
        paint_position_text(painter, (100, 80), '12°', 'font', (3, 4, 5))
        self.assertEqual(painter.calls[0], ((92, 72), 'P', (3, 4, 5), 'font'))
        self.assertEqual(painter.calls[1], ((90, 75), '12°', (3, 4, 5), 'font'))

    def test_optical_centring_accounts_for_glyph_bearings(self):
        class FakeDraw:
            def __init__(self):
                self.calls = []
            def textbbox(self, xy, text, font=None):
                return (2, 5, 22, 15)
            def text(self, xy, text, fill=None, font=None):
                self.calls.append((xy, text, fill))
        painter = FakeDraw()
        optical_text_center(painter, (100, 80), '♄', 'font', (0, 0, 0))
        self.assertEqual(painter.calls, [((88, 70), '♄', (0, 0, 0))])

    def test_measured_planet_cluster_uses_one_angular_slot(self):
        sizes = ((12, 12), (16, 9), (13, 8))
        for angle in (0, math.pi / 4, math.pi / 2, math.pi):
            layout = planet_cluster_radii(130, 185, angle, *sizes)
            self.assertGreater(layout['glyph'], layout['degree'])
            self.assertGreater(layout['degree'], layout['minute'])
            reaches = [radial_half_extent(size, angle) for size in sizes]
            self.assertLessEqual(layout['glyph'] + reaches[0], 183.01)
            self.assertGreaterEqual(layout['minute'] - reaches[2], 131.99)
            self.assertGreaterEqual(
                layout['glyph'] - reaches[0],
                layout['degree'] + reaches[1] - .001)
            self.assertGreaterEqual(
                layout['degree'] - reaches[1],
                layout['minute'] + reaches[2] - .001)
        with self.assertRaises(ValueError):
            planet_cluster_radii(80, 80, 0, *sizes)

    def test_single_position_row_stays_inward_of_glyph(self):
        glyph_box = (13.0, 13.0)
        text_box = (30.0, 10.0)  # e.g. 07°05'
        for angle in (0, math.pi / 4, math.pi / 2, math.pi):
            radii = compact_planet_radii(
                100.0, 161.0, angle, glyph_box, text_box)
            self.assertGreater(radii['glyph'], radii['position'])
            glyph_reach = radial_half_extent(glyph_box, angle)
            text_reach = radial_half_extent(text_box, angle)
            self.assertLessEqual(radii['glyph'] + glyph_reach, 159.01)
            self.assertGreaterEqual(radii['position'] - text_reach, 101.99)
            self.assertGreaterEqual(
                radii['glyph'] - glyph_reach,
                radii['position'] + text_reach)
        with self.assertRaises(ValueError):
            compact_planet_radii(100, 100, 0, glyph_box, text_box)

    def test_compact_planet_group_is_actually_centered(self):
        # Before the fix, glyphs were pushed to the outer boundary. The
        # ink-box envelope should straddle the band midpoint.
        glyph_box, position_box = (11.0, 11.0), (29.0, 10.0)
        for angle in (0, math.pi / 4, math.pi / 2, math.pi):
            radii = compact_planet_radii(
                110.0, 177.0, angle, glyph_box, position_box)
            gr = radial_half_extent(glyph_box, angle)
            pr = radial_half_extent(position_box, angle)
            outside = radii['glyph'] + gr
            inside = radii['position'] - pr
            self.assertAlmostEqual(
                (outside + inside) / 2.0, (110 + 177) / 2.0,
                places=6)
            self.assertGreater(outside, inside)
            self.assertGreater(inside, 111)
            self.assertLess(outside, 176)

    def test_shared_traditional_terms_follow_unequal_bounds(self):
        # A synthetic sign: the original GraphChart uses successive
        # cumulative endpoints, not 6-degree equal partitions.
        terms = [[(1, 4), (2, 8), (3, 6), (4, 5), (5, 7)]]
        values = list(traditional_term_markers(terms))
        self.assertEqual([planet for _, planet, _ in values], [1, 2, 3, 4, 5])
        self.assertEqual([mid for mid, _, _ in values],
                         [2.0, 8.0, 15.0, 20.5, 26.5])
        self.assertEqual([boundary for _, _, boundary in values],
                         [4.0, 12.0, 18.0, 23.0, 30.0])

    def test_shared_decans_follow_original_morinus_centres(self):
        ruler_sets = [[1, 2, 3], [4, 5, 6]]
        values = list(traditional_decan_markers(ruler_sets))
        self.assertEqual([mid for mid, _, _ in values],
                         [5.0, 15.0, 25.0, 35.0, 45.0, 55.0])
        self.assertEqual([boundary for _, _, boundary in values],
                         [0.0, 10.0, 20.0, 30.0, 40.0, 50.0])

    def test_four_angles_match_morinus_quadrants(self):
        self.assertEqual(angle_longitudes(350, 75), (350, 170, 75, 255))

    def test_positions_move_inward_in_morinus_order(self):
        for inner, outer in ((30, 95), (180, 239), (239, 312)):
            r = planet_band_radii(inner, outer)
            self.assertTrue(inner < r['motion'] < r['minute'] <
                            r['degree'] < r['glyph'] < outer)
            self.assertTrue(r['tick'] < outer)
        with self.assertRaises(ValueError):
            planet_band_radii(100, 100)
        with self.assertRaises(ValueError):
            planet_band_radii(120, 100)


if __name__ == '__main__':
    unittest.main()

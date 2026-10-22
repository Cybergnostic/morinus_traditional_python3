import math
import unittest

from wheel_primitives import (angle_longitudes, planet_band_radii,
                              polar_point, position_text,
                              paint_glyph, paint_position_text)


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

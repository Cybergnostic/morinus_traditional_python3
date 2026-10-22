import unittest

from multiwheel_layout import (allocate_rings, allocate_traditional_rings,
                               spread_longitudes, zodiac_sign_lane)


class MultiWheelLayoutTests(unittest.TestCase):
    def test_one_to_three_rings_fit_without_overlap(self):
        for count in (1, 2, 3):
            core, zodiac, rings = allocate_rings(300, count)
            self.assertEqual(len(rings), count)
            self.assertTrue(0 < core < zodiac[1] < rings[0][1] <= 300)
            self.assertAlmostEqual(zodiac[0], core)
            self.assertAlmostEqual(rings[0][0], zodiac[1])
            for previous, following in zip(rings, rings[1:]):
                self.assertAlmostEqual(previous[1], following[0])
            self.assertAlmostEqual(rings[-1][1], 300)
            descending = [rings[-1][1], rings[-1][0], zodiac[0], 0]
            self.assertTrue(all(a > b for a, b in zip(descending, descending[1:])))

    def test_zodiac_sign_lane_follows_degree_ticks(self):
        for inner, outer in ((80, 100), (180, 220), (0, 40)):
            lane, end = zodiac_sign_lane((inner, outer))
            self.assertGreater(lane, inner + .28 * (outer - inner))
            self.assertLess(lane, outer)
            self.assertAlmostEqual((lane + end) / 2,
                                   inner + .69 * (outer - inner))
        with self.assertRaises(ValueError):
            zodiac_sign_lane((100, 100))

    def test_invalid_rings(self):
        for value in (0, 4):
            with self.assertRaises(ValueError):
                allocate_rings(200, value)

    def test_traditional_reference_bands_appear_once(self):
        for count in (1, 2, 3):
            for show_terms in (False, True):
                for show_decans in (False, True):
                    core, decans, terms, zodiac, outer = allocate_traditional_rings(
                        300, count, show_terms, show_decans)
                    self.assertEqual(len(outer), count)
                    self.assertEqual(decans is not None, show_decans)
                    self.assertEqual(terms is not None, show_terms)
                    cursor = core
                    for band in (decans, terms, zodiac, *outer):
                        if band is None:
                            continue
                        self.assertAlmostEqual(cursor, band[0])
                        self.assertGreater(band[1], band[0])
                        cursor = band[1]
                    self.assertAlmostEqual(cursor, 300)
                    self.assertGreater(core, 0)

    def test_compact_biwheel_preserves_outer_boundary(self):
        # Before the refinement, the bi-wheel radix core was .555 of the
        # maximum radius. Increasing it makes the outer ring slimmer while
        # keeping the chart's overall diameter the same.
        rmax = 300.0
        core, decans, terms, zodiac, rings = allocate_traditional_rings(
            rmax, 1, True, True)
        previous_width = rmax * (1 - (.555 + .08 + .10))
        self.assertGreater(core, rmax * .60)
        self.assertLess(rings[0][1] - rings[0][0], previous_width * .82)
        self.assertAlmostEqual(rings[-1][1], rmax)
        self.assertAlmostEqual(zodiac[1], rings[0][0])

    def test_wider_radix_and_ordered_rings_for_all_wheel_counts(self):
        for count in (1, 2, 3):
            for terms in (False, True):
                for decans in (False, True):
                    core, dband, tband, zodiac, rings = allocate_traditional_rings(
                        300.0, count, terms, decans)
                    self.assertEqual(len(rings), count)
                    self.assertTrue(all(b > a for a, b in rings))
                    self.assertAlmostEqual(rings[-1][1], 300.0)
                    for prev, next_ring in zip(rings, rings[1:]):
                        self.assertAlmostEqual(prev[1], next_ring[0])

    def test_traditional_band_is_large_enough_for_original_glyphs(self):
        # GraphChart's ruler glyphs are approximately 1/18 radius.
        # Each strip must fit them with margin, across all ring counts.
        radius = 300.0
        for count in (1, 2, 3):
            _, decans, terms, _, rings = allocate_traditional_rings(
                radius, count, True, True)
            for inner, outer in (decans, terms):
                self.assertGreater(outer - inner, radius * .045)
            self.assertAlmostEqual(rings[-1][1], radius)

    def test_traditional_layout_rejects_invalid_dimensions(self):
        for count in (0, 4):
            with self.assertRaises(ValueError):
                allocate_traditional_rings(300, count)
        for size in (0, -1):
            with self.assertRaises(ValueError):
                allocate_traditional_rings(size, 2)

    def test_spreading_keeps_order_across_aries(self):
        longitudes = [359, 1, 3, 15, 210]
        result = spread_longitudes(longitudes, 9)
        self.assertEqual(len(result), len(longitudes))
        # Start at 210, the first object following the largest circular gap.
        chain = [result[i] for i in (4, 0, 1, 2, 3)]
        gaps = [(b - a) % 360 for a, b in
                zip(chain, chain[1:] + chain[:1])]
        self.assertTrue(all(g >= 9 - 1e-8 for g in gaps), gaps)

    def test_all_equal_longitudes_and_wrap(self):
        for data in ([0, 0, 0, 0], [358, 359, 0, 1, 2],
                     [15], [], [0, 180]):
            result = spread_longitudes(data, 10)
            self.assertEqual(len(result), len(data))
            if len(data) >= 2:
                sorted_out = sorted(result)
                gaps = [(sorted_out[(i + 1) % len(data)] -
                         sorted_out[i]) % 360 for i in range(len(data))]
                self.assertTrue(all(g >= 10 - 1e-8 for g in gaps), gaps)

    def test_impossible_separation(self):
        with self.assertRaises(ValueError):
            spread_longitudes([1, 2, 3, 4], 91)


if __name__ == '__main__':
    unittest.main()

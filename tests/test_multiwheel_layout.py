import unittest

from multiwheel_layout import allocate_rings, spread_longitudes


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

    def test_invalid_rings(self):
        for value in (0, 4):
            with self.assertRaises(ValueError):
                allocate_rings(200, value)

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

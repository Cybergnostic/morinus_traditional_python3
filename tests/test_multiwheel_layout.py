import unittest

from multiwheel_layout import (allocate_rings, allocate_traditional_rings,
                               spread_longitudes, zodiac_sign_lane,
                               place_planet_clusters, _intersect_area,
                               shared_planet_font_sizes, house_sector,
                               place_planet_glyphs, place_degree_annotations)


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

    def test_biwheel_reserves_space_for_readable_outer_planets(self):
        rmax = 300.0
        core, decans, terms, zodiac, rings = allocate_traditional_rings(
            rmax, 1, True, True)
        # Previous implementation left only 15.5% of radius for ring 1.
        self.assertGreater(core, rmax * .50)
        self.assertLess(core, rmax * .56)
        self.assertGreater(rings[0][1] - rings[0][0], rmax * .24)
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

    @staticmethod
    def boxes(count):
        return [((13, 13), (15, 9), (13, 9), (0, 0))
                for _ in range(count)]

    def test_conjunction_uses_measured_angular_and_radial_lanes(self):
        longitudes = [12.0, 12.0, 12.0, 12.0]
        result, unresolved = place_planet_clusters(
            longitudes, self.boxes(4), (150, 235), 180)
        # Four bodies at one degree may exceed the available angular/radial
        # space. The renderer must flag any collision instead of hiding it.
        self.assertLess(len(unresolved), 4)
        self.assertEqual(len(result), 4)
        self.assertTrue(any(p['offset'] != 0 or
                            abs(p['longitude'] - 12) > .001 for p in result))
        for i, a in enumerate(result):
            self.assertTrue(a['fits'])
            self.assertEqual(int(a['longitude'] // 30), 0)
            self.assertEqual(a['exact'], 12)
            for b in result[i + 1:]:
                for rect_a in a['rects']:
                    for rect_b in b['rects']:
                        if _intersect_area(rect_a, rect_b) > 0:
                            j = result.index(b)
                            self.assertTrue(i in unresolved or j in unresolved)

    def test_no_label_can_cross_into_adjacent_sign(self):
        longitudes = [29.8, 29.9, 30.0, 30.15, 359.8, .05]
        result, _ = place_planet_clusters(
            longitudes, self.boxes(len(longitudes)), (100, 205), 90)
        for original, candidate in zip(longitudes, result):
            self.assertEqual(int(original // 30),
                             int(candidate['longitude'] // 30))
            self.assertEqual(candidate['exact'], original)
            self.assertLessEqual(
                abs((candidate['longitude'] - original + 180) % 360 - 180), 8.01)

    def test_unreadable_narrow_band_reports_the_problem(self):
        lons = [15.0, 15.0, 15.0]
        result, unresolved = place_planet_clusters(
            lons, self.boxes(3), (100, 112), 30)
        self.assertEqual(len(result), len(lons))
        self.assertTrue(unresolved)

    def test_invalid_cluster_inputs(self):
        with self.assertRaises(ValueError):
            place_planet_clusters([1], [], (100, 200), 0)
        with self.assertRaises(ValueError):
            place_planet_clusters([1], self.boxes(1), (100, 100), 0)
        with self.assertRaises(ValueError):
            place_planet_clusters([1], self.boxes(1), (100, 200), 0, -1)

    def test_planet_font_sizes_are_shared_across_every_ring(self):
        # Unlike the previous renderer, outer bands do not choose their
        # font size separately. The smallest content band sets the scale.
        for widths in ([40, 65], [65, 40], [80, 40, 65]):
            sizes = shared_planet_font_sizes(300, widths)
            self.assertGreaterEqual(sizes['glyph'], 17)
            self.assertLess(sizes['degree'], sizes['glyph'])
            self.assertGreaterEqual(sizes['degree'], 9)
            self.assertGreaterEqual(sizes['minute'], 9)
            self.assertGreaterEqual(sizes['motion'], 9)
            self.assertGreater(sizes['glyph'], sizes['degree'])
        # Zooming the chart makes it possible to use larger shared glyphs.
        sizes = shared_planet_font_sizes(800, [115, 136, 122, 128])
        self.assertGreater(sizes['glyph'], 12)
        self.assertEqual(sizes, shared_planet_font_sizes(
            800, [128, 115, 136, 122]))

    def test_shared_planet_fonts_reject_invalid_dimensions(self):
        for widths in ([], [0], [-3, 65]):
            with self.assertRaises(ValueError):
                shared_planet_font_sizes(300, widths)
        with self.assertRaises(ValueError):
            shared_planet_font_sizes(0, [50])

    @staticmethod
    def twelve_cusps():
        # House I covers 350° to 20° (crosses 0 Aries); House II
        # starts at 20° Aries, within the same zodiac sign.
        return [350, 20, 50, 80, 110, 140,
                170, 200, 230, 260, 290, 320]

    def test_chart_house_lookup_handles_aries_wrap_and_exact_cusp(self):
        cusps = self.twelve_cusps()
        self.assertEqual(house_sector(359, cusps), 0)
        self.assertEqual(house_sector(0, cusps), 0)
        self.assertEqual(house_sector(19.999, cusps), 0)
        self.assertEqual(house_sector(20, cusps), 1)
        self.assertEqual(house_sector(20.1, cusps), 1)
        with self.assertRaises(ValueError):
            house_sector(10, [0, 30])

    def test_primary_glyphs_stay_in_correct_sign_and_house(self):
        original = [19.8, 20.0, 20.2, 359.8, 0.1, 120]
        glyphs, unresolved = place_planet_glyphs(
            original, [(19, 21)] * len(original), (110, 180),
            350, house_cusps=self.twelve_cusps())
        self.assertEqual(len(glyphs), len(original))
        self.assertTrue(set(unresolved).issubset(set(range(len(original)))))
        for original_lon, glyph in zip(original, glyphs):
            self.assertEqual(int(original_lon // 30),
                             int(glyph['longitude'] // 30))
            self.assertEqual(house_sector(original_lon, self.twelve_cusps()),
                             house_sector(glyph['longitude'],
                                          self.twelve_cusps()))
            self.assertEqual(glyph['exact'], original_lon)
            self.assertLessEqual(abs((glyph['longitude'] -
                                      original_lon + 180) % 360 - 180),
                                 7.501)

    def test_glyphs_do_not_depend_on_degree_label_dimensions(self):
        longitudes = [4, 4.5, 5, 195]
        boxes = [(23, 24)] * 4
        glyphs, unresolved = place_planet_glyphs(
            longitudes, boxes, (170, 260), 30)
        # Grossly oversized numbers may need to be hidden, but cannot move
        # any glyph. Primary positions remain exactly the same objects.
        labels, hidden = place_degree_annotations(
            glyphs, longitudes, [(400, 20)] * 4,
            (170, 260), 30, -1)
        self.assertEqual(len(labels), len(glyphs))
        self.assertEqual(hidden, [0, 1, 2, 3])
        self.assertTrue(all(label is None for label in labels))
        self.assertEqual([g['exact'] for g in glyphs], longitudes)

    def test_annotations_never_overlap_primary_ink(self):
        longitudes = [10, 95, 205]
        glyphs, _ = place_planet_glyphs(
            longitudes, [(20, 20)] * 3, (110, 195), 40)
        boxes = [(16, 9)] * 3
        labels, hidden = place_degree_annotations(
            glyphs, longitudes, boxes, (110, 195), 40, -1)
        self.assertFalse(hidden)
        for point, box in zip(labels, boxes):
            self.assertIsNotNone(point)
            rect = (point[0] - box[0] / 2 - .7,
                    point[1] - box[1] / 2 - .7,
                    point[0] + box[0] / 2 + .7,
                    point[1] + box[1] / 2 + .7)
            self.assertTrue(all(_intersect_area(rect, g['rect']) == 0
                                for g in glyphs))

    def test_all_degree_labels_fit_in_typical_biwheel_band(self):
        # A real-looking wheel: nine bodies, including close neighbours,
        # positioned around the circle. Each must get a degree annotation.
        longitudes = [0.4, 12.6, 19.2, 20.4, 58.0,
                      88.0, 174.0, 251.0, 359.0]
        glyphs, _ = place_planet_glyphs(
            longitudes, [(19, 21)] * 9, (175, 251), 78)
        degree_points, hidden = place_degree_annotations(
            glyphs, longitudes, [(19, 9)] * 9,
            (175, 251), 78, -1)
        self.assertEqual(hidden, [])
        self.assertTrue(all(point is not None for point in degree_points))
        for i, point in enumerate(degree_points):
            label_rect = (point[0] - 10.3, point[1] - 5.3,
                          point[0] + 10.3, point[1] + 5.3)
            for glyph in glyphs:
                self.assertEqual(_intersect_area(label_rect,
                                                  glyph['rect']), 0)

    def test_full_position_labels_use_both_radial_sides(self):
        # The full degree+minute text is wider, but has sufficient space
        # in a typical outer ring without colliding with the glyphs.
        longitudes = [0.4, 12.6, 19.2, 20.4, 58.0,
                      88.0, 174.0, 251.0, 359.0]
        glyphs, _ = place_planet_glyphs(
            longitudes, [(19, 21)] * 9, (270, 375), 78)
        points, hidden = place_degree_annotations(
            glyphs, longitudes, [(34, 9)] * 9,
            (270, 375), 78, 1)
        self.assertEqual(hidden, [])
        self.assertTrue(all(point is not None for point in points))

    def test_primary_glyph_layout_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            place_planet_glyphs([10], [], (110, 195), 40)
        with self.assertRaises(ValueError):
            place_planet_glyphs([10], [(20, 20)], (110, 110), 40)
        with self.assertRaises(ValueError):
            place_planet_glyphs([10], [(20, 20)], (110, 195), 40,
                                house_cusps=[10])
        with self.assertRaises(ValueError):
            place_degree_annotations([], [1], [], (100, 200), 40, -1)

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

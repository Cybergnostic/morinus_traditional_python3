"""Unit tests of chart raster sizing and click mapping (no wx required)."""
import unittest
from chartquality import scale_for, raster_size, render_position


class ChartQualityTests(unittest.TestCase):
    def test_standard_is_unchanged(self):
        self.assertEqual(scale_for((960, 720), 'standard'), 1)
        self.assertEqual(raster_size((960, 720), 1), (960, 720))

    def test_high_quality_double_resolution(self):
        self.assertEqual(scale_for((960, 720), 'high'), 2)
        self.assertEqual(raster_size((960, 720), 2), (1920, 1440))

    def test_preserves_wide_aspect_ratio(self):
        self.assertEqual(raster_size((1100, 550), 2), (2200, 1100))

    def test_memory_cap(self):
        self.assertEqual(scale_for((3000, 2000), 'high'), 1)

    def test_tiny_charts_fall_back(self):
        self.assertEqual(scale_for((320, 180), 'high'), 1)

    def test_hit_test_mapping(self):
        self.assertEqual(render_position((103, 251), 2), (206, 502))
        self.assertEqual(render_position((103, 251), 1), (103, 251))


if __name__ == '__main__':
    unittest.main()

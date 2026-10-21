"""Table display sizing, scroll anchoring and header/zoom tests."""
import unittest
from PIL import Image
from tablepresentation import (
    zoom_value, pixel_size, anchored_scroll, header_colour, resample,
)


class TablePresentationTests(unittest.TestCase):
    def test_zoom_rounding_and_limits(self):
        self.assertEqual(zoom_value(1.004, 800, 400), 1.0)
        self.assertEqual(zoom_value(100, 800, 400), 3.0)
        self.assertEqual(zoom_value(0.1, 800, 400), 0.5)

    def test_large_table_zoom_is_limited(self):
        self.assertLess(zoom_value(3.0, 4000, 4000), 3.0)

    def test_raster_dimensions(self):
        self.assertEqual(pixel_size(800, 400, 1.25), (1000, 500))
        self.assertEqual(pixel_size(800, 400, 1.0), (800, 400))

    def test_cursor_anchor(self):
        # Document position (200 + 100) / 1.0 = 300 remains under x=100.
        self.assertEqual(anchored_scroll(200, 100, 1.0, 1.5), 350)
        self.assertEqual(anchored_scroll(200, 100, 1.5, 1.0), 100)

    def test_anchor_is_nonnegative(self):
        self.assertEqual(anchored_scroll(0, 500, 2.0, 0.5), 0)

    def test_headers_keep_monochrome(self):
        self.assertEqual(header_colour((255, 255, 255), (0, 0, 0), True),
                         (255, 255, 255))

    def test_header_tint_is_subtle(self):
        self.assertEqual(header_colour((255, 255, 255), (0, 0, 0)),
                         (235, 235, 235))

    def test_resample_dimensions_and_one_to_one(self):
        source = Image.new('RGB', (30, 12), (255, 255, 255))
        source.putpixel((6, 5), (0, 0, 0))
        self.assertEqual(resample(source, (30, 12)).tobytes(), source.tobytes())
        self.assertEqual(resample(source, (60, 24)).size, (60, 24))


if __name__ == '__main__':
    unittest.main()

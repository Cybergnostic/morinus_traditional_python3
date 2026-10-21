"""Regression tests for the native sidebar width logic."""
import unittest
import sidebar


class SidebarWidthTests(unittest.TestCase):
    def test_normal_width(self):
        self.assertEqual(sidebar.fit_width(960, 310), 310)

    def test_minimum_and_maximum(self):
        self.assertEqual(sidebar.fit_width(1200, 5), 250)
        self.assertEqual(sidebar.fit_width(1200, 9000), 560)

    def test_narrow_frame(self):
        self.assertEqual(sidebar.fit_width(520, 310), 220)
        self.assertEqual(sidebar.fit_width(700, 560), 400)

    def test_no_side_effects(self):
        before = sidebar.tradoptions.values()
        sidebar.fit_width(480, 350)
        self.assertEqual(before, sidebar.tradoptions.values())


if __name__ == '__main__':
    unittest.main()

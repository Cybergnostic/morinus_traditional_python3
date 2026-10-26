"""Temporary multiwheel chart visibility never mutates chart source slots."""
import unittest

from multiwheel_visibility import (
    visible_slot_indices, displayed_charts, remap_highlights, aspect_ring,
)


class MultiwheelVisibilityTests(unittest.TestCase):
    def test_all_slots_visible_by_default(self):
        self.assertEqual(visible_slot_indices(2, (True, True, True, True)),
                         (0, 1))
        self.assertEqual(visible_slot_indices(4, (True,) * 4),
                         (0, 1, 2, 3))

    def test_hide_radix_while_sr_lr_become_biwheel(self):
        original = [object() for _ in range(4)]
        before = tuple(original)
        shown = visible_slot_indices(3, (False, True, True, True))
        self.assertEqual(shown, (1, 2))
        centre, rings = displayed_charts(original, shown)
        self.assertIs(centre, original[1])
        self.assertEqual(rings, [original[2]])
        self.assertEqual(tuple(original), before)

    def test_middle_slot_omission_compresses_without_reordering(self):
        self.assertEqual(
            visible_slot_indices(4, (True, False, True, True)),
            (0, 2, 3))
        self.assertEqual(
            visible_slot_indices(4, (False, True, False, True)),
            (1, 3))

    def test_two_visible_charts_minimum(self):
        with self.assertRaises(ValueError):
            visible_slot_indices(3, (False, True, False, True))
        with self.assertRaises(ValueError):
            visible_slot_indices(2, (False, True, True, True))

    def test_inactive_slots_ignored(self):
        self.assertEqual(
            visible_slot_indices(2, (True, True, False, False)),
            (0, 1))

    def test_malformed_input_rejected(self):
        with self.assertRaises(ValueError):
            visible_slot_indices(5, [True] * 5)
        with self.assertRaises(ValueError):
            visible_slot_indices(3, [True, True])

    def test_time_lord_marks_remap_to_visible_layer(self):
        source = {
            "marks": [
                {"ring": 0, "planet": "Sun", "role": "natal"},
                {"ring": 1, "planet": "Sun", "role": "solar"},
                {"ring": 2, "planet": "Moon", "role": "lunar"},
            ],
            "areas": [
                {"ring": 0, "role": "natal"},
                {"ring": 1, "role": "solar"},
                {"ring": 2, "role": "lunar"},
            ],
            "legend": [{"role": "annual", "text": "Annual lord"},
                       {"role": "monthly", "text": "Monthly lord"}],
        }
        copied = remap_highlights(source, (1, 2))
        for field in ("marks", "areas"):
            self.assertEqual([entry["ring"] for entry in copied[field]],
                             [0, 1])
            self.assertEqual([entry["ring"] for entry in source[field]],
                             [0, 1, 2])
        self.assertEqual(copied["legend"], source["legend"])
        self.assertIsNot(copied["legend"], source["legend"])

    def test_selected_original_ring_is_mapped_after_hiding_chart(self):
        self.assertEqual(aspect_ring(-1, (0, 1, 2)), -1)
        self.assertEqual(aspect_ring(0, (1, 2)), 0)
        self.assertEqual(aspect_ring(2, (1, 2)), 1)
        self.assertEqual(aspect_ring(3, (0, 2, 3)), 2)
        self.assertEqual(aspect_ring(1, (0, 2, 3)), -1)

    def test_visible_layers_reference_original_chart_objects(self):
        a, b, c = (object(), object(), object())
        centre, outer = displayed_charts([a, b, c], (1, 2))
        self.assertIs(centre, b)
        self.assertIs(outer[0], c)


if __name__ == "__main__":
    unittest.main()

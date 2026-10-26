"""Opts/traditional.json: unusable saved values fall back to their defaults."""
import json
import os
import tempfile
import unittest

import tradoptions


class LoadValidationTests(unittest.TestCase):
	def setUp(self):
		self.saved_values = tradoptions._values
		self.saved_name = tradoptions.FILENAME
		self.folder = tempfile.TemporaryDirectory()
		tradoptions.FILENAME = os.path.join(self.folder.name, 'traditional.json')

	def tearDown(self):
		tradoptions.FILENAME = self.saved_name
		tradoptions._values = self.saved_values
		self.folder.cleanup()

	def load(self, data):
		with open(tradoptions.FILENAME, 'w', encoding='utf-8') as f:
			f.write(data if isinstance(data, str) else json.dumps(data))
		return tradoptions.load()

	def test_good_values_are_kept(self):
		values = self.load({'aspect_preset': 'custom',
			'aspect_custom_moon': 10, 'show_toolbar': False, 'zr_years': 90})
		self.assertEqual(values['aspect_preset'], 'custom')
		self.assertEqual(values['aspect_custom_moon'], 10)
		self.assertFalse(values['show_toolbar'])
		self.assertEqual(values['zr_years'], 90)

	def test_bad_values_fall_back(self):
		values = self.load({'aspect_preset': 'modern', 'aspect_custom_moon': 45,
			'aspect_custom_sun': -1,
			'show_toolbar': 'yes', 'ca_rays': [True], 'unknown': 1})
		for key in ('aspect_preset', 'aspect_custom_moon',
				'aspect_custom_sun', 'show_toolbar', 'ca_rays'):
			self.assertEqual(values[key], tradoptions.DEFAULTS[key], key)
		self.assertNotIn('unknown', values)

	def test_removed_orb_options_are_ignored(self):
		# Files written before the course rules became fixed.
		values = self.load({'aspect_combine': 'average', 'aspect_boundary': 0})
		self.assertNotIn('aspect_combine', values)
		self.assertNotIn('aspect_boundary', values)

	def test_not_an_object_or_not_json(self):
		self.assertEqual(self.load([1, 2]), tradoptions.DEFAULTS)
		self.assertEqual(self.load('{'), tradoptions.DEFAULTS)

	def test_every_default_is_valid(self):
		for key, value in tradoptions.DEFAULTS.items():
			self.assertTrue(tradoptions.valid(key, value), key)


if __name__ == '__main__':
	unittest.main()

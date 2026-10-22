"""Tests for the Serbian translation; no wxPython or display required."""
import re
import unittest
import i18n
import i18n_sr
import mtexts
import mtexts_sr

FORMAT = re.compile(r'%[-+ #0]*\d*(?:\.\d+)?[sdfgrx%]')


def tables():
	"""Each Serbian table of mtexts_sr with the English table it overlays."""
	for name, sr in vars(mtexts_sr).items():
		if isinstance(sr, dict) and not name.startswith('_'):
			yield name, sr, getattr(mtexts, name + 'eng')


class MorinusTextsTests(unittest.TestCase):
	def tearDown(self):
		mtexts.setLang(0)

	def test_keys_are_english_keys(self):
		for name, sr, eng in tables():
			self.assertEqual(set(sr) - set(eng), set(), name)

	def test_shortcuts_and_formats_kept(self):
		for name, sr, eng in tables():
			for key, text in sr.items():
				self.assertEqual(text.partition('\t')[2], eng[key].partition('\t')[2], (name, key))
				self.assertEqual(FORMAT.findall(text), FORMAT.findall(eng[key]), (name, key))

	def test_serbian_language(self):
		self.assertEqual(mtexts.langtexts[3], 'Srpski (Serbian)')
		self.assertEqual(len(mtexts.langs[3]), len(mtexts.langs[0]))
		mtexts.setLang(3)
		self.assertEqual(mtexts.menutxts['HMNew'], '&Nova karta\tCtrl+N')
		self.assertEqual(mtexts.current, 3)


class TranslateTests(unittest.TestCase):
	def setUp(self):
		mtexts.setLang(3)

	def tearDown(self):
		mtexts.setLang(0)

	def test_formats_kept(self):
		for key, text in i18n_sr.TEXTS.items():
			self.assertEqual(FORMAT.findall(text.replace('%.0s', '%s')), FORMAT.findall(key), key)

	def test_menu_text(self):
		self.assertEqual(i18n.tr('Positions and data...\tCtrl+Shift+P'), 'Položaji i podaci...\tCtrl+Shift+P')
		self.assertEqual(i18n.tr('Theme:'), 'Tema:')

	def test_declined_phrases(self):
		self.assertEqual(i18n.tr('natal Sun'), 'natalno Sunce')
		self.assertEqual(i18n.tr('enters Leo'), 'ulazi u Lava')
		self.assertEqual(i18n.tr('Mars return...'), 'Povratak Marsa...')
		self.assertEqual(i18n.tr('the antiscion of Moon'), 'antiscija Lune')

	def test_lists_and_unknown(self):
		self.assertEqual(i18n.tr(['Day', 'Night']), ['Dan', 'Noć'])
		self.assertEqual(i18n.tr(('Day',)), ('Dan',))
		self.assertEqual(i18n.tr('Regulus'), 'Regulus')
		self.assertEqual(i18n.tr(7), 7)

	def test_plural_counter(self):
		self.assertEqual(i18n.tr('%d matching command%s') % (5, 's'), 'Pronađeno komandi: 5')

	def test_english_unchanged(self):
		mtexts.setLang(0)
		self.assertEqual(i18n.tr('Theme:'), 'Theme:')


if __name__ == '__main__':
	unittest.main()

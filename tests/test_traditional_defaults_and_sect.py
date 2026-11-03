"""Traditional defaults, the one sect rule, planetary hours near midnight, the
temperament natures of the lights, Ptolemy's ages and profection participators
(final audit, November 2026)."""
import os
import sys
import unittest
from types import SimpleNamespace as NS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
	import astrology
except ImportError:
	astrology = None

import multiwheel_highlight as mh


class PtolemaicAgesAndParticipators(unittest.TestCase):

	def test_ages(self):
		# Moon 0-3, Mercury 4-13, Venus 14-21, Sun 22-40, Mars 41-55, Jupiter 56-67, Saturn 68-
		cases = {0: (6, 0, 3), 3: (6, 0, 3), 4: (5, 4, 13), 13: (5, 4, 13), 14: (4, 14, 21), 22: (3, 22, 40),
			40: (3, 22, 40), 41: (2, 41, 55), 56: (1, 56, 67), 67: (1, 56, 67), 68: (0, 68, None), 95: (0, 68, None)}
		for age, expected in cases.items():
			self.assertEqual(mh.ptolemaic_age(age), expected, age)

	@staticmethod
	def chart(lons, ayan=0.0):
		return NS(planets=NS(planets=[NS(data=(lon,)) for lon in lons]), ayanamsha=ayan)

	def test_natal_first_then_solar(self):
		natal = self.chart([10, 40, 70, 100, 130, 160, 190])	# Saturn in Aries, ... Moon in Libra
		self.assertEqual(mh.participators(natal, 0), ([0], 'natal'))
		self.assertEqual(mh.participators(natal, 11), ([], None))
		solar = self.chart([335, 340, 1, 2, 3, 4, 5])
		self.assertEqual(mh.participators(natal, 11, solar), ([0, 1], 'solar'))
		# natal planets in the sign win over solar ones
		self.assertEqual(mh.participators(natal, 0, solar), ([0], 'natal'))

	def test_sidereal(self):
		natal = self.chart([32, 100, 100, 100, 100, 100, 100], ayan=24.0)
		self.assertEqual(mh.participators(natal, 0, sidereal=True)[0], [0])
		self.assertEqual(mh.participators(natal, 1)[0], [0])


class TraditionalDefaults(unittest.TestCase):

	def test_factory_defaults(self):
		import options
		import lots
		o = options.Options.__new__(options.Options)
		options.Options.__init__(o)
		self.assertFalse(o.def_oneruler)			# all three triplicity rulers
		self.assertTrue(o.def_useexaltationmercury)	# Mercury exalted in Virgo
		self.assertTrue(o.def_usedaynightorb)
		self.assertEqual(o.def_daynightorb, 3.0)
		self.assertEqual(o.def_dignityscores, [5, 4, 3, 2, 1])
		# Ibn Ezra's house points: I 12, X 11, VII 10, IV 9, XI 8, V 7, II 6, VIII 5, IX 4, III 3, XII 2, VI 1
		self.assertEqual(o.def_housescores, [12, 6, 3, 9, 7, 1, 10, 5, 4, 11, 8, 2])
		self.assertEqual(len(o.def_lots), 7)
		self.assertEqual(len(o.def_lotsvisible), 7)
		L = lots.Lots
		formulas = [l[1] for l in o.def_lots]
		self.assertEqual(formulas[0], (L.ASC, L.MOON, L.SUN))		# Fortune
		self.assertEqual(formulas[1], (L.ASC, L.SUN, L.MOON))		# Spirit
		self.assertTrue(all(l[3] for l in o.def_lots))				# reversed by night

	def test_tradoptions(self):
		import tradoptions
		self.assertEqual(tradoptions.DEFAULTS['speed_means'], 'traditional')
		self.assertEqual(tradoptions.DEFAULTS['temp_orb'], 6.0)
		self.assertEqual(tradoptions.DEFAULTS['temp_moon_orb'], 6.0)
		self.assertEqual(tradoptions.DEFAULTS['sect_ask_window'], 0.5)
		self.assertFalse(tradoptions.valid('speed_means', 'fast'))
		self.assertFalse(tradoptions.valid('sect_ask_window', 5.0))


@unittest.skipIf(astrology is None, 'sweastrology extension not built')
class TemperamentLights(unittest.TestCase):

	def test_sun_by_season_moon_by_phase(self):
		import traditional	# registers the swisseph module hor_tools needs
		from hor_tools.analysis import temperament as t
		t._LIGHTS['Sun'], t._LIGHTS['Moon'] = 10.0, 100.0		# spring; Moon 90 degrees ahead
		self.assertEqual(t._light_qualities('Sun'), {'hot', 'moist'})
		self.assertEqual(t._light_qualities('Moon'), {'hot', 'dry'})		# first quarter to full
		t._LIGHTS['Sun'], t._LIGHTS['Moon'] = 245.0, 80.0		# autumn (Sagittarius); Moon 195 ahead
		self.assertEqual(t._light_qualities('Sun'), {'cold', 'dry'})
		self.assertEqual(t._light_qualities('Moon'), {'cold', 'dry'})		# full to last quarter
		t._LIGHTS['Sun'], t._LIGHTS['Moon'] = 280.0, 270.0		# winter; Moon 350 ahead
		self.assertEqual(t._light_qualities('Sun'), {'cold', 'moist'})
		self.assertEqual(t._light_qualities('Moon'), {'cold', 'moist'})
		self.assertIsNone(t._light_qualities('Mars'))


@unittest.skipIf(astrology is None, 'sweastrology extension not built')
class RealCharts(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		astrology.swe_set_ephe_path(os.path.join(ROOT, 'SWEP', 'Ephem'))

	def time(self, t, p):
		import chart
		place = chart.Place(*p)
		return chart.Time(*(t + (place,))), place

	def test_planetary_hour_zone_and_local_midnight(self):
		import chart
		T = chart.Time
		names = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')
		belgrade = ('Beograd', 20, 28, 0, True, 44, 49, 0, True, 117)
		# 00:45 CEST = 00:07 local mean time: the night still belongs to Friday
		# 14 July 2023 (Morinus 6.2 went back to Thursday: Mercury).
		t, _ = self.time((2023, 7, 15, 0, 45, 0, False, T.GREGORIAN, T.ZONE, True, 1, 0, True), belgrade)
		self.assertEqual(names[t.ph.planetaryhour], 'Jupiter')
		self.assertEqual(t.ph.weekday, 4)
		# 23:59:30 zone time is after local mean midnight in Sydney: still Sunday's night
		t, _ = self.time((2001, 7, 22, 23, 59, 30, False, T.GREGORIAN, T.ZONE, True, 10, 0, False), ('Sydney', 151, 12, 0, True, 33, 52, 0, False, 0))
		self.assertEqual(names[t.ph.planetaryhour], 'Moon')
		# Julian calendar: 10 March 1500 (Julian) was a Tuesday, first hour Mars
		# (Morinus 6.2 read the date as Gregorian: Saturday)
		t, _ = self.time((1500, 3, 10, 6, 7, 0, False, T.JULIAN, T.LOCALMEAN, True, 0, 0, False), ('Rome', 12, 29, 0, True, 41, 54, 0, True, 0))
		self.assertEqual(t.ph.weekday, 1)
		self.assertEqual(names[t.ph.planetaryhour], 'Mars')
		# polar night: no sunrise, the date's weekday (Friday)
		t, _ = self.time((1990, 12, 21, 12, 0, 0, False, T.GREGORIAN, T.ZONE, True, 1, 0, False), ('Tromso', 18, 57, 0, True, 69, 39, 0, True, 0))
		self.assertEqual(t.ph.weekday, 4)

	def test_one_sect_and_the_question(self):
		import chart
		import options
		T = chart.Time
		opts = options.Options.__new__(options.Options)
		options.Options.__init__(opts)
		opts.usedaynightorb, opts.daynightorb = True, 3.0
		belgrade = ('Beograd', 20, 28, 0, True, 44, 49, 0, True, 117)
		asked = []
		try:
			chart.Chart.sectquestion = lambda c, arc: asked.append(arc) or False
			# find a time after sunset where the Sun is about 3 degrees (of the orb) below the horizon
			# (the orb runs at the Sun's diurnal motion: 3 degrees are about 12 minutes)
			for minute in range(30, 90):
				t, place = self.time((2023, 3, 20, 17 + minute // 60, minute % 60, 0, False, T.GREGORIAN, T.ZONE, True, 1, 0, False), belgrade)
				c = chart.Chart('t', True, t, place, chart.Chart.RADIX, '', opts, True)
				arc = c.sunArcBelowHorizon()
				if arc is not None and abs(arc - 3.0) < 0.3:
					break
			self.assertTrue(asked)
			self.assertFalse(c.isDaySect())			# the answer wins over the orb
			self.assertFalse(c.firdaria.isdaily)
			import lotswnd
			self.assertTrue(lotswnd.LotsWnd.isNightChart(c))
			# without a question (headless) the orb decides
			chart.Chart.sectquestion = None
			c = chart.Chart('t', True, t, place, chart.Chart.RADIX, '', opts, True)
			self.assertEqual(c.isDaySect(), arc < 3.0)
		finally:
			chart.Chart.sectquestion = None


if __name__ == '__main__':
	unittest.main()


@unittest.skipIf(astrology is None, 'sweastrology extension not built')
class HylegExamples(unittest.TestCase):
	"""Worked examples (birth data: Astro-Databank, AA)."""

	@classmethod
	def setUpClass(cls):
		astrology.swe_set_ephe_path(os.path.join(ROOT, 'SWEP', 'Ephem'))

	def calc(self, t, p):
		import chart
		import options
		import hyleg
		import tradoptions
		tradoptions.load()
		tradoptions.set(dict(tradoptions.values(), hyleg_places='wholesign'))
		opts = options.Options.__new__(options.Options)
		options.Options.__init__(opts)
		place = chart.Place(*p)
		c = chart.Chart('x', True, chart.Time(*(t + (place,))), place, chart.Chart.RADIX, '', opts, True)
		return hyleg, hyleg.calculate(c)

	def test_diana(self):
		import chart
		T = chart.Time
		h, r = self.calc((1961, 7, 1, 19, 45, 0, False, T.GREGORIAN, T.ZONE, True, 0, 0, True), ('Sandringham', 0, 30, 0, True, 52, 50, 0, True, 0))
		self.assertEqual(r.hyleg.key, 'moon')
		self.assertEqual(r.alcocoden, h.JUPITER)
		self.assertEqual(r.strength, h.SUCCEDENT)	# middle years 45.5, retrograde: a fifth less
		self.assertEqual(r.years[1], 45.5)

	def test_steve_jobs(self):
		import chart
		T = chart.Time
		h, r = self.calc((1955, 2, 24, 19, 15, 0, False, T.GREGORIAN, T.ZONE, False, 8, 0, False), ('San Francisco', 122, 25, 0, False, 37, 47, 0, True, 0))
		self.assertEqual(r.hyleg.key, 'sun')
		self.assertEqual(r.alcocoden, h.JUPITER)
		self.assertEqual(r.strength, h.ANGULAR)		# greater years 79
		self.assertEqual(r.years[0], 79)

	def test_elizabeth_hyleg(self):
		# the Moon is often taken as alcocoden for her mutual reception with the
		# Sun; by the written rules Venus has more dignity: only the hyleg is checked
		import chart
		T = chart.Time
		h, r = self.calc((1926, 4, 21, 2, 40, 0, False, T.GREGORIAN, T.ZONE, True, 0, 0, True), ('London', 0, 9, 0, False, 51, 31, 0, True, 0))
		self.assertEqual(r.hyleg.key, 'sun')
		self.assertIn(h.MOON, [row[0] for row in r.alcocodens])


class StarNatures(unittest.TestCase):
	"""Robson's list (Fiksne zvezde i sazvezdja u astrologiji, 1991, pp. 62-111)."""

	def test_robson_list(self):
		import starnatures as sn
		if not sn.catalogue():
			self.skipTest('no sefstars.txt')
		self.assertEqual(len(sn.ROWS), 111)
		self.assertEqual(len(sn.ENTRIES), 111)	# Orion's Belt has none; Aseli are two stars
		for name, planets in (('Aldebaran', ('Mars',)), ('Achernar', ('Jupiter',)), ('Almach', ('Venus',)),
				('Acrux', ('Jupiter',)), ('Agena', ('Venus', 'Jupiter')), ('Zubenelgenubi', ('Saturn', 'Mars')),
				('El Nath', ('Mars', 'Mercury')), ('Asellus Australis', ('Mars', 'Sun')), ('Deneb', ('Venus', 'Mercury')),
				('Deneb el Okab Australis', ('Mars', 'Jupiter'))):
			self.assertEqual(sn.nature(name), (planets, True), name)
		# printed as Neptune and Saturn; Ptolemy: Jupiter and Saturn
		self.assertEqual(sn.nature('Alnilam'), (('Jupiter', 'Saturn'), True))
		self.assertEqual(sn.describe('Alhena'), 'Mercury or Venus')
		self.assertEqual(sn.nature('Vertex'), (('Mars', 'Moon'), True))		# alias
		self.assertEqual(sn.nature(nomenclature='alTau'), (('Mars',), True))
		# stars Robson does not describe have no nature
		for name in ('Alioth', 'Rasalgethi', 'Dubhe', 'No such star'):
			self.assertIsNone(sn.nature(name), name)
		self.assertIsNone(sn.nature(nomenclature='thTau'))

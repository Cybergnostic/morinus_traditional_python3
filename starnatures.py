"""The natures of the fixed stars as Vivian Robson gives them ("Fiksne zvezde i
sazvezdja u astrologiji", Decje novine 1991, chapter V, the numbered
descriptions on pages 62-111): the planets each star is like, the first the
stronger (natal/basic lesson 11: "the nature of a star is expressed by one or
two planets"). Later writers' attributions (Alvidas, Simmonite, Wilson,
Pearce) are kept apart from the main nature. A star Robson does not describe
has no nature here.

One deliberate difference from the printed book: Alnilam is printed as
"Neptune and Saturn, according to Ptolemy", which cannot be Ptolemy's; the
course (basic lesson 11) gives Jupiter and Saturn, which is used.

No wx: used by the tables and tested headless."""

import os

ROWS = [
	(1, 'Ahernar', 'Jupiter', '', 62),
	(2, 'Akruks', 'Jupiter', '', 62),
	(3, 'Akubens', 'Saturn + Mercury', '', 62),
	(4, 'Akuleus', 'Mars + Moon', '', 62),
	(5, 'Akumen', 'Mars + Moon', 'Same nature as Akuleus (stated by Robson).', 62),
	(6, 'Adhafera', 'Saturn + Mercury', '', 62),
	(7, 'Agena', 'Venus + Jupiter', 'Alvidas: Mars conjunct Mercury.', 62),
	(8, 'Albireo', 'Venus + Mercury', '', 63),
	(9, 'Alkione', 'Mars + Moon', '', 63),
	(10, 'Aldebaran', 'Mars', 'Alvidas: Mercury + Mars + Jupiter.', 63),
	(11, 'Algenib', 'Mars + Mercury', '', 65),
	(12, 'Algenubi', 'Saturn + Mars', '', 65),
	(13, 'Algol', 'Saturn + Jupiter', '', 65),
	(14, 'Algorab', 'Mars + Saturn', '', 66),
	(15, 'Al Heka', 'Mars', 'Alvidas: Mercury conjunct Saturn.', 66),
	(16, 'Alhena', 'Mercury OR Venus', 'Alvidas: Moon + Venus.', 67),
	(17, 'Al-Dzabha', 'Saturn + Mercury', '', 67),
	(18, 'Almah', 'Venus', '', 68),
	(19, 'Alnilam', 'Neptune + Saturn', 'Alvidas: Mercury + Saturn.', 68),
	(20, 'Alfard', 'Saturn + Venus', 'Alvidas: Sun sextile Jupiter.', 68),
	(21, 'Alfeka', 'Venus + Mercury', 'Alvidas: Mars + Mercury.', 69),
	(22, 'Alferac', 'Jupiter + Venus', 'Alvidas adds Mars to Jupiter + Venus.', 70),
	(23, 'Al Ferg', 'Saturn + Jupiter', '', 71),
	(24, 'Altair', 'Mars + Jupiter', 'Wilson: Saturn + Mercury; Simmonite: Uranus; Alvidas: Uranus and Mercury sextile Sun.', 71),
	(25, 'Antares', 'Mars + Jupiter', 'Alvidas: Jupiter sextile Venus.', 71),
	(26, 'Arkturus', 'Mars + Jupiter', 'Alvidas: Venus conjunct Mercury.', 73),
	(27, 'Armus', 'Mars + Mercury', '', 73),
	(28, 'Ascela', 'Jupiter + Mercury', '', 74),
	(29, 'Aseli (North and South)', 'Mars + Sun', 'Alvidas: North Asellus - Sun sextile Mars; South Asellus - Sun and Mars in semisquare.', 74),
	(30, 'Baten Kaitos', 'Saturn', '', 75),
	(31, 'Belatriks', 'Mars + Mercury', 'Alvidas: favorable Mercury-Mars aspect.', 75),
	(32, 'Betelgez', 'Mars + Mercury', 'Alvidas: favorable aspect of Mercury, Saturn and Jupiter.', 76),
	(33, 'Bos', 'Saturn + Venus', '', 77),
	(34, 'Bungula', 'Venus + Jupiter', 'Alvidas: Mars with Moon and Uranus in Scorpio.', 77),
	(35, 'Kanopus', 'Saturn + Jupiter', 'Alvidas: Moon + Mars.', 78),
	(36, 'Kapela', 'Mars + Mercury', 'Alvidas: Mercury + Moon.', 78),
	(37, 'Kafir', 'Mercury + Venus', 'Simmonite: Mercury alone; Alvidas: Venus + Mercury.', 79),
	(38, 'Kapulus', 'Mars + Mercury', '', 80),
	(39, 'Kastor', 'Mercury', 'Wilson, Simmonite and Pearce: Mars + Venus + Saturn; Alvidas: Moon + Mars + Uranus.', 80),
	(40, 'Kastra', 'Saturn + Jupiter', '', 81),
	(41, "Cingula Orionis (Orion's Belt)", 'Not assigned separately', 'Robson refers to the separate natures of Mintaka and Alnilam.', 81),
	(42, 'Kopula', 'Moon + Venus', '', 81),
	(43, 'Dabih', 'Saturn + Venus', 'Alvidas: Uranus conjunct Saturn, square Mercury.', 81),
	(44, 'Deneb', 'Mars + Jupiter', '', 82),
	(45, 'Deneb Adige', 'Venus + Mercury', '', 82),
	(46, 'Deneb Algedi', 'Saturn + Jupiter', 'Alvidas: Uranus + Mercury in Aquarius opposing Saturn in Leo.', 82),
	(47, 'Denebola', 'Saturn + Venus', 'Wilson and Pearce: Saturn + Venus + Mercury; Simmonite: Uranus; Alvidas: Mercury + Uranus + Mars.', 83),
	(48, 'Difda', 'Saturn', 'Alvidas: Mars + Saturn + Mercury.', 84),
	(49, 'Dirah', 'Mercury + Venus', '', 84),
	(50, 'Dorsum', 'Saturn + Jupiter', '', 84),
	(51, 'El-Nat', 'Mars + Mercury', '', 84),
	(52, 'Ensis', 'Mars + Moon', '', 85),
	(53, 'Facies', 'Sun + Mars', '', 85),
	(54, 'Fomalhaut', 'Venus + Mercury', 'Alvidas: Jupiter square Saturn in Pisces and Sagittarius.', 85),
	(55, 'Foramen', 'Saturn + Jupiter', '', 86),
	(56, 'Giedi', 'Venus + Mars', 'Simmonite: Venus + Mercury; Alvidas: Uranus sextile Venus.', 86),
	(57, 'Grafias', 'Mars + Saturn', 'Alvidas: Jupiter square Saturn, with Moon also indicated.', 87),
	(58, 'Hamal', 'Mars + Saturn', 'Alvidas: Venus + Saturn.', 88),
	(59, 'Han', 'Saturn + Venus', '', 88),
	(60, 'Isidis', 'Mars + Saturn', 'Alvidas: Jupiter square Moon.', 88),
	(61, 'Kambalia', 'Mercury + Mars', '', 89),
	(62, 'Labrum', 'Venus + Mercury', '', 89),
	(63, 'Lesat', 'Mercury + Mars', '', 89),
	(64, 'Manubrium', 'Sun + Mars', '', 89),
	(65, 'Markab', 'Mars + Mercury', 'Simmonite: Mars + Venus; Alvidas: Jupiter square Mercury and Saturn.', 89),
	(66, 'Markeb', 'Saturn + Jupiter', '', 90),
	(67, 'Menkalinan', 'Mars + Mercury', '', 90),
	(68, 'Menkar', 'Saturn', 'Simmonite: Mars; Alvidas: Venus + Moon.', 90),
	(69, 'Mintaka', 'Saturn + Mercury', 'Alvidas: Mercury + Saturn + Jupiter.', 91),
	(70, 'Mirah', 'Venus', 'Alvidas: Mars + Moon.', 92),
	(71, 'Nasira', 'Saturn + Jupiter', 'Simmonite: Saturn alone.', 92),
	(72, 'Okulus', 'Saturn + Venus', '', 92),
	(73, 'Pelagus', 'Jupiter + Mercury', 'Alvidas: Saturn + Mercury.', 92),
	(74, 'Fakt', 'Venus + Mercury', '', 93),
	(75, 'Plejade (Pleiades)', 'Moon + Mars', 'Alvidas: Mars + Moon + Sun in opposition.', 93),
	(76, 'Polaris', 'Saturn + Venus', '', 94),
	(77, 'Polis', 'Jupiter + Mars', '', 95),
	(78, 'Poluks', 'Mars', 'Alvidas: Moon + Mars + Uranus.', 95),
	(79, 'Prezepe', 'Mars + Moon', '', 96),
	(80, 'Prima Hiadum', 'Saturn + Mercury', 'Alvidas: Mercury + Mars; Simmonite: Mars (Robson considers this probably erroneous).', 96),
	(81, 'Princeps', 'Mercury + Saturn', '', 97),
	(82, 'Prokion', 'Mercury + Mars', 'Simmonite: Venus + Mars (Robson suggests printing error); Alvidas: Moon + Jupiter + Uranus.', 97),
	(83, 'Propus', 'Mercury + Venus', '', 98),
	(84, 'Rasalhag', 'Saturn + Venus', 'Alvidas: Jupiter + Mercury, sextile Mars.', 98),
	(85, 'Rastaban', 'Saturn + Mars', '', 99),
	(86, 'Regulus', 'Mars + Jupiter', 'Many later writers: Mars alone; Alvidas: favorable aspect of Sun and Uranus.', 99),
	(87, 'Rigel', 'Jupiter + Saturn', 'Later writers: Jupiter + Mars; Alvidas: Mercury + Mars + Jupiter.', 101),
	(88, 'Sabik', 'Saturn + Venus', 'Alvidas: Jupiter + Venus.', 101),
	(89, 'Sadalmelik', 'Saturn + Mercury', 'Simmonite: Saturn + Jupiter; Alvidas: Jupiter and Uranus sextile Sun in Pisces or Taurus.', 102),
	(90, 'Sadalsuud', 'Saturn + Mercury', 'Simmonite: Uranus; Alvidas: Sun sextile Uranus.', 103),
	(91, 'Severna Skala', 'Jupiter + Mercury', 'Later writers: Jupiter + Mars; Alvidas: Mars sextile Jupiter.', 103),
	(92, 'Juzna Skala', 'Saturn + Mars', 'Later writers: Saturn + Venus, or Saturn + Mercury; Alvidas: Mars + Venus + Saturn.', 104),
	(93, 'Skeat', 'Mars + Mercury', 'Simmonite: Saturn; others: Saturn + Mercury; Alvidas: Neptune square Saturn or Mars.', 105),
	(94, 'Seginus', 'Mercury + Saturn', '', 105),
	(95, 'Saratan', 'Mars + Saturn', '', 105),
	(96, 'Sinistra', 'Saturn + Venus', '', 106),
	(97, 'Sirijus', 'Jupiter + Mars', 'Alvidas: Moon + Jupiter + Mars.', 106),
	(98, 'Skat', 'Saturn + Jupiter', 'Simmonite: Uranus; Alvidas: Uranus and Venus sextile Mercury.', 106),
	(99, 'Spica', 'Venus + Mars', 'Alvidas: Venus + Jupiter + Mercury.', 107),
	(100, 'Spikulum', 'Mars + Moon', '', 108),
	(101, 'Tedzat', 'Mercury + Venus', '', 108),
	(102, 'Terebelum', 'Venus + Saturn', '', 108),
	(103, 'Unukalhai', 'Saturn + Mars', 'Simmonite: Saturn + Venus; Pearce: Saturn + Venus + Mars; Alvidas: Mars and Saturn opposing Venus.', 108),
	(104, 'Verteks', 'Mars + Moon', '', 109),
	(105, 'Vindemiatriks', 'Saturn + Mercury', 'Simmonite: Saturn + Venus (Robson suggests printing error); Wilson and Pearce: Saturn + Venus + Mercury; Alvidas: adverse Mercury-Saturn aspect.', 109),
	(106, 'Vasat', 'Saturn', '', 110),
	(107, 'Vega', 'Venus + Mercury', 'Alvidas: Saturn trine Jupiter in earth signs.', 110),
	(108, 'Jed Prior', 'Saturn + Venus', '', 110),
	(109, 'Zanija', 'Mercury + Venus', 'Alvidas: Venus sextile Mercury.', 111),
	(110, 'Zavijava', 'Mercury + Mars', '', 111),
	(111, 'Zosma', 'Saturn + Venus', '', 111),
]

# Robson's (Serbian) names -> names in the Swiss Ephemeris catalogue
# (sefstars.txt); None: not in the catalogue by name (kept by Robson's name)
CATALOGUE_NAMES = {
	'Ahernar': 'Achernar', 'Akruks': 'Acrux', 'Akubens': 'Acubens', 'Akuleus': 'Aculeus', 'Akumen': 'Acumen',
	'Adhafera': 'Adhafera', 'Agena': 'Agena', 'Albireo': 'Albireo', 'Alkione': 'Alcyone', 'Aldebaran': 'Aldebaran',
	'Algenib': 'Algenib', 'Algenubi': 'Ras Elased Australis', 'Algol': 'Algol', 'Algorab': 'Algorab', 'Al Heka': 'Al Hecka',
	'Alhena': 'Alhena', 'Al-Dzabha': 'Al Jabhah', 'Almah': 'Almach', 'Alnilam': 'Alnilam', 'Alfard': 'Alphard',
	'Alfeka': 'Alphecca', 'Alferac': 'Alpheratz', 'Al Ferg': 'Al Pherg', 'Altair': 'Altair', 'Antares': 'Antares',
	'Arkturus': 'Arcturus', 'Armus': 'Armus', 'Ascela': 'Ascella', 'Baten Kaitos': 'Baten Kaitos', 'Belatriks': 'Bellatrix',
	'Betelgez': 'Betelgeuse', 'Bos': 'Bos', 'Bungula': 'Rigil Kentaurus', 'Kanopus': 'Canopus', 'Kapela': 'Capella',
	'Kafir': 'Porrima', 'Kapulus': 'Capulus', 'Kastor': 'Castor', 'Kastra': 'Castra', 'Kopula': None, 'Dabih': 'Dabih',
	'Deneb': 'Deneb el Okab Australis', 'Deneb Adige': 'Deneb', 'Deneb Algedi': 'Deneb Algedi', 'Denebola': 'Denebola',
	'Difda': 'Difda', 'Dirah': 'Tejat', 'Dorsum': 'Dorsum', 'El-Nat': 'El Nath', 'Ensis': 'Orion Nebula', 'Facies': 'Facies',
	'Fomalhaut': 'Fomalhaut', 'Foramen': 'Foramen', 'Giedi': 'Algedi', 'Grafias': 'Graffias', 'Hamal': 'Hamal', 'Han': 'Han',
	'Isidis': 'Dschubba', 'Kambalia': 'Khambalia', 'Labrum': 'Labrum', 'Lesat': 'Lesath', 'Manubrium': None,
	'Markab': 'Markab', 'Markeb': 'Markeb', 'Menkalinan': 'Menkalinan', 'Menkar': 'Menkar', 'Mintaka': 'Mintaka',
	'Mirah': 'Mirach', 'Nasira': 'Nashira', 'Okulus': 'Oculus', 'Pelagus': 'Nunki', 'Fakt': 'Phact',
	'Plejade (Pleiades)': None, 'Polaris': 'Polaris', 'Polis': 'Polis', 'Poluks': 'Pollux', 'Prezepe': 'Praesepe Cluster',
	'Prima Hiadum': 'Prima Hyadum', 'Princeps': 'Princeps', 'Prokion': 'Procyon', 'Propus': 'Propus iotGem',
	'Rasalhag': 'Rasalhague', 'Rastaban': 'Rastaban', 'Regulus': 'Regulus', 'Rigel': 'Rigel', 'Sabik': 'Sabik',
	'Sadalmelik': 'Sadalmelik', 'Sadalsuud': 'Sadalsuud', 'Severna Skala': 'Zubeneshamali', 'Juzna Skala': 'Zubenelgenubi',
	'Skeat': 'Scheat', 'Seginus': 'Seginus', 'Saratan': 'Sheratan', 'Sinistra': 'Sinistra', 'Sirijus': 'Sirius',
	'Skat': 'Skat', 'Spica': 'Spica', 'Spikulum': None, 'Tedzat': 'Propus', 'Terebelum': None, 'Unukalhai': 'Unukalhai',
	'Verteks': 'Andromeda Galaxy', 'Vindemiatriks': 'Vindemiatrix', 'Vasat': 'Wasat', 'Vega': 'Vega', 'Jed Prior': 'Yed Prior',
	'Zanija': 'Zaniah', 'Zavijava': 'Zavijava', 'Zosma': 'Zosma', 'Mirah': 'Mirach',
	'Aseli (North and South)': ('Asellus Borealis', 'Asellus Australis'),
	'Cingula Orionis (Orion\'s Belt)': None,
}
# English names of the stars that the catalogue does not have by name
OTHER_NAMES = {'Kopula': 'Copula', 'Manubrium': 'Manubrium', 'Plejade (Pleiades)': 'Pleiades', 'Spikulum': 'Spiculum',
	'Terebelum': 'Terebellum'}
COURSE = {'Alnilam': ('Jupiter', 'Saturn')}	# see the module text


class Entry:
	def __init__(self, number, robson, planets, either, others, page, name):
		self.number = number
		self.robson = robson		# Robson's (Serbian) name
		self.planets = planets		# tuple of planet names
		self.either = either		# "Mercury or Venus": one or the other
		self.others = others		# later writers' attributions (English)
		self.page = page
		self.name = name			# catalogue (or English) name


def _entries():
	out = []
	for number, robson, main, others, page in ROWS:
		target = CATALOGUE_NAMES.get(robson)
		if main.startswith('Not assigned'):
			continue			# Orion's Belt: see Mintaka and Alnilam
		either = ' OR ' in main
		planets = tuple(p.strip() for p in main.replace(' OR ', ' + ').split('+'))
		names = target if isinstance(target, tuple) else (target or OTHER_NAMES.get(robson, robson),)
		for name in names:
			planets_used = COURSE.get(name, planets)
			out.append(Entry(number, robson, planets_used, either, others, page, name))
	return out


ENTRIES = _entries()
NATURES = {e.name: e.planets for e in ENTRIES}
BYNAME = {e.name: e for e in ENTRIES}

# Other spellings of the same stars (hor_tools, older catalogues)
ALIASES = {'Vertex': 'Andromeda Galaxy', 'Praesepe': 'Praesepe Cluster', 'Algenubi': 'Ras Elased Australis',
	'Al Jabbah': 'Al Jabhah', 'Isidis': 'Dschubba', 'Ras Alhague': 'Rasalhague', 'Deneb Okab': 'Deneb el Okab Australis',
	'Deneb Kaitos': 'Difda', 'Diphda': 'Difda', 'Alpherg': 'Al Pherg', 'Ensis': 'Orion Nebula', 'Bungula': 'Rigil Kentaurus',
	'Deneb Adige': 'Deneb', 'Acrab': 'Graffias', 'Akrab': 'Graffias', 'Sadalmelek': 'Sadalmelik', 'Rasalgethi': None,
	'Zuben Elgenubi': 'Zubenelgenubi', 'Zuben Eschamali': 'Zubeneshamali', 'Alrescha': None}

_catalogue = None


def catalogue():
	"""{catalogue name: nomenclature} of sefstars.txt (several names may share one star)."""
	global _catalogue
	if _catalogue is None:
		_catalogue = {}
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SWEP', 'Ephem', 'sefstars.txt')
		try:
			with open(path, encoding='latin-1') as f:
				for line in f:
					if line.startswith('#') or ',' not in line:
						continue
					name, nomen = [x.strip() for x in line.split(',')[:2]]
					_catalogue.setdefault(name, nomen)
		except OSError:
			pass
	return _catalogue


_nomen = None


def entry(name=None, nomenclature=None):
	"""Robson's Entry for a star given by name or by nomenclature ('alTau'); None if he gives no nature."""
	global _nomen
	if name is not None:
		name = name.strip()
		name = ALIASES.get(name, name)
		if name in BYNAME:
			return BYNAME[name]
		if nomenclature is None:
			nomenclature = catalogue().get(name)
	if nomenclature:
		if _nomen is None:
			cat = catalogue()
			_nomen = {cat[e.name]: e for e in ENTRIES if e.name in cat}
		return _nomen.get(nomenclature)
	return None


def nature(name=None, nomenclature=None):
	"""(planets, True) of a star, or None when Robson gives it no nature."""
	e = entry(name, nomenclature)
	return (e.planets, True) if e else None


def text(planets, own=True, tr=lambda s: s, either=False):
	"""'Mars, Jupiter' ('Mercury or Venus' for Robson's either-or)."""
	return (' %s ' % tr('or')).join(tr(p) for p in planets) if either else ', '.join(tr(p) for p in planets)


def describe(name, tr=lambda s: s):
	"""The nature of a star as text, '-' when there is none."""
	e = entry(name)
	return text(e.planets, True, tr, e.either) if e else '-'

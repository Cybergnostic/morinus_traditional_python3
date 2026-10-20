"""Fixed star names and lookup for the Swiss Ephemeris 2.10 catalogue (sefstars.txt).

The catalogue names some stars differently from the one of Morinus 6.2
(fixstars.cat), e.g. Pushya for Asellus Australis or Rigil Kentaurus for
Bungula, and lists many stars more than once under other names. Morinus keeps
the names it had and shows each star once; a few designations were renamed, and
stars that are no longer in the catalogue are left out instead of failing."""

import os
import astrology

CATALOGUE = 'sefstars.txt'

# designations of fixstars.cat that sefstars.txt writes differently
ALIASES = {'al-1Cru': 'alCru', 'omiLMi': '46LMi', 'roCap': 'rhCap'}

# the names of fixstars.cat where Swiss Ephemeris 2.10 gives another one
TRADITIONAL = {
	'16Tau': 'Caleano', '21Tau': 'Sterope I', '80Uma': 'Saidak', 'M31': 'Andromeda',
	'al-2Cap': 'Algedi2', 'al-2Lib': 'Zuben Elgenubi', 'alAnd': 'Sirrah', 'alCen': 'Bungula',
	'alCrB': 'Gemma', 'alOri': 'Beteigeuse', 'beCen': 'Agena', 'beCep': 'Alfirk', 'beCet': 'Difda',
	'beDra': 'Rastaban', 'beLib': 'Zuben Eshamali', 'beOph': 'Kelb Alrai', 'beTau': 'El Nath',
	'de-1Tau': 'Hyadum II', 'deAql': 'Deneb Okab', 'deCnc': 'Asellus Australis', 'deDra': 'Altais',
	'deLib': 'Zuben Elakribi', 'deSgr': 'Kaus Medis', 'epAur': 'Al Anz', 'epCMa': 'Adhara',
	'etLeo': 'Algieba', 'etUMa': 'Benetnash', 'ga-1And': 'Almak', 'ga-2Vel': 'Regor', 'gaCyg': 'Sadr',
	'gaGem': 'Almeisan', 'gaGru': 'Al Dhanab', 'gaLib': 'Zuben Elakrab', 'gaLyr': 'Sulafat',
	'gaTau': 'Hyadum I', 'ioAql': 'Al Thalimaim', 'ioOri': 'Nair al Saif',
	'ioUMa': 'Talitha Borealis', 'kaHer': 'Marfik', 'laAql': 'Al Thalimaim', 'laHer': 'Maasym',
	'laSco': 'Shaula', 'muLeo': 'Rasalas', 'nu-1Sgr': 'Ain al Rami', 'nuLib': 'Zuben Hakrabi',
	'ome-1Cyg': 'Ruchbah', 'ome-2Cyg': 'Ruchbah', 'omeDra': 'Alathfar', 'omeHer': 'Kajam',
	'taCrB': 'The Blaze Star', 'taPeg': 'Salm', 'thLeo': 'Chort', 'up-2Hya': 'Minchir',
	'xiPup': 'Asmidiske', 'zeAql': 'Dheneb', 'zeAur': 'Hoedus I', 'zeCnc': 'Tegmine',
	'zeDra': 'Aldhibah', 'zePer': 'Atik'
}


def lookup(nom, tjd_ut, flag):
	"""(name, designation, positions) of a star by its designation, or None."""
	ret, name, dat, serr = astrology.swe_fixstar_ut(',' + ALIASES.get(nom, nom), tjd_ut, flag)
	if ret[0] < 0:
		return None
	name = name[0].split(',')[0].strip()
	return TRADITIONAL.get(nom, name), nom, dat


def catalogue(ephepath):
	"""(name, designation) of every star in the catalogue once, in its order."""
	seen = set()
	out = []
	with open(os.path.join(ephepath, CATALOGUE), encoding='latin-1') as f:
		for line in f:
			if line.startswith('#') or line.count(',') < 2:
				continue
			name, nom = [x.strip() for x in line.split(',')[:2]]
			if not nom or nom in seen:
				continue
			seen.add(nom)
			out.append((TRADITIONAL.get(nom, name), nom))
	return out

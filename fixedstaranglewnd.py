"""Fixed stars on the angles at the birth and the paranatellonta of the birth day,
as a native Morinus table."""

import wx
import common
import tablewnd
import fixedstarangles as fsa
import zodiacalreleasing as zr

AT_BIRTH = ('Star', 'Angle', 'Time', 'From the birth')
PARANS = ('', 'Angle', 'Star', 'Angle', 'Time', 'Apart')


class FixedStarAnglesWnd(tablewnd.TableWnd):

	def __init__(self, parent, chrt, options, mainfr):
		tablewnd.TableWnd.__init__(self, parent, chrt, options, mainfr)
		jd = chrt.time.jd
		at = [[name, '%s (%s)' % (fsa.ANGLES[ai][1], fsa.ANGLES[ai][2]), zr.datestr(chrt, t, True), '%+.1f min' % ((t - jd) * 1440.0)]
			for name, ai, t in fsa.at_birth(chrt)]
		pr, colours = [], []
		for pl, pai, name, sai, pt, st in fsa.parans(chrt):
			pr.append([(tablewnd.GLYPH, common.common.planets[pl]), fsa.ANGLES[pai][1], name, fsa.ANGLES[sai][1],
				zr.datestr(chrt, pt, True), '%.1f min' % (abs(pt - st) * 1440.0)])
			colours.append(self.options.clrplanets[pl])
		minutes, paran = fsa.tradoptions.get('fsa_minutes'), fsa.tradoptions.get('fsa_paranminutes')
		self.sections = [tablewnd.Section(at or [['none within %d minutes' % minutes, '', '', '']], AT_BIRTH),
			tablewnd.Section(pr or [['', '', 'none', '', '', '']], PARANS, colours or None)]
		self.notes = ['Above: stars on an angle within %d minutes of the birth. Below: paranatellonta of the birth day, a planet and a star on angles within %d minutes.' % (minutes, paran),
			'Stars from Options > Fixed stars; times in the time of the chart.']
		self.layout()

	def getExt(self):
		return '_StarAngles'


class FixedStarAnglesFrame(tablewnd.TableFrame):

	def __init__(self, parent, title, chrt, options):
		tablewnd.TableFrame.__init__(self, parent, title + ' - Fixed stars on the angles', lambda f: FixedStarAnglesWnd(f, chrt, options, parent))

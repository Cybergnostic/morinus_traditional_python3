"""The natures of the fixed stars as a Morinus table, in zodiacal order."""

import i18n
import wx
import astrology
import starnatures
import tablewnd

HEADERS = ('Star', 'Longitude', 'Latitude', 'Magnitude', 'Nature')


def rows(chrt):
	out, unplaced = [], []
	flag = astrology.SEFLG_SWIEPH
	cat = starnatures.catalogue()
	for e in starnatures.ENTRIES:
		cells = [i18n.tr(e.name)]
		nature = starnatures.text(e.planets, True, i18n.tr, e.either)
		nomen = cat.get(e.name)
		dat = None
		if nomen is not None:
			try:
				ret, found, dat, serr = astrology.swe_fixstar_ut(',' + nomen, chrt.time.jd, flag)
				if ret[0] < 0:
					dat = None
			except Exception:
				dat = None
		if dat is None:
			unplaced.append(cells + ['-', '', '', nature])
			continue
		try:
			magtxt = '%.2f' % astrology.swe_fixstar_mag(',' + nomen)[2][0]
		except Exception:
			magtxt = ''
		out.append((dat[0], cells + [(tablewnd.POSITION, dat[0]), '%+.2f\xb0' % dat[1], magtxt, nature]))
	out.sort(key=lambda r: r[0])
	return [cells for lon, cells in out] + unplaced


class StarNaturesWnd(tablewnd.TableWnd):

	def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
		tablewnd.TableWnd.__init__(self, parent, chrt, options, mainfr, id, size)
		self.sections = [tablewnd.Section(rows(chrt), HEADERS)]
		self.layout()

	def getExt(self):
		return '_StarNatures'


class StarNaturesFrame(tablewnd.TableFrame):

	def __init__(self, parent, title, chrt, options):
		tablewnd.TableFrame.__init__(self, parent, title + ' - ' + i18n.tr('Natures of the fixed stars'), lambda f: StarNaturesWnd(f, chrt, options, parent))

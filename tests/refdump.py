# Headless regression dump of Morinus calculations.
#
# Runs unchanged on Python 2 (original code) and Python 3 (ported code):
#   python refdump.py <morinus-dir> <out.json>
# The dumps are then compared with refcompare.py.

import os
import sys
import json
import types


def stub_wx():
	# The calculation modules only touch wx for error dialogs.
	class Anything(object):
		def __init__(self, *a, **k):
			pass
		def __call__(self, *a, **k):
			return Anything()
		def __getattr__(self, name):
			return Anything()
		def __or__(self, other):
			return 0
		__ror__ = __or__

	class WxModule(types.ModuleType):
		def __getattr__(self, name):
			return Anything

	sys.modules['wx'] = WxModule('wx')


MAXDEPTH = 14
SKIPKEYS = set(['options', 'abort', 'win', 'parent'])


def text(s):
	if isinstance(s, bytes) and not isinstance(s, str):
		return s.decode('utf-8', 'replace')
	if sys.version_info[0] < 3 and isinstance(s, str):
		return s.decode('utf-8', 'replace')
	return s


def dump(o, path=(), depth=0):
	if depth > MAXDEPTH:
		return '<depth>'
	if o is None or isinstance(o, bool):
		return o
	if isinstance(o, float):
		if o != o:
			return 'nan'
		if o in (float('inf'), float('-inf')):
			return repr(o)
		return o
	if isinstance(o, int) or type(o).__name__ == 'long':
		return int(o)
	if isinstance(o, (str, bytes)) or type(o).__name__ == 'unicode':
		return text(o)
	if id(o) in path:
		return '<cycle>'
	path = path+(id(o),)
	if isinstance(o, (list, tuple)):
		return [dump(x, path, depth+1) for x in o]
	if isinstance(o, (set, frozenset)):
		return sorted([dump(x, path, depth+1) for x in o], key=repr)
	if isinstance(o, dict):
		return dict((text(str(k)), dump(v, path, depth+1)) for k, v in o.items())
	if hasattr(o, 'isoformat'):
		return o.isoformat()
	if isinstance(o, (types.ModuleType, types.FunctionType, types.MethodType, type)):
		return '<'+type(o).__name__+'>'
	if hasattr(o, '__dict__'):
		res = {'__class__': o.__class__.__name__}
		for k, v in o.__dict__.items():
			if k in SKIPKEYS:
				continue
			res[k] = dump(v, path, depth+1)
		return res
	return '<'+type(o).__name__+'>'


def main():
	mdir = os.path.abspath(sys.argv[1])
	out = os.path.abspath(sys.argv[2])

	try:
		import wx
	except ImportError:
		stub_wx()

	sys.path.insert(0, mdir)
	os.chdir(mdir)

	import chart
	import options
	import primdirs
	import placidiansapd
	import placidianutppd
	import regiomontanpd
	import campanianpd
	import transits
	import revolutions
	import suntransits
	import secdir
	import profections
	import munprofections
	import ephemcalc
	import pdsinchart
	import astrology

	# as MFrame.__init__ does (common.Common().ephepath)
	os.environ['SE_EPHE_PATH'] = ''
	astrology.swe_set_ephe_path(os.path.join('SWEP', 'Ephem'))

	T = chart.Time
	#name: (y, m, d, h, mi, s, bc, cal, zt, plus, zh, zm, dst), (place, lond, lonm, lons, east, latd, latm, lats, north, alt)
	CHARTS = [
		('budapest', (1975, 4, 13, 14, 30, 0, False, T.GREGORIAN, T.ZONE, True, 1, 0, False), ('Budapest', 19, 3, 0, True, 47, 30, 0, True, 100)),
		('newyork', (1952, 11, 3, 3, 15, 27, False, T.GREGORIAN, T.ZONE, False, 5, 0, False), ('New York', 74, 0, 21, False, 40, 42, 51, True, 10)),
		('sydney', (2001, 7, 22, 23, 59, 30, False, T.GREGORIAN, T.ZONE, True, 10, 0, False), ('Sydney', 151, 12, 0, True, 33, 52, 0, False, 0)),
		('tromso', (1990, 12, 21, 12, 0, 0, False, T.GREGORIAN, T.ZONE, True, 1, 0, False), ('Tromso', 18, 57, 0, True, 69, 39, 0, True, 0)),
		('rome_julian', (1500, 3, 10, 6, 7, 0, False, T.JULIAN, T.LOCALMEAN, True, 0, 0, False), ('Rome', 12, 29, 0, True, 41, 54, 0, True, 0)),
		('london_dst_lat', (1930, 6, 15, 9, 45, 0, False, T.GREGORIAN, T.LOCALAPPARENT, True, 0, 0, False), ('London', 0, 7, 0, False, 51, 30, 0, True, 0)),
		('greenwich_dst', (2010, 8, 1, 18, 20, 0, False, T.GREGORIAN, T.GREENWICH, True, 0, 0, True), ('Lima', 77, 2, 0, False, 12, 2, 0, False, 150)),
		('bc', (100, 5, 5, 12, 0, 0, True, T.JULIAN, T.LOCALMEAN, True, 0, 0, False), ('Alexandria', 29, 55, 0, True, 31, 12, 0, True, 0)),
	]

	results = {}

	def run(key, fn):
		try:
			results[key] = dump(fn())
		except Exception as e:
			results[key] = 'ERROR: %s: %s' % (type(e).__name__, e)
		sys.stderr.write('%s\n' % key)

	def mkchart(name, opts, full=True, htype=chart.Chart.RADIX):
		for cname, t, p in CHARTS:
			if cname == name:
				place = chart.Place(*p)
				time = T(*(t+(place,)))
				return chart.Chart(cname, True, time, place, htype, '', opts, full)

	def defopts():
		opts = options.Options()
		return opts

	for cname, t, p in CHARTS:
		run('chart/%s' % cname, lambda: mkchart(cname, defopts()))

	for hsys in range(12):	# index into houses.Houses.hsystems in this version
		def f():
			opts = defopts()
			opts.hsys = hsys
			return mkchart('budapest', opts)
		run('hsys/%d' % hsys, f)
		run('hsys_tromso/%d' % hsys, lambda: (lambda o: (setattr(o, 'hsys', hsys), mkchart('tromso', o))[1])(defopts()))

	for ayan in [1, 2, 3]:
		def f():
			opts = defopts()
			opts.ayanamsha = ayan
			return mkchart('budapest', opts)
		run('ayanamsha/%d' % ayan, f)

	for ayan in [0, 1]:
		def f():
			opts = defopts()
			opts.hsys = 5	# whole sign
			opts.ayanamsha = ayan
			return mkchart('newyork', opts).houses
		run('wholesign_ayanamsha/%d' % ayan, f)

	for cname, t, p in CHARTS:
		for ayan in [0, 1]:
			def f():
				opts = defopts()
				opts.ayanamsha = ayan
				ch = mkchart(cname, opts)
				return [ch.dignity(pid) for pid in range(len(ch.planets.planets))]
			run('dignity/%s/%d' % (cname, ayan), f)

	for bonatti in [True, False]:
		for cname in ['budapest', 'sydney']:
			def f():
				opts = defopts()
				opts.isfirbonatti = bonatti
				return mkchart(cname, opts).firdaria
			run('firdaria/%s/%s' % (cname, bonatti), f)

	def topo():
		opts = defopts()
		opts.topocentric = True
		return mkchart('budapest', opts)
	run('topocentric', topo)

	PD = primdirs.PrimDirs
	PDCLASSES = [(PD.PLACIDIANSEMIARC, placidiansapd.PlacidianSAPD), (PD.PLACIDIANUNDERTHEPOLE, placidianutppd.PlacidianUTPPD), (PD.REGIOMONTAN, regiomontanpd.RegiomontanPD), (PD.CAMPANIAN, campanianpd.CampanianPD)]
	for cname in ['budapest', 'sydney', 'tromso']:
		for meth, cls in PDCLASSES:
			for sub in [PD.MUNDANE, PD.ZODIACAL, PD.BOTH]:
				def f():
					opts = defopts()
					opts.primarydir = meth
					opts.subprimarydir = sub
					ch = mkchart(cname, opts)
					return cls(ch, opts, PD.RANGEALL, PD.BOTHDC, primdirs.AbortPD())
				run('pd/%s/%d/%d' % (cname, meth, sub), f)

	for meth, cls in PDCLASSES:
		def f():
			import tempfile
			opts = defopts()
			opts.primarydir = meth
			opts.subprimarydir = PD.BOTH
			pds = cls(mkchart('newyork', opts), opts, PD.RANGEALL, PD.BOTHDC, primdirs.AbortPD())
			fd, fname = tempfile.mkstemp()
			os.close(fd)
			pds.print2file(fname)
			txt = open(fname).read()
			os.remove(fname)
			return txt.split('\n')
		run('pdtext/%d' % meth, f)

	for key in [PD.NAIBOD, PD.CARDAN, PD.PTOLEMY]:
		for keyd in [PD.TRUESOLAREQUATORIALARC, PD.BIRTHDAYSOLARECLIPTICALARC]:
			def f():
				opts = defopts()
				opts.pdkeys = key
				opts.pdkeyd = keyd
				opts.pdkeydyn = True
				ch = mkchart('budapest', opts)
				pds = placidiansapd.PlacidianSAPD(ch, opts, PD.RANGE50, PD.DIRECT, primdirs.AbortPD())
				return pds
			run('pdkey/%d/%d' % (key, keyd), f)

	for da in [12.5, -33.25]:
		run('pdsinchart/%s' % da, lambda: pdsinchart.PDsInChart(mkchart('budapest', defopts()), da))

	for cname in ['budapest', 'sydney']:
		def f():
			tr = transits.Transits()
			tr.month(2011, 3, mkchart(cname, defopts()))
			return tr
		run('transits/%s' % cname, f)

	for typ in range(4):
		for cname in ['budapest', 'sydney']:
			def f():
				revs = revolutions.Revolutions()
				res = revs.compute(typ, 2011, 6, 1, mkchart(cname, defopts()))
				return (res, revs)
			run('revolutions/%s/%d' % (cname, typ), f)

	def sunt():
		ch = mkchart('budapest', defopts())
		st = suntransits.SunTransits()
		res = st.compute(2011, 1, 1, ch, ch.planets.planets[0].data[0])
		return (res, st)
	run('suntransits', sunt)

	for age in [0, 30, 77]:
		for direct in [True, False]:
			for soltime in [True, False]:
				run('secdir/%d/%s/%s' % (age, direct, soltime), lambda: secdir.SecDir(mkchart('budapest', defopts()), age, direct, soltime).compute())

	for cyc in [0, 5]:
		def f():
			ch = mkchart('budapest', defopts())
			prof = profections.Profections(ch, 2011, 7, 20, 13.5, cyc)
			mprof = munprofections.MunProfections(ch, 2011, 7, 20, 13.5, cyc)
			opts = defopts()
			pchart = chart.Chart(ch.name, ch.male, ch.time, ch.place, chart.Chart.PROFECTION, '', opts, False)
			pchart.calcProfPos(prof)
			return (prof, mprof, pchart)
		run('profections/%d' % cyc, f)

	run('ephem/2011', lambda: ephemcalc.EphemCalc(2011, defopts()))

	f = open(out, 'w')
	json.dump(results, f, sort_keys=True, indent=0)
	f.close()


if __name__ == '__main__':
	main()

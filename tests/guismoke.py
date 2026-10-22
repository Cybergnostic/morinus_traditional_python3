# GUI smoke test: loads a chart and triggers every menu command, answering
# dialogs with OK, painting every window, and recording exceptions and wx
# assertion failures. Run it against a scratch copy of the program, since
# confirmed option dialogs save into Opts/:
#
#   xvfb-run python3 guismoke.py <morinus-copy> <outdir> [--shots] [--trace-div] [--lang N]
#
# --exercise also selects list rows, changes choices and check boxes, types
# into fields and presses the buttons inside every dialog it opens.
# --trace-div rewrites every '/' in the program at import time to record
# which division sites see two ints (Py2 floor division semantics), and
# every str()/'%s' formatting that sees a float (Py2 printed 12 digits).
# guismoke.json also lists controls drawn smaller than their contents need
# ("clipped"), e.g. fixed sizes that fit on Windows but not on GTK.

import os
import sys
import faulthandler
import ast
import json
import time
import traceback
import subprocess
import importlib.abc
import importlib.util

import wx
import wx.adv


class DivTracer(ast.NodeTransformer):
	def __init__(self, fname):
		self.fname = fname

	def call(self, left, right, node):
		site = ast.Constant('%s:%d:%d' % (self.fname, node.lineno, node.col_offset))
		return ast.copy_location(ast.Call(ast.Name('__div_trace__', ast.Load()), [left, right, site], []), node)

	def visit_BinOp(self, node):
		self.generic_visit(node)
		if isinstance(node.op, ast.Div):
			return self.call(node.left, node.right, node)
		if isinstance(node.op, ast.Mod) and isinstance(node.left, ast.Constant) and isinstance(node.left.value, str) and '%s' in node.left.value:
			site = ast.Constant('%s:%d:%d' % (self.fname, node.lineno, node.col_offset))
			return ast.copy_location(ast.Call(ast.Name('__fmt_trace__', ast.Load()), [node.left, node.right, site], []), node)
		return node

	def visit_Call(self, node):
		self.generic_visit(node)
		if isinstance(node.func, ast.Name) and node.func.id == 'str' and len(node.args) == 1 and not node.keywords:
			site = ast.Constant('%s:%d:%d' % (self.fname, node.lineno, node.col_offset))
			return ast.copy_location(ast.Call(ast.Name('__str_trace__', ast.Load()), [node.args[0], site], []), node)
		return node

	def visit_AugAssign(self, node):
		self.generic_visit(node)
		if isinstance(node.op, ast.Div):
			load = ast.parse(ast.unparse(node.target), mode='eval').body
			return ast.copy_location(ast.Assign([node.target], self.call(load, node.value, node)), node)
		return node


DIVSITES = {}
CLIPPED = []
STATE = {}	# the step reached and whether the run finished, for guismoke.json


def div_trace(a, b, site):
	kind = 'int' if isinstance(a, int) and isinstance(b, int) and not isinstance(a, bool) else 'other'
	DIVSITES.setdefault(site, set()).add(kind)
	return a/b


STRSITES = {}


def str_trace(x, site):
	# Python 2 str(float) gave 12 significant digits, Python 3 gives repr()
	if isinstance(x, float):
		STRSITES.setdefault(site, set()).add('str')
	return str(x)


def fmt_trace(fmt, args, site):
	if any(isinstance(a, float) for a in (args if isinstance(args, tuple) else (args,))):
		STRSITES.setdefault(site, set()).add('fmt')
	return fmt % args


class TracingFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
	def __init__(self, mdir):
		self.mdir = mdir

	def find_spec(self, name, path, target=None):
		fn = os.path.join(self.mdir, name+'.py')
		if '.' not in name and os.path.isfile(fn):
			return importlib.util.spec_from_file_location(name, fn, loader=self)
		return None

	def create_module(self, spec):
		return None

	def exec_module(self, module):
		fn = module.__spec__.origin
		tree = DivTracer(os.path.basename(fn)).visit(ast.parse(open(fn, encoding='utf-8').read(), fn))
		ast.fix_missing_locations(tree)
		module.__dict__['__div_trace__'] = div_trace
		module.__dict__['__str_trace__'] = str_trace
		module.__dict__['__fmt_trace__'] = fmt_trace
		exec(compile(tree, fn, 'exec'), module.__dict__)


HANDLERS = ['onLoad', 'comparisonGrid', 'multiWheel', 'chartQuality', 'tablePresentation', 'positionsWorkspace', 'fixedStarsWorkspace', 'hoursRiseSetWorkspace', 'lunationNavigator', 'ephemerisWorkspace', 'legacyShortcuts', 'transitSearch', 'clickWheel', 'onPositions', 'onAlmutenZodiacal', 'onAlmutenChart', 'onAlmutenTopical', 'onMisc', 'onMunPos', 'onAntiscia',
	'onAspects', 'onMidpoints', 'onRiseSet', 'onSpeeds', 'onZodPars', 'onFixedStars', 'onFixedStarsAsps', 'onLots', 'onStrip',
	'onPlanetaryHours', 'onExactTransits', 'onProfections', 'onUserSpeculum', 'onFirdaria', 'onPrimaryDirs', 'onTransits',
	'onRevolutions', 'onSunTransits', 'onSecondaryDirs', 'onElections', 'onReturnsList', 'menu:mcharts', 'menu:mview', 'onChartLook', 'settings', 'onConditions', 'onTemperament', 'onZRFortune', 'onZRSpirit', 'onDecennials', 'onCircumambulation', 'onHeliacal', 'onStarAngles', 'onDodecaCalc', 'onTradOpts:0', 'onTradOpts:1', 'onTradOpts:2', 'onTradOpts:3', 'onTradOpts:4', 'onTradOpts:5', 'onTradOpts:6', 'onTradOpts:7', 'onSquareChart', 'onSyzygyChart', 'onSyzygyChart2',
	'onProfectionsChart', 'onHelioChart', 'onEphemeris', 'onFindTime', 'onSynastry', 'onSaveAsBitmap', 'onSave', 'onHereAndNow',
	'onNew', 'onData', 'onLoad',
	'onAppearance1', 'onAppearance2', 'onDignities', 'onTriplicities', 'onTerms', 'onDecans', 'onChartAlmuten', 'onTopicals',
	'onAyanamsha', 'onColors', 'onOrbs', 'onPrimaryDirsOpt', 'onPrimaryKeys', 'onPDsInChartOpt', 'onLotsOpt', 'onSyzygy',
	'onFixedStarsOpt', 'onProfectionsOpt', 'onFirdariaOpt', 'onDefLocationOpt', 'onMenuSelFirst', 'onMenuSelSecond',
	'onLanguages', 'onAutoSaveOpts', 'onSaveOpts', 'onReload', 'onHelp', 'onAbout', 'onClose', 'onLoad', 'onExit']


# option overrides for --variant N, to reach code behind non-default settings
VARIANTS = {
	1: {'primarydir': 2, 'subprimarydir': 2, 'ayanamsha': 1, 'bw': True, 'hsys': 2, 'showterms': True, 'showdecans': True, 'netbook': True, 'showobject': 1, 'isfirbonatti': False},
	2: {'primarydir': 3, 'subprimarydir': 1, 'topocentric': True, 'hsys': 5, 'showobject': 2, 'zodprof': False, 'enableclick': False},
	3: {'primarydir': 1, 'subprimarydir': 2, 'bw': True, 'ayanamsha': 3, 'netbook': True, 'usezodprojsprof': True, 'showterms': True},
}


def menu_items(menu):
	for item in menu.GetMenuItems():
		if item.IsSubMenu():
			for sub in menu_items(item.GetSubMenu()):
				yield sub
		elif not item.IsSeparator():
			yield item


def popup_menus(win):
	# (handler window, menu) pairs for menus stored on a window or its children
	res = []
	for w in [win]+list(win.GetChildren()):
		for v in list(vars(w).values()):
			if isinstance(v, wx.Menu):
				res.append((w, v))
	return res


def main():
	mdir = os.path.abspath(sys.argv[1])
	out = os.path.abspath(sys.argv[2])
	shots = '--shots' in sys.argv
	if not os.path.isdir(out):
		os.makedirs(out)
	# a crash of wx itself ends Python without a traceback: this writes where it was
	crashlog = open(os.path.join(out, 'crash.txt'), 'w')
	faulthandler.enable(crashlog)

	sys.path.insert(0, mdir)
	os.chdir(mdir)
	if '--trace-div' in sys.argv:
		sys.meta_path.insert(0, TracingFinder(mdir))

	import options
	import mtexts
	import i18n
	import morin

	errors = []

	def record(where, exc_info=None):
		tb = ''.join(traceback.format_exception(*(exc_info or sys.exc_info())))
		errors.append({'step': state['step'], 'where': where, 'traceback': tb})
		sys.stderr.write('!! %s / %s\n%s\n' % (state['step'], where, tb))

	sys.excepthook = lambda *ei: record('event', ei)

	horpath = os.path.join(mdir, 'Hors', 'Morinus.hor')

	SKIP_BUTTONS = (wx.ID_OK, wx.ID_CANCEL, wx.ID_CLOSE, wx.ID_HELP, wx.ID_CONTEXT_HELP, wx.ID_YES, wx.ID_NO)

	def all_children(win):
		for c in win.GetChildren():
			yield c
			for cc in all_children(c):
				yield cc

	clipped = CLIPPED

	def check_clipping(win):
		# controls smaller than their contents need on this platform (fixed sizes
		# chosen for Windows); number fields are measured with their largest value
		for c in all_children(win):
			try:
				if not c.IsShownOnScreen():	# also not inside a hidden panel
					continue
				if isinstance(c, wx.TextCtrl) and not c.IsMultiLine():
					sample = c.GetValue()
					maxim = getattr(c.GetValidator(), 'maxim', None)
					if maxim is not None and len(str(maxim)) > len(sample):
						sample = str(maxim)
					if not sample:
						continue
					need = c.GetSizeFromTextSize(c.GetTextExtent(sample))
				elif isinstance(c, wx.Button):
					# GTK's best size has a minimum width; what matters is the label
					tw, th = c.GetTextExtent(c.GetLabel())
					need = wx.Size(tw + 8, th)
				elif isinstance(c, (wx.SpinCtrl, wx.Choice, wx.ComboBox, wx.CheckBox, wx.RadioButton, wx.StaticText, wx.Slider)):
					if c.GetSize().height == 0:
						continue	# on a page that is not shown
					need = c.GetBestSize()
				else:
					continue
				size = c.GetSize()
				if size.width + 1 < need.width or size.height + 1 < need.height:
					item = {'window': type(win).__name__, 'control': type(c).__name__,
						'text': c.GetValue() if isinstance(c, wx.TextCtrl) else c.GetLabel(),
						'size': list(size), 'needs': list(need)}
					if item not in clipped:
						clipped.append(item)
			except Exception:
				pass

	def fire(ctrl, evtype):
		evt = wx.CommandEvent(evtype, ctrl.GetId())
		evt.SetEventObject(ctrl)
		ctrl.GetEventHandler().ProcessEvent(evt)

	def exercise(dlg):
		# what a user does inside a dialog: select list rows, change choices and
		# check boxes, type into fields, press the dialog's own buttons
		name = type(dlg).__name__
		for c in list(all_children(dlg)):
			try:
				if c.IsBeingDeleted():
					continue
				if isinstance(c, wx.ListCtrl):
					for i in range(min(c.GetItemCount(), 3)):
						c.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
						wx.SafeYield()
				elif isinstance(c, (wx.Choice, wx.ComboBox)) and c.GetCount() > 1:
					c.SetSelection(1)
					fire(c, wx.wxEVT_CHOICE if isinstance(c, wx.Choice) else wx.wxEVT_COMBOBOX)
				elif isinstance(c, wx.CheckBox):
					c.SetValue(not c.GetValue())
					fire(c, wx.wxEVT_CHECKBOX)
				elif isinstance(c, wx.RadioButton):
					c.SetValue(True)
					fire(c, wx.wxEVT_RADIOBUTTON)
				elif isinstance(c, wx.TextCtrl) and c.IsEditable():
					evt = wx.KeyEvent(wx.wxEVT_CHAR)
					evt.SetKeyCode(ord('5'))
					evt.SetEventObject(c)
					c.GetEventHandler().ProcessEvent(evt)
			except Exception:
				record('exercise %s %s' % (name, type(c).__name__))
		for c in list(all_children(dlg)):
			try:
				if isinstance(c, wx.Button) and c.GetId() not in SKIP_BUTTONS and not c.IsBeingDeleted() and c.IsEnabled():
					state['button'] = c.GetLabel()
					fire(c, wx.wxEVT_BUTTON)
					wx.SafeYield()
			except Exception:
				record('button %s "%s"' % (name, state.get('button')))

	def show_briefly(dlg):
		try:
			dlg.Fit()
			dlg.Show()
			for i in range(5):
				wx.SafeYield()
			check_clipping(dlg)
			shot('dlg-'+type(dlg).__name__)
			if '--exercise' in sys.argv and state.get('depth', 0) == 0:
				state['depth'] = 1
				try:
					exercise(dlg)
				finally:
					state['depth'] = 0
			dlg.Hide()
		except Exception:
			record('dialog '+type(dlg).__name__)

	def dialog_modal(self):
		show_briefly(self)
		return wx.ID_OK

	def message_modal(self):
		return wx.ID_YES if self.GetMessageDialogStyle() & wx.YES_NO else wx.ID_OK

	def file_modal(self):
		if self.GetWindowStyle() & wx.FD_SAVE:
			name = self.GetFilename() or 'saved'
			state['filepath'] = os.path.join(out, 'saved-'+os.path.basename(name))
		else:
			state['filepath'] = horpath
		return wx.ID_OK

	try:
		import gtkfit	# as morinus.py does at start
		gtkfit.install()
	except ImportError:
		pass
	wx.Dialog.ShowModal = dialog_modal
	wx.MessageDialog.ShowModal = message_modal
	# on Windows the About box is native and modal, out of reach of the patches
	wx.adv.AboutBox = lambda info, parent=None: None
	# wx.MessageBox opens a native dialog that the patches above do not reach
	wx.MessageBox = lambda message, caption='', style=wx.OK, parent=None, *a: wx.YES if style & wx.YES_NO else wx.OK
	wx.FileDialog.ShowModal = file_modal
	wx.FileDialog.GetPath = lambda self: state['filepath']
	wx.FileDialog.GetDirectory = lambda self: os.path.dirname(state['filepath'])
	# native pickers would block the run; answer them like a user who cancels
	for cls in (wx.ColourDialog, wx.FontDialog, wx.DirDialog, wx.TextEntryDialog, wx.SingleChoiceDialog, wx.MultiChoiceDialog, wx.PrintDialog):
		cls.ShowModal = lambda self: wx.ID_CANCEL
	# the native GTK about box is not a wx window and cannot be closed from here
	# (on Windows the generic one is modal too and would hang the run: keep the stub above)
	if wx.Platform != '__WXMSW__':
		wx.adv.AboutBox = lambda info, parent=None: wx.adv.GenericAboutBox(info, parent)

	state = STATE
	state.update({'step': 'startup', 'filepath': horpath})

	def capture_window(window, filename):
		"""Save a native screenshot when the platform supports ScreenDC."""
		try:
			wx.SafeYield()
			r = window.GetScreenRect()
			bmp = wx.Bitmap(r.width, r.height)
			mem = wx.MemoryDC(bmp)
			mem.Blit(0, 0, r.width, r.height, wx.ScreenDC(), r.x, r.y)
			mem.SelectObject(wx.NullBitmap)
			bmp.SaveFile(os.path.join(out, filename), wx.BITMAP_TYPE_PNG)
		except Exception:
			# Rendered wheel PNGs are always kept independently.
			pass

	def shot(name):
		if shots:
			fn = os.path.join(out, '%02d-%s-%s.png' % (state['n'], state['step'], name))
			subprocess.call(['import', '-window', 'root', fn])

	app = wx.App(False)
	wx.Log.SetLogLevel(wx.LOG_Info)	# as morinus.py: no wxWidgets debug diagnostics
	opts = options.Options()
	if '--variant' in sys.argv:
		for k, v in VARIANTS[int(sys.argv[sys.argv.index('--variant')+1])].items():
			assert hasattr(opts, k), k
			setattr(opts, k, v)
	if '--lang' in sys.argv:	# e.g. 3: Serbian
		opts.langid = int(sys.argv[sys.argv.index('--lang')+1])
	mtexts.setLang(opts.langid)
	frame = morin.MFrame(None, -1, mtexts.txtscommon['ProgramTitle'], opts)
	frame.Show(True)

	steps = iter(['onLoad', 'comparisonGrid', 'multiWheel', 'onExit'] if '--multiwheel-only' in sys.argv else HANDLERS)
	state['n'] = 0

	def settle(secs):
		end = time.time()+secs
		while time.time() < end:
			wx.SafeYield()
			time.sleep(0.02)

	def next_step():
		for w in wx.GetTopLevelWindows():
			if w is not frame and not w.IsBeingDeleted():
				try:
					# MFrame keeps some dialogs for reuse, so only hide those
					if isinstance(w, wx.Dialog):
						w.Hide()
					else:
						w.Destroy()
				except Exception:
					record('destroy')
		settle(0.2)
		write_results(out, errors, quiet=True)	# keep findings if a later step hangs
		try:
			name = next(steps)
		except StopIteration:
			return
		state['step'] = name
		state['n'] += 1
		sys.stderr.write('== %s\n' % name)
		try:
			if name == 'comparisonGrid':
				# Four independent single-wheel canvases, including an open transit.
				import chart, transitframe, comparegrid
				secondary = chart.Chart(frame.horoscope.name, frame.horoscope.male,
					frame.horoscope.time, frame.horoscope.place, chart.Chart.TRANSIT,
					'', frame.options, False)
				tw = transitframe.TransitFrame(frame, 'Smoke transit', secondary,
					frame.horoscope, frame.options)
				tw.Show(True)
				wnd = comparegrid.show(frame)
				settle(0.3)
				wnd.cells[1].picker.refresh()
				assert len(wnd.cells[1].picker.sources) > 1
				wnd.cells[1].picker.choice.SetSelection(1)
				wnd.cells[1].picker.changed(None)
				wnd.layout_choice.SetSelection(1)
				wnd.change_layout()
				settle(0.3)
				for cell in wnd.cells:
					cell.redraw()
					assert cell.buffer is not None and cell.buffer.IsOk()
				assert wnd.cells[1].picker.selected() is secondary
				capture_window(wnd, 'comparison-grid.png')
				wnd.SetSize((1200, 740))
				settle(0.2)
				wnd.refresh_wheels()
				wnd.Close()
				tw.Close()
			elif name == 'multiWheel':
				# Three ring counts, hit testing, resize, and PNG export.
				import multiwheel, chart
				secondary = chart.Chart(frame.horoscope.name, frame.horoscope.male,
					frame.horoscope.time, frame.horoscope.place, chart.Chart.TRANSIT,
					'', frame.options, False)
				wnd = multiwheel.show(frame)
				settle(0.3)
				picker = wnd.pickers[0]
				picker.loaded.append(('Smoke transit', secondary))
				picker.refresh()
				picker.choice.SetSelection(len(picker.sources) - 1)
				for count in (1, 2, 3):
					wnd.count_choice.SetSelection(count - 1)
					wnd.change_count()
					# Default is no aspects; keep it in the saved reference images.
					wnd.aspect_choice.SetSelection(0)
					settle(0.3)
					wnd.redraw()
					assert wnd.renderer.aspect_ring == -1
					assert wnd.buffer is not None and wnd.buffer.IsOk()
					# Radix-only and radix-to-outer-ring remain available.
					wnd.aspect_choice.SetSelection(1)
					wnd.redraw()
					assert wnd.renderer.aspect_ring == 0
					wnd.aspect_choice.SetSelection(2)
					wnd.redraw()
					assert wnd.renderer.aspect_ring == 1
					wnd.aspect_choice.SetSelection(0)
					wnd.redraw()
					assert len(wnd.renderer.others) == count
					assert wnd.renderer.hits, 'No glyph hitboxes'
					assert wnd.renderer.onClick(wnd.renderer.hits[0][0])
					path = os.path.join(out, 'multiwheel-%d-rings.png' % count)
					assert wnd.buffer.SaveFile(path, wx.BITMAP_TYPE_PNG)
					assert os.path.getsize(path) > 0
				# Check the shared Morinus reference bands even when the normal
				# test options have both traditional strips switched off.
				original_terms = frame.options.showterms
				original_decans = frame.options.showdecans
				try:
					frame.options.showterms = True
					frame.options.showdecans = True
					wnd.redraw()
					assert wnd.buffer is not None and wnd.buffer.IsOk()
					path = os.path.join(out, 'multiwheel-shared-traditional-bands.png')
					assert wnd.buffer.SaveFile(path, wx.BITMAP_TYPE_PNG)
				finally:
					frame.options.showterms = original_terms
					frame.options.showdecans = original_decans
				wnd.redraw()
				# Changing house systems must keep the multiwheel open, and
				# refresh all the retained charts rather than destroying it.
				previous_hsys = frame.options.hsys
				next_hsys = 5 if previous_hsys != 5 else 2
				frame.onHouseSystem(wx.CommandEvent(wx.wxEVT_MENU,
					frame.hsbase + next_hsys))
				settle(0.2)
				assert not wnd.IsBeingDeleted() and wnd.IsShown()
				wnd.redraw()
				assert wnd.buffer is not None and wnd.buffer.IsOk()
				assert wnd.renderer.radix is frame.horoscope
				frame.onHouseSystem(wx.CommandEvent(wx.wxEVT_MENU,
					frame.hsbase + previous_hsys))
				settle(0.2)
				assert not wnd.IsBeingDeleted()
				wnd.redraw()
				# The multiwheel's chart-creation menu reuses the existing
				# Morinus return/transit workflows, then picks the result.
				import transitframe
				original_revolutions = frame.onRevolutions
				original_transits = frame.onTransits
				generated_windows = []
				def fake_generate(kind):
					created = chart.Chart(frame.horoscope.name, frame.horoscope.male,
						frame.horoscope.time, frame.horoscope.place, kind, '',
						frame.options, False)
					new_window = transitframe.TransitFrame(
						frame, 'Smoke generated', created, frame.horoscope, frame.options)
					new_window.Show(True)
					generated_windows.append(new_window)
				try:
					frame.onRevolutions = lambda event, planet=None: fake_generate(
						chart.Chart.SOLAR if planet == 3 else chart.Chart.LUNAR)
					frame.onTransits = lambda event: fake_generate(chart.Chart.TRANSIT)
					for requested, htype in ((3, chart.Chart.SOLAR),
							(6, chart.Chart.LUNAR), (None, chart.Chart.TRANSIT)):
						picker.create_chart(requested)
						assert picker.selected().htype == htype
						assert picker.choice.GetStringSelection() != ''
				finally:
					frame.onRevolutions = original_revolutions
					frame.onTransits = original_transits
					for gen_window in generated_windows:
						gen_window.Close()
				# Restore our reference image to the original smoke transit.
				picker.refresh()
				picker.choice.SetSelection(next(i for i, (_, selected) in
					enumerate(picker.sources) if selected is secondary))
				wnd.redraw()
				capture_window(wnd, 'multiwheel-window.png')
				wnd.SetSize((1050, 790))
				settle(0.2)
				wnd.redraw()
				wnd.onSaveAsBitmap(None)
				wnd.Close()
			elif name == 'chartQuality':
				# Check both render modes on the same wheel. Scaling must never
				# enlarge the on-screen bitmap or change click coordinates.
				import graphchart, tradoptions, planets, houses, math
				old_quality = tradoptions.get('chart_quality')
				try:
					for quality, factor in (('standard', 1), ('high', 2)):
						tradoptions.set({'chart_quality': quality})
						g = graphchart.GraphChart(frame.horoscope, (640, 480),
							frame.options, frame.options.bw)
						bmp = g.drawChart()
						assert g.render_scale == factor, (quality, g.render_scale)
						assert (bmp.GetWidth(), bmp.GetHeight()) == (640, 480)
						i = planets.Planets.SUN
						lon = g.chart.planets.planets[i].data[planets.Planet.LON]
						asc = g.chart.houses.ascmc[houses.Houses.ASC]
						angle = math.pi + math.radians(asc - lon - g.pshift[i])
						x = (g.center.x + math.cos(angle) * g.rPlanet) / factor
						y = (g.center.y + math.sin(angle) * g.rPlanet) / factor
						assert g.onClick((x, y)) == i, 'Planet hit test: ' + quality
				finally:
					tradoptions.set({'chart_quality': old_quality})
			elif name == 'tablePresentation':
				# A5: verify that display zoom does not touch the export source;
				# typed Miscellaneous CSV rows must remain two-column data.
				import miscframe, miscwnd, tablepresentation
				fr = miscframe.MiscFrame(frame, frame.title, frame.horoscope, frame.options)
				try:
					table = next(c for c in fr.GetChildren() if isinstance(c, miscwnd.MiscWnd))
					rows = table.tableRows()
					assert len(rows) == 3 and all(len(row) == 2 for row in rows), rows
					before = (table.buffer.GetWidth(), table.buffer.GetHeight())
					table.setZoom(1.5, keep=False)
					image = table.scaled()
					assert (image.GetWidth(), image.GetHeight()) == tablepresentation.pixel_size(*before, table.zoom)
					assert (table.buffer.GetWidth(), table.buffer.GetHeight()) == before
					table.setZoom(1.0, keep=False)
					assert table.zoom == 1.0
				finally:
					fr.Destroy()
			elif name == 'positionsWorkspace':
				# B1: exercise all four embedded, original Morinus tables.
				# The speculum selector must not alter primary-directions settings.
				import positionsworkspace, positionscatalog
				pdir = frame.options.primarydir
				wnd = positionsworkspace.show(frame, 1)
				assert wnd.book.GetPageCount() == len(positionscatalog.TABS)
				for method in (0, 1):
					wnd.activeView().setMethod(method)
					if positionsworkspace.has_columns(frame.options, method):
						assert wnd.activeView().view.speculum == method
						assert wnd.activeView().view.tableRows(), 'speculum CSV rows'
				assert frame.options.primarydir == pdir
				# Configure columns must keep the workspace open (its own window)
				wnd.activeView().onConfigure(None)
				assert wnd and not wnd.IsBeingDeleted(), 'Configure columns closed the workspace'
				# the overview: a row per planet and node, house positions as '12th, 22.0%'
				wnd.selectTab(0)
				rows = wnd.activeView().tableRows()
				assert any('%' in cell for row in rows for cell in row), rows[:3]
				assert wnd.activeView().chart is frame.horoscope
				wnd.Close()
			elif name == 'legacyShortcuts':
				# F1, F5, F6, F10, F11, Ctrl+F1, Ctrl+F2, Ctrl+F5, Ctrl+Shift+F7/F8 of
				# Morinus 6: the accelerator ids still open their tables and charts
				expect = ((frame.ID_Positions, 'positions_workspace'), (frame.ID_Misc, 'positions_workspace'),
					(frame.ID_MunPos, 'positions_workspace'), (frame.ID_Speeds, 'positions_workspace'),
					(frame.ID_RiseSet, 'hours_riseset_workspace'), (frame.ID_PlanetaryHours, 'hours_riseset_workspace'),
					(frame.ID_FixedStars, 'fixed_stars_workspace'), (frame.ID_FixedStarsAsps, 'fixed_stars_workspace'),
					(frame.ID_SyzygyChart, None), (frame.ID_SyzygyChart2, None),
					(frame.ID_ExactTransits, 'transit_search'), (frame.ID_SunTransits, 'transit_search'),
					(frame.ID_UserSpeculum, 'positions_workspace'))
				for iid, attr in expect:
					before = set(wx.GetTopLevelWindows())
					frame.GetEventHandler().ProcessEvent(wx.CommandEvent(wx.wxEVT_MENU, iid))
					settle(0.2)
					if attr is not None:
						assert getattr(frame, attr, None), 'shortcut %d did not open %s' % (iid, attr)
					else:
						assert set(wx.GetTopLevelWindows()) - before, 'shortcut %d opened no chart' % iid
			elif name == 'transitSearch':
				# a month of transits of the sample chart, its chart and its CSV
				import transitsearch
				wnd = transitsearch.show(frame)
				wnd.fromyear.SetValue(frame.horoscope.time.origyear)
				wnd.toyear.SetValue(frame.horoscope.time.origyear)
				wnd.tomonth.SetSelection(wnd.frommonth.GetSelection())
				wnd.onSearch(None)
				assert wnd.results, 'no transits in a month'
				wnd.list.Select(0)
				wnd.onOpen(None)
				wnd.onCSV(None)
				wnd.Close()
			elif name == 'fixedStarsWorkspace':
				# Exercise lazy tabs without calculating all angular crossings twice.
				import fixedstarsworkspace, fixedstarscatalog
				if frame.options.fixedstars:
					wnd = fixedstarsworkspace.show(frame, 0)
					if wnd is not None:
						assert wnd.book.GetPageCount() == len(fixedstarscatalog.TABS)
						assert wnd.activeView().chart is frame.horoscope
						wnd.selectTab(1)
						assert wnd.activeView().chart is frame.horoscope
						wnd.selectTab(0)
						assert len(wnd.views) == 2, 'Lazy third tab was constructed early'
						wnd.Close()
			elif name == 'hoursRiseSetWorkspace':
				import hoursrisesetworkspace
				wnd = hoursrisesetworkspace.show(frame, 0)
				assert wnd.book.GetPageCount() == 2
				assert len(wnd.views) == 1
				assert wnd.activeView().chart is frame.horoscope
				wnd.selectTab(1)
				assert wnd.activeView().chart is frame.horoscope
				assert len(wnd.views) == 2
				wnd.selectTab(0)
				wnd.Close()
			elif name == 'lunationNavigator':
				import lunationnavigator, lunationnav
				if not frame.horoscope.time.bc:
					syz = frame.horoscope.syzygy
					wnd = lunationnavigator.show(frame)
					assert wnd and len(wnd.events) >= 5
					assert frame.horoscope.syzygy is syz
					assert any(e[0] < frame.horoscope.time.jd for e in wnd.events)
					assert any(e[0] > frame.horoscope.time.jd for e in wnd.events)
					for jd, name, sun, moon in wnd.events:
						target = 0.0 if name == 'New Moon' else 180.0
						assert abs(lunationnav.phase_difference(moon, sun, target)) < 0.0005
					wnd.shift(55)
					assert frame.horoscope.syzygy is syz
					wnd.Close()
			elif name == 'ephemerisWorkspace':
				# B5: the table, graph and events must share one 366-day leap
				# series; test real Swiss ingresses/stations and CSV column counts.
				import ephemerisworkspace, ephemerisdata
				wnd = ephemerisworkspace.show(frame, 2024)
				settle(0.3)
				assert wnd.data.year == 2024
				assert len(wnd.data.dates) == 366
				assert len(wnd.data.longitudes) == 7
				assert len(wnd.data.longitudes[0]) == 366
				assert len(wnd.dailyRows()) == 367
				assert len(wnd.dailyRows()[0]) == 15
				assert wnd.data.events, 'No Swiss stations or ingresses in 2024'
				wnd.month.SetSelection(2)
				wnd.fillDays()
				assert wnd.days.GetItemCount() == 29, 'Leap-year February must have 29 days'
				wnd.month.SetSelection(0)
				wnd.fillDays()
				wnd.book.SetSelection(0)
				settle(0.2)
				wnd.mountGraph()
				assert wnd.graph is not None, 'Graph must be sized/visible after Show'
				assert len(wnd.graph.posArr[0]) == 366
				wnd.selectDay(59)
				assert wnd.selected_day == 59 and wnd.graph.focus_day == 59
				wnd.graph.setShowMoon(True)
				assert wnd.graph.numberOfPlanets() == 7
				for ev in wnd.data.events[:6]:
					if ev.kind == 'Station':
						assert abs(ephemerisdata.swiss_sampler(frame.options)(
							ev.jd, ev.planet)[1]) < 0.001
				wnd.Close()
			elif name == 'clickWheel':
				w, h = frame.GetClientSize()
				for fx in range(1, 10):
					for fy in range(1, 10):
						evt = wx.MouseEvent(wx.wxEVT_LEFT_UP)
						evt.SetPosition(wx.Point(w*fx//10, h*fy//10))
						frame.GetEventHandler().ProcessEvent(evt)
			elif name == 'settings':
				# the Settings window is not modal: visit its categories, search, then use every control
				import settingswnd
				wnd = settingswnd.show(frame)
				settle(0.3)
				for i in range(wnd.list.GetCount()):
					wnd.list.SetSelection(i)
					fire(wnd.list, wx.wxEVT_LISTBOX)
					settle(0.1)
					check_clipping(wnd)
				wnd.search.SetValue('orbs')
				settle(0.1)
				for query, title, category in (
				        ('Egyptian terms', 'Terms', 'Dignities'),
				        ('Regiomontanus', 'House system', 'Calculation'),
				        ('Zodiacal releasing years shown', 'Years shown', 'Time lords')):
				    wnd.search.SetValue(query)
				    settle(0.1)
				    match = next((r for r in wnd.shown if r['title'] == i18n.tr(title) and r['category'] == i18n.tr(category)), None)
				    assert match is not None, 'Settings search failed: %s' % query
				    wnd.showEntry(match)
				    assert wnd.book.GetSelection() == match['category_index']
				wnd.search.SetValue('')
				exercise(wnd)
				if wnd:
					wnd.Close()
			elif name.startswith('menu:'):
				# every item of a menu of the menu bar (check items twice, to end as they were)
				for item in list(menu_items(getattr(frame, name[5:]))):
					for _ in range(2 if item.GetKind() == wx.ITEM_CHECK else 1):
						state['step'] = '%s/%s' % (name, item.GetItemLabelText())
						if item.GetKind() == wx.ITEM_CHECK:
							item.Check(not item.IsChecked())
						elif item.GetKind() == wx.ITEM_RADIO:
							item.Check(True)
						evt = wx.CommandEvent(wx.wxEVT_MENU, item.GetId())
						evt.SetInt(int(item.IsChecked()) if item.IsCheckable() else 0)
						try:
							frame.GetEventHandler().ProcessEvent(evt)
							settle(0.3)
						except Exception:
							record('menu')
				state['step'] = name
			elif ':' in name:
				# handlers taking an index, e.g. onTradOpts:0 (the options dialogs of tradoptsdlg)
				method, arg = name.split(':')
				getattr(frame, method)(int(arg))
			else:
				getattr(frame, name)(wx.CommandEvent())
		except Exception:
			record('handler')
		# primary directions run in a thread and post EVT_PDREADY
		end = time.time()+120
		while hasattr(frame, 'progbar') and time.time() < end:
			settle(0.2)
		settle(0.5)
		for w in wx.GetTopLevelWindows():
			try:
				if w.IsShown():
					w.Refresh()
					wx.Window.Update(w)
			except Exception:
				record('paint')
		settle(0.3)
		for w in wx.GetTopLevelWindows():
			if w.IsShown():
				check_clipping(w)
		shot('wnd')
		popups(name)
		if name == 'onExit':
			state['finished'] = True
			write_results(out, errors, quiet=True)
			wx.CallLater(2000, app.ExitMainLoop)
			return
		wx.CallLater(50, next_step)

	def fake_click(owner):
		# popup commands of list windows act on the row that was right-clicked
		if getattr(owner, 'curposx', 0) is None:
			border = getattr(type(owner), 'BORDER', 10)
			owner.curposx = border+5
			owner.curposy = border+getattr(owner, 'TITLE_CELL_HEIGHT', 20)+getattr(owner, 'SPACE_TITLEY', 0)+getattr(owner, 'LINE_HEIGHT', 20)//2

	def popups(name):
		# fire every popup menu item of the windows this step opened; menus are
		# looked up again for each item, as some items rebuild the window
		opened = [w for w in wx.GetTopLevelWindows() if w is not frame and isinstance(w, wx.Frame) and w.IsShown()]
		for top in opened:
			i = 0
			while True:
				try:
					items = [(owner, item) for owner, menu in popup_menus(top) for item in menu_items(menu)]
					# the copies of the popup menus in the window's menu bar (menubars.py)
					bar = top.GetMenuBar()
					if bar is not None:
						items += [(top, item) for m in range(bar.GetMenuCount()) for item in menu_items(bar.GetMenu(m))]
				except RuntimeError:
					break
				if i >= len(items):
					break
				owner, item = items[i]
				i += 1
				before = set(wx.GetTopLevelWindows())
				state['step'] = '%s/popup:%s' % (name, item.GetItemLabelText())
				try:
					fake_click(owner)
					evt = wx.CommandEvent(wx.wxEVT_MENU, item.GetId())
					evt.SetEventObject(owner)
					owner.GetEventHandler().ProcessEvent(evt)
					settle(0.3)
					for w in wx.GetTopLevelWindows():
						if w not in before and w.IsShown():
							w.Refresh()
							wx.Window.Update(w)
					settle(0.2)
				except Exception:
					record('popup')
				for w in wx.GetTopLevelWindows():
					if w not in before and not w.IsBeingDeleted():
						if isinstance(w, wx.Dialog):
							w.Hide()
						else:
							w.Destroy()
				settle(0.1)
		state['step'] = name

	wx.CallLater(500, next_step)
	try:
		app.MainLoop()
	finally:
		write_results(out, errors)


def write_results(out, errors, quiet=False):
	res = {'errors': errors, 'clipped': CLIPPED, 'laststep': STATE.get('step'), 'finished': STATE.get('finished', False)}
	if DIVSITES:
		res['divsites'] = dict((k, sorted(v)) for k, v in DIVSITES.items())
	if STRSITES:
		res['floatstrsites'] = dict((k, sorted(v)) for k, v in STRSITES.items())
	with open(os.path.join(out, 'guismoke.json'), 'w') as f:
		json.dump(res, f, indent=1)
	if not quiet:
		sys.stderr.write('%d errors\n' % len(errors))


if __name__ == '__main__':
	main()

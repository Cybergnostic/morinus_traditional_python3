# GUI smoke test: loads a chart and triggers every menu command, answering
# dialogs with OK, painting every window, and recording exceptions and wx
# assertion failures. Run it against a scratch copy of the program, since
# confirmed option dialogs save into Opts/:
#
#   xvfb-run python3 guismoke.py <morinus-copy> <outdir> [--shots] [--trace-div]
#
# --trace-div rewrites every '/' in the program at import time to record
# which division sites see two ints (Py2 floor division semantics), and
# every str()/'%s' formatting that sees a float (Py2 printed 12 digits).

import os
import sys
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


HANDLERS = ['onLoad', 'onPositions', 'onAlmutenZodiacal', 'onAlmutenChart', 'onAlmutenTopical', 'onMisc', 'onMunPos', 'onAntiscia',
	'onAspects', 'onMidpoints', 'onRiseSet', 'onSpeeds', 'onZodPars', 'onFixedStars', 'onFixedStarsAsps', 'onLots', 'onStrip',
	'onPlanetaryHours', 'onExactTransits', 'onProfections', 'onUserSpeculum', 'onFirdaria', 'onPrimaryDirs', 'onTransits',
	'onRevolutions', 'onSunTransits', 'onSecondaryDirs', 'onElections', 'onSquareChart', 'onSyzygyChart', 'onSyzygyChart2',
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

	sys.path.insert(0, mdir)
	os.chdir(mdir)
	if '--trace-div' in sys.argv:
		sys.meta_path.insert(0, TracingFinder(mdir))

	import options
	import mtexts
	import morin

	errors = []

	def record(where, exc_info=None):
		tb = ''.join(traceback.format_exception(*(exc_info or sys.exc_info())))
		errors.append({'step': state['step'], 'where': where, 'traceback': tb})
		sys.stderr.write('!! %s / %s\n%s\n' % (state['step'], where, tb))

	sys.excepthook = lambda *ei: record('event', ei)

	horpath = os.path.join(mdir, 'Hors', 'Morinus.hor')

	def show_briefly(dlg):
		try:
			dlg.Fit()
			dlg.Show()
			for i in range(5):
				wx.SafeYield()
			shot('dlg-'+type(dlg).__name__)
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

	wx.Dialog.ShowModal = dialog_modal
	wx.MessageDialog.ShowModal = message_modal
	wx.FileDialog.ShowModal = file_modal
	wx.FileDialog.GetPath = lambda self: state['filepath']
	wx.FileDialog.GetDirectory = lambda self: os.path.dirname(state['filepath'])
	# the native GTK about box is not a wx window and cannot be closed from here
	wx.adv.AboutBox = lambda info, parent=None: wx.adv.GenericAboutBox(info, parent)

	state = {'step': 'startup', 'filepath': horpath}

	def shot(name):
		if shots:
			fn = os.path.join(out, '%02d-%s-%s.png' % (state['n'], state['step'], name))
			subprocess.call(['import', '-window', 'root', fn])

	app = wx.App(False)
	opts = options.Options()
	if '--variant' in sys.argv:
		for k, v in VARIANTS[int(sys.argv[sys.argv.index('--variant')+1])].items():
			assert hasattr(opts, k), k
			setattr(opts, k, v)
	mtexts.setLang(opts.langid)
	frame = morin.MFrame(None, -1, mtexts.txtscommon['ProgramTitle'], opts)
	frame.Show(True)

	steps = iter(HANDLERS)
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
		try:
			name = next(steps)
		except StopIteration:
			return
		state['step'] = name
		state['n'] += 1
		sys.stderr.write('== %s\n' % name)
		try:
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
		shot('wnd')
		popups(name)
		if name == 'onExit':
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


def write_results(out, errors):
	res = {'errors': errors}
	if DIVSITES:
		res['divsites'] = dict((k, sorted(v)) for k, v in DIVSITES.items())
	if STRSITES:
		res['floatstrsites'] = dict((k, sorted(v)) for k, v in STRSITES.items())
	with open(os.path.join(out, 'guismoke.json'), 'w') as f:
		json.dump(res, f, indent=1)
	sys.stderr.write('%d errors\n' % len(errors))


if __name__ == '__main__':
	main()

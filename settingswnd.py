"""The Settings window: every setting by category, with a search. The options of
the added techniques and the simple choices are shown here and take effect at
once; the dialogs of Morinus 6 open from their entries ("Edit...")."""

import copy
import wx
import mtexts
import tradoptions
import tradoptsdlg


def menutext(key):
	"""A menu text without its mnemonic, and its shortcut."""
	text, _, keys = mtexts.menutxts[key].partition('\t')
	return text.replace('&', ''), keys


# entries: ('dialog', title or menu text key, handler of MFrame, description[, title]),
# ('trad', index in tradoptsdlg.DIALOGS), ('houses',) the house system and the nodes,
# ('general',) saving the settings
CATEGORIES = [
	('General', [
		('general',),
		('dialog', 'OMLanguages', 'onLanguages', 'The language of the menus, dialogs and tables.'),
		('dialog', 'OMMenuSelFirst', 'onMenuSelFirst', 'Which items of the File, Tables and Charts menus are shown.', 'Menu selection: File, Tables, Charts'),
		('dialog', 'OMMenuSelSecond', 'onMenuSelSecond', 'Which items of the Settings and Help menus are shown.', 'Menu selection: Settings, Help'),
		('trad', 7),
	]),
	('Appearance', [
		('dialog', 'Chart look', 'onChartLook', 'The colour theme (Ink, Instrument or Classic), the weight of the lines and smooth drawing, with a preview.'),
		('dialog', 'OMAppearance1', 'onAppearance1', 'What the chart shows: house cusps, terms, decans, chart data, the outer ring (fixed stars, antiscia, lots or dodecatemoria); '
			'black and white, topocentric positions, clicking planets, the width of the Asc-MC lines and the size of the tables.'),
		('dialog', 'OMColors', 'onColors', 'The colour of each part of the chart: frame, signs, houses, Asc-MC, each planet and aspect, the Lot of Fortune, the background and the tables.'),
		('dialog', 'OMAppearance2', 'onAppearance2', 'The columns of the speculum tables: Placidian, Regiomontanian and Campanian mundane positions.'),
	]),
	('Calculation', [
		('houses',),
		('dialog', 'OMAyanamsha', 'onAyanamsha', 'The tropical zodiac, or a sidereal one with its ayanamsa.'),
		('dialog', 'OMOrbs', 'onOrbs', 'The orbs of each planet for the aspects and parallels, and those of planets in houses, the angles, intermediate cusps, day and night and the fixed stars.'),
		('trad', 5),
	]),
	('Dignities', [
		('dialog', 'OMDignities', 'onDignities', 'The domiciles and exaltations of the planets.'),
		('dialog', 'OMTriplicities', 'onTriplicities', 'The triplicity rulers: Dorothean, Ptolemaic or Morinus.'),
		('dialog', 'OMTerms', 'onTerms', 'The terms (bounds): Egyptian, Ptolemaic, or edited.'),
		('dialog', 'OMDecans', 'onDecans', 'The decans (faces): Chaldean or by triplicity.'),
	]),
	('Almutens and lots', [
		('dialog', 'OMChartAlmuten', 'onChartAlmuten', 'How the almuten of the chart is scored: essential dignities, houses, the phase of the Sun and the rulers of the day and hour.'),
		('dialog', 'OMTopical', 'onTopicals', 'The topical almutens and the points each one counts.'),
		('dialog', 'OMLots', 'onLotsOpt', 'The lots: their formulas, reversal by night and the point they are measured from.'),
		('dialog', 'OMSyzygy', 'onSyzygy', 'How the prenatal syzygy is found.'),
	]),
	('Directions', [
		('dialog', 'OMPrimaryDirs', 'onPrimaryDirsOpt', 'The method of the primary directions (Placidus, Regiomontanus, Campanus...), the latitudes used, and the promissors and significators.'),
		('dialog', 'OMPrimaryKeys', 'onPrimaryKeys', 'The key of the directions: dynamic or static, and its measure.'),
		('dialog', 'OMPDsInChartOpt', 'onPDsInChartOpt', 'How the primary directions are drawn in a chart.'),
		('trad', 2),
	]),
	('Time lords', [
		('dialog', 'OMProfectionsOpt', 'onProfectionsOpt', 'Zodiacal or Placidian annual profections, and the zodiacal projections of the planets.'),
		('dialog', 'OMFirdariaOpt', 'onFirdariaOpt', 'The order of the nocturnal firdaria: Bonatus or Al Biruni.'),
		('trad', 0),
		('trad', 1),
	]),
	('Fixed stars and visibility', [
		('dialog', 'OMFixedStarsOpt', 'onFixedStarsOpt', 'Which fixed stars are used, chosen from the whole catalogue.'),
		('trad', 4),
		('trad', 3),
	]),
	('Places and time zones', [
		('dialog', 'OMDefLocationOpt', 'onDefLocationOpt', 'The place, time zone and daylight saving filled in for a new chart.'),
		('trad', 6),
	]),
]

HOUSESYSTEMS = ('OMHSPlacidus', 'OMHSKoch', 'OMHSRegiomontanus', 'OMHSCampanus', 'OMHSEqual', 'OMHSWholeSign', 'OMHSAxial', 'OMHSMorinus', 'OMHSHorizontal', 'OMHSPagePolich', 'OMHSAlcabitus', 'OMHSPorphyrius')


class SettingsWnd(wx.Dialog):

	def __init__(self, frame):
		wx.Dialog.__init__(self, frame, -1, 'Settings', size=(940, 660), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
		self.frame = frame
		self.tradctrls = []
		self.SetMinSize((720, 460))

		self.search = wx.SearchCtrl(self, -1, size=(230, -1))
		self.search.SetDescriptiveText('Search settings')
		self.search.ShowCancelButton(True)
		self.list = wx.ListBox(self, -1, size=(230, -1), style=wx.LB_SINGLE)
		self.book = wx.Simplebook(self)
		self.texts = []
		for name, entries in CATEGORIES:
			page = wx.ScrolledWindow(self.book, -1, style=wx.VSCROLL)
			page.SetScrollRate(0, 12)
			vsizer = wx.BoxSizer(wx.VERTICAL)
			head = wx.StaticText(page, -1, name)
			head.SetFont(head.GetFont().Bold().Scaled(1.4))
			vsizer.Add(head, 0, wx.ALL, 12)
			words = [name]
			for e in entries:
				words += self.addEntry(page, vsizer, e)
			page.SetSizer(vsizer)
			self.book.AddPage(page, name)
			self.texts.append(' '.join(words).lower())

		left = wx.BoxSizer(wx.VERTICAL)
		left.Add(self.search, 0, wx.EXPAND | wx.BOTTOM, 6)
		left.Add(self.list, 1, wx.EXPAND)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(left, 0, wx.EXPAND | wx.ALL, 10)
		hsizer.Add(self.book, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 10)
		close = wx.Button(self, wx.ID_CLOSE)
		self.SetEscapeId(wx.ID_CLOSE)
		note = wx.StaticText(self, -1, 'Changes take effect at once.')
		note.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
		bottom = wx.BoxSizer(wx.HORIZONTAL)
		bottom.Add(note, 0, wx.ALIGN_CENTER_VERTICAL)
		bottom.AddStretchSpacer()
		bottom.Add(close, 0)
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		mvsizer.Add(hsizer, 1, wx.EXPAND)
		mvsizer.Add(bottom, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		self.SetSizer(mvsizer)

		self.shown = list(range(len(CATEGORIES)))
		self.list.Set([c[0] for c in CATEGORIES])
		self.list.SetSelection(0)
		self.list.Bind(wx.EVT_LISTBOX, self.onCategory)
		self.search.Bind(wx.EVT_TEXT, self.onSearch)
		self.search.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.search.SetValue(''))
		close.Bind(wx.EVT_BUTTON, lambda e: self.Close())
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_ACTIVATE, self.onActivate)
		self.refresh()

	def addEntry(self, page, vsizer, e):
		"""Adds an entry to a page; returns its words for the search."""
		kind = e[0]
		if kind == 'dialog':
			key, handler, desc = e[1], e[2], e[3]
			title, keys = menutext(key) if key in mtexts.menutxts else (key, '')
			if len(e) > 4:
				title = e[4]
			box = wx.BoxSizer(wx.HORIZONTAL)
			texts = wx.BoxSizer(wx.VERTICAL)
			t = wx.StaticText(page, -1, title)
			t.SetFont(t.GetFont().Bold())
			texts.Add(t, 0)
			d = wx.StaticText(page, -1, desc + ('   (' + keys + ')' if keys else ''))
			d.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
			d.Wrap(520)
			texts.Add(d, 0, wx.TOP, 2)
			box.Add(texts, 1, wx.ALIGN_CENTER_VERTICAL)
			btn = wx.Button(page, -1, 'Edit...')
			btn.Bind(wx.EVT_BUTTON, lambda ev, h=handler: self.onEdit(h))
			box.Add(btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 12)
			vsizer.Add(box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
			return [title, desc]
		if kind == 'trad':
			title, fields = tradoptsdlg.DIALOGS[e[1]]
			t = wx.StaticText(page, -1, title)
			t.SetFont(t.GetFont().Bold())
			vsizer.Add(t, 0, wx.LEFT | wx.RIGHT, 12)
			holder = []
			sizer, ctrls = tradoptsdlg.build(page, fields, lambda: self.onTradChange(holder[0]))
			holder.append(ctrls)
			self.tradctrls.append(ctrls)
			row = wx.BoxSizer(wx.HORIZONTAL)
			row.Add(sizer, 1)
			defaults = wx.Button(page, -1, 'Defaults')
			defaults.SetToolTip('The values the program comes with')
			defaults.Bind(wx.EVT_BUTTON, lambda ev: self.onTradDefaults(ctrls))
			row.Add(defaults, 0, wx.ALIGN_BOTTOM | wx.ALL, 6)
			vsizer.Add(row, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 6)
			return [title] + [f[2] for f in fields if len(f) > 2 and isinstance(f[2], str)] + [f[1] for f in fields if f[0] == tradoptsdlg.SECTION]
		if kind == 'houses':
			grid = wx.FlexGridSizer(0, 2, 8, 10)
			self.hsys = wx.Choice(page, -1, choices=[menutext(k)[0] for k in HOUSESYSTEMS])
			self.nodes = wx.Choice(page, -1, choices=[menutext('OMNMean')[0], menutext('OMNTrue')[0]])
			for label, ctrl in (('House system', self.hsys), ('Lunar nodes', self.nodes)):
				t = wx.StaticText(page, -1, label + ':')
				t.SetFont(t.GetFont().Bold())
				grid.Add(t, 0, wx.ALIGN_CENTER_VERTICAL)
				grid.Add(ctrl, 0)
			self.hsys.Bind(wx.EVT_CHOICE, self.onHouseSystem)
			self.nodes.Bind(wx.EVT_CHOICE, self.onNodes)
			vsizer.Add(grid, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
			return ['house system', 'houses', 'nodes', 'mean', 'true'] + [menutext(k)[0] for k in HOUSESYSTEMS]
		if kind == 'general':
			self.autosave = wx.CheckBox(page, -1, 'Save the settings automatically')
			self.autosave.SetToolTip('Otherwise the settings are kept until the program closes, unless saved with "Save the settings now".')
			self.autosave.Bind(wx.EVT_CHECKBOX, self.onAutoSave)
			save = wx.Button(page, -1, 'Save the settings now')
			save.Bind(wx.EVT_BUTTON, lambda ev: self.frame.onSaveOpts(wx.CommandEvent()))
			reload = wx.Button(page, -1, 'Default settings...')
			reload.SetToolTip('Remove your saved settings and use those the program comes with')
			reload.Bind(wx.EVT_BUTTON, self.onReload)
			row = wx.BoxSizer(wx.HORIZONTAL)
			row.Add(save, 0, wx.RIGHT, 8)
			row.Add(reload, 0)
			vsizer.Add(self.autosave, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
			vsizer.Add(row, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
			return ['save', 'automatic', 'autosave', 'reload', 'default settings']
		return []

	def refresh(self):
		"""The controls as the settings are (they may have changed elsewhere)."""
		values = tradoptions.values()
		for ctrls in self.tradctrls:
			tradoptsdlg.fill(ctrls, values)
		self.hsys.SetSelection(self.frame.options.hsys)
		self.nodes.SetSelection(0 if self.frame.options.meannode else 1)
		self.autosave.SetValue(self.frame.options.autosave)

	def onActivate(self, event):
		if event.GetActive():
			self.refresh()
		event.Skip()

	def onCategory(self, event):
		sel = self.list.GetSelection()
		if sel != wx.NOT_FOUND:
			self.book.SetSelection(self.shown[sel])

	def onSearch(self, event):
		q = self.search.GetValue().strip().lower()
		current = self.book.GetSelection()
		self.shown = [i for i, text in enumerate(self.texts) if all(w in text for w in q.split())]
		self.list.Set([CATEGORIES[i][0] for i in self.shown])
		if self.shown:
			i = current if current in self.shown else self.shown[0]
			self.list.SetSelection(self.shown.index(i))
			self.book.SetSelection(i)

	def onEdit(self, handler):
		getattr(self.frame, handler)(wx.CommandEvent())
		if self:
			self.refresh()

	def changed(self):
		"""After a change of tradoptions."""
		if self.frame.options.autosave:
			tradoptions.save()
		else:
			self.frame.enableOptMenus(True)

	def onTradChange(self, ctrls):
		tradoptions.set(tradoptsdlg.values(ctrls))
		self.changed()

	def onTradDefaults(self, ctrls):
		tradoptsdlg.fill(ctrls, copy.deepcopy(tradoptions.DEFAULTS))
		self.onTradChange(ctrls)

	def onHouseSystem(self, event):
		self.frame.onHouseSystem(wx.CommandEvent(wx.wxEVT_MENU, self.frame.hsbase + self.hsys.GetSelection()))
		self.frame.setHouse()

	def onNodes(self, event):
		self.frame.onNodes(wx.CommandEvent(wx.wxEVT_MENU, self.frame.nodebase + self.nodes.GetSelection()))
		self.frame.setNode()

	def onAutoSave(self, event):
		if hasattr(self.frame, 'autosave'):
			self.frame.autosave.Check(self.autosave.GetValue())
			self.frame.onAutoSaveOpts(wx.CommandEvent())
		else:
			self.frame.options.autosave = self.autosave.GetValue()

	def onReload(self, event):
		self.frame.onReload(wx.CommandEvent())
		self.refresh()

	def onClose(self, event):
		self.frame.settingswnd = None
		self.Destroy()


def show(frame, category=None):
	"""Shows the Settings window of frame (one at a time), at a category."""
	wnd = getattr(frame, 'settingswnd', None)
	if not wnd:
		wnd = frame.settingswnd = SettingsWnd(frame)
		wnd.CenterOnParent()
	if category is not None:
		names = [c[0] for c in CATEGORIES]
		wnd.search.SetValue('')
		wnd.list.SetSelection(names.index(category))
		wnd.book.SetSelection(names.index(category))
	wnd.Show()
	wnd.Raise()
	return wnd

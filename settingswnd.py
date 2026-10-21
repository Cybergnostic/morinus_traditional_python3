"""The Settings window: every setting by category, with a search. The options of
the added techniques and the simple choices are shown here and take effect at
once; the dialogs of Morinus 6 open from their entries ("Edit...")."""

import copy
import wx
import wx.lib.scrolledpanel as scrolledpanel
import mtexts
import tradoptions
import tradoptsdlg
import settingsindex


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
		wx.Dialog.__init__(self, frame, -1, 'Settings', size=(1000, 700), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
		self.frame = frame
		self.tradctrls = []
		self.entries = []		# searchable settings with live control targets
		self.pages = []
		self.SetMinSize((850, 520))

		self.search = wx.SearchCtrl(self, -1, size=(265, -1), style=wx.TE_PROCESS_ENTER)
		self.search.SetDescriptiveText('Find a setting or option')
		self.search.ShowCancelButton(True)
		self.list = wx.ListBox(self, -1, size=(265, -1), style=wx.LB_SINGLE)
		self.result_count = wx.StaticText(self, -1, 'Browse by category')
		self.result_count.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
		self.book = wx.Simplebook(self)
		for category_index, (name, entries) in enumerate(CATEGORIES):
			page = scrolledpanel.ScrolledPanel(self.book, -1)
			self.pages.append(page)
			vsizer = wx.BoxSizer(wx.VERTICAL)
			head = wx.StaticText(page, -1, name)
			head.SetFont(head.GetFont().Bold().Scaled(1.4))
			vsizer.Add(head, 0, wx.ALL, 12)
			for e in entries:
				self.addEntry(page, vsizer, e, name, category_index)
			page.SetSizer(vsizer)
			page.SetupScrolling(scroll_x=False, scroll_y=True, rate_y=12)
			self.book.AddPage(page, name)

		left = wx.BoxSizer(wx.VERTICAL)
		left.Add(self.search, 0, wx.EXPAND | wx.BOTTOM, 6)
		left.Add(self.result_count, 0, wx.BOTTOM, 7)
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

		self.shown = settingsindex.categories(CATEGORIES)
		self.list.Set([c[0] for c in CATEGORIES])
		self.list.SetSelection(0)
		self.list.Bind(wx.EVT_LISTBOX, self.onCategory)
		self.list.Bind(wx.EVT_LISTBOX_DCLICK, self.onCategory)
		self.search.Bind(wx.EVT_TEXT, self.onSearch)
		self.search.Bind(wx.EVT_TEXT_ENTER, self.onSearchEnter)
		self.search.Bind(wx.EVT_CHAR_HOOK, self.onSearchKey)
		self.search.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.search.SetValue(''))
		close.Bind(wx.EVT_BUTTON, lambda e: self.Close())
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_ACTIVATE, self.onActivate)
		self.refresh()

	def register(self, title, category, category_index, description, control, group=''):
		"""Index a real option or dialog action without altering its behavior."""
		self.entries.append({
			'title': title, 'category': category, 'category_index': category_index,
			'description': description, 'control': control, 'group': group,
		})

	def addEntry(self, page, vsizer, e, category, category_index):
		"""Build existing controls and index their searchable targets."""
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
			d.Wrap(365)
			texts.Add(d, 0, wx.TOP, 2)
			box.Add(texts, 1, wx.ALIGN_CENTER_VERTICAL)
			btn = wx.Button(page, -1, 'Edit...')
			btn.Bind(wx.EVT_BUTTON, lambda ev, h=handler: self.onEdit(h))
			box.Add(btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 12)
			vsizer.Add(box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)
			self.register(title, category, category_index, desc, btn)
			return
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
			vsizer.Add(row, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
			for field in fields:
				if field[0] == tradoptsdlg.SECTION:
					continue
				ctrl = ctrls[field[1]][1]
				if field[0] == tradoptsdlg.CHECKS:
					ctrl = ctrl.boxes[0] if ctrl.boxes else defaults
				choices = ''
				if field[0] == tradoptsdlg.CHOICE:
					choices = ' '.join(str(label) for value, label in field[3])
				elif field[0] == tradoptsdlg.CHECKS:
					choices = ' '.join(field[3])
				self.register(field[2], category, category_index,
					' '.join((title, field[-1], choices)), ctrl, title)
			return
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
			vsizer.Add(grid, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)
			self.register('House system', category, category_index,
				'Available house systems: ' + ', '.join(menutext(k)[0] for k in HOUSESYSTEMS), self.hsys)
			self.register('Lunar nodes', category, category_index, 'Mean or true lunar nodes', self.nodes)
			return
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
			self.register('Save settings automatically', category, category_index, 'Autosave all settings', self.autosave)
			self.register('Save the settings now', category, category_index, 'Save settings manually', save)
			self.register('Default settings', category, category_index, 'Reload and reset all saved settings', reload)
			return

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

	def showEntry(self, entry, focus=False):
		"""Open its category and scroll to the specific, existing control."""
		self.book.SetSelection(entry['category_index'])
		ctrl = entry.get('control')
		if ctrl is not None:
			page = self.pages[entry['category_index']]
			wx.CallAfter(self.reveal, page, ctrl, focus)

	def reveal(self, page, ctrl, focus):
		if not self or not page or not ctrl:
			return
		page.ScrollChildIntoView(ctrl)
		if focus:
			ctrl.SetFocus()

	def onCategory(self, event):
		sel = self.list.GetSelection()
		if 0 <= sel < len(self.shown):
			self.showEntry(self.shown[sel], True)

	def onSearch(self, event):
		query = self.search.GetValue().strip()
		if query:
			self.shown = settingsindex.search(self.entries, query)
			labels = [settingsindex.label(e) for e in self.shown]
			self.result_count.SetLabel('%d matching setting%s' %
				(len(self.shown), '' if len(self.shown) == 1 else 's'))
		else:
			self.shown = settingsindex.categories(CATEGORIES)
			labels = [c[0] for c in CATEGORIES]
			self.result_count.SetLabel('Browse by category')
		self.list.Set(labels)
		if self.shown:
			self.list.SetSelection(0)
			self.showEntry(self.shown[0])

	def onSearchEnter(self, event):
		self.onCategory(event)

	def onSearchKey(self, event):
		key = event.GetKeyCode()
		if key in (wx.WXK_DOWN, wx.WXK_UP):
			if self.shown:
				old = self.list.GetSelection()
				change = 1 if key == wx.WXK_DOWN else -1
				self.list.SetSelection(max(0, min(len(self.shown) - 1, old + change)))
				self.showEntry(self.shown[self.list.GetSelection()])
		else:
			event.Skip()

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


def show(frame, category=None, setting=None):
	"""Show category or a specific (group, field-title) within the Settings window."""
	wnd = getattr(frame, 'settingswnd', None)
	if not wnd:
		wnd = frame.settingswnd = SettingsWnd(frame)
		wnd.CenterOnParent()
	if category is not None:
		names = [c[0] for c in CATEGORIES]
		wnd.search.SetValue('')
		wnd.onSearch(None)
		wnd.list.SetSelection(names.index(category))
		wnd.book.SetSelection(names.index(category))
	wnd.Show()
	wnd.Raise()
	if setting is not None:
		group, title = setting
		wnd.search.SetValue(' '.join((group, title)))
		wnd.onSearch(None)
		for index, item in enumerate(wnd.shown):
			if item['title'] == title and item['group'] == group and item['category'] == category:
				wnd.list.SetSelection(index)
				wnd.showEntry(item, True)
				break
	return wnd

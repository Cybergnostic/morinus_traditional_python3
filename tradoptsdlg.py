"""Options dialogs of the added techniques, built from a list of fields; each field
has a help text (tooltip, and the ? button), and Defaults restores the shipped
values. The values are tradoptions'."""

import i18n
import copy
import wx
import tradoptions

# field kinds
SECTION, CHOICE, INT, FLOAT, CHECK, CHECKS, TEXT = 'section', 'choice', 'int', 'float', 'check', 'checks', 'text'


def build(parent, fields, onchange=None):
	"""The controls of fields on parent, in boxes per section: (sizer, ctrls).
	onchange() is called after any control changes."""
	ctrls = {}
	vsizer = wx.BoxSizer(wx.VERTICAL)
	grid = None
	for f in fields:
		kind = f[0]
		if kind == SECTION:
			box = wx.StaticBoxSizer(wx.StaticBox(parent, label=i18n.tr(f[1])), wx.VERTICAL)
			grid = wx.FlexGridSizer(0, 2, 6, 10)
			grid.AddGrowableCol(1)
			box.Add(grid, 0, wx.EXPAND | wx.ALL, 6)
			vsizer.Add(box, 0, wx.EXPAND | wx.ALL, 6)
			continue
		key, label, help = f[1], f[2], f[-1]
		events = []
		if kind == CHOICE:
			ctrl = wx.Choice(parent, -1, choices=i18n.tr([text for value, text in f[3]]))
			events = [(ctrl, wx.EVT_CHOICE)]
		elif kind == INT:
			ctrl = wx.SpinCtrl(parent, -1, min=f[3], max=f[4])
			events = [(ctrl, wx.EVT_SPINCTRL)]
		elif kind == FLOAT:
			ctrl = wx.SpinCtrlDouble(parent, -1, min=f[3], max=f[4], inc=f[5])
			ctrl.SetDigits(f[6])
			events = [(ctrl, wx.EVT_SPINCTRLDOUBLE)]
		elif kind == CHECK:
			ctrl = wx.CheckBox(parent, -1, i18n.tr(label))
			events = [(ctrl, wx.EVT_CHECKBOX)]
		elif kind == CHECKS:
			ctrl = wx.BoxSizer(wx.HORIZONTAL)
			ctrl.boxes = [wx.CheckBox(parent, -1, i18n.tr(t)) for t in f[3]]
			for b in ctrl.boxes:
				ctrl.Add(b, 0, wx.RIGHT, 8)
				b.SetHelpText(i18n.tr(help))
				b.SetToolTip(i18n.tr(help))
				events.append((b, wx.EVT_CHECKBOX))
		else:
			ctrl = wx.TextCtrl(parent, -1, size=(180, -1))
			events = [(ctrl, wx.EVT_TEXT)]
		if kind != CHECKS:
			ctrl.SetHelpText(i18n.tr(help))
			ctrl.SetToolTip(i18n.tr(help))
		grid.Add(wx.StaticText(parent, -1, i18n.tr('' if kind == CHECK else label + ':')), 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(ctrl, 0, wx.EXPAND if kind == TEXT else 0)
		ctrls[key] = (f, ctrl)
		if onchange is not None:
			for w, evt in events:
				w.Bind(evt, lambda e: onchange())
	return vsizer, ctrls


def fill(ctrls, values):
	for key, (f, ctrl) in ctrls.items():
		v = values[key]
		kind = f[0]
		if kind == CHOICE:
			ctrl.SetSelection([value for value, text in f[3]].index(v))
		elif kind == CHECKS:
			for b, on in zip(ctrl.boxes, v):
				b.SetValue(on)
		elif kind == TEXT:
			ctrl.ChangeValue(str(v))
		else:
			ctrl.SetValue(v)


def values(ctrls):
	out = {}
	for key, (f, ctrl) in ctrls.items():
		kind = f[0]
		if kind == CHOICE:
			out[key] = f[3][ctrl.GetSelection()][0]
		elif kind == CHECKS:
			out[key] = [b.GetValue() for b in ctrl.boxes]
		elif kind == TEXT:
			out[key] = ctrl.GetValue().strip()
		else:
			out[key] = ctrl.GetValue()
	return out


class TradOptsDlg(wx.Dialog):

	def __init__(self, parent, title, fields):
		wx.Dialog.__init__(self)
		self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		self.Create(parent, -1, i18n.tr(title), style=wx.DEFAULT_DIALOG_STYLE)
		self.fields = fields
		mvsizer, self.ctrls = build(self, fields)
		btnsizer = wx.StdDialogButtonSizer()
		if wx.Platform != '__WXMSW__':
			btnsizer.AddButton(wx.ContextHelpButton(self))
		ok = wx.Button(self, wx.ID_OK)
		ok.SetDefault()
		btnsizer.AddButton(ok)
		btnsizer.AddButton(wx.Button(self, wx.ID_CANCEL))
		btnsizer.Realize()
		defaults = wx.Button(self, -1, i18n.tr('Defaults'))
		defaults.SetToolTip(i18n.tr('Fill in the values the program comes with (saved only with OK)'))
		bottom = wx.BoxSizer(wx.HORIZONTAL)
		bottom.Add(defaults, 0, wx.ALIGN_CENTER_VERTICAL)
		bottom.AddStretchSpacer()
		bottom.Add(btnsizer, 0)
		mvsizer.Add(bottom, 0, wx.EXPAND | wx.ALL, 10)
		self.SetSizerAndFit(mvsizer)
		defaults.Bind(wx.EVT_BUTTON, lambda e: self.fill(copy.deepcopy(tradoptions.DEFAULTS)))
		self.fill(tradoptions.values())

	def fill(self, values):
		fill(self.ctrls, values)

	def values(self):
		return values(self.ctrls)


DIALOGS = [
	('Zodiacal releasing', [
		(SECTION, 'Periods'),
		(CHOICE, 'zr_yeardays', 'Length of a year', [(360.0, '360 days (Valens)'), (365.25, '365.25 days (solar year)')],
			'Valens counts the periods in years of 360 days (12 months of 30 days); some astrologers use solar years.'),
		(INT, 'zr_years', 'Years shown', 30, 150, 'How many years after the birth the table lists.'),
	]),
	('Decennials', [
		(SECTION, 'Periods'),
		(CHOICE, 'dec_start', 'Start from', [('sect', 'the sect light (Valens)'), ('sun', 'the Sun'), ('moon', 'the Moon'),
			('asc', 'the first planet after the Ascendant'), ('fortune', 'the first planet after the Lot of Fortune')],
			'The planet that rules the first 10 years 9 months; the others follow in the zodiacal order of the chart.'),
		(CHOICE, 'dec_monthdays', 'Length of a month', [(30.0, '30 days (Valens)'), (30.4375, 'a twelfth of a solar year (30.44 days)')],
			'The periods are counted in months: 129 for each planet at level 1, the minor years as months at level 2.'),
		(INT, 'dec_years', 'Years shown', 30, 150, 'How many years after the birth the table lists.'),
	]),
	('Circumambulation', [
		(SECTION, 'Directing'),
		(CHOICE, 'ca_point', 'Point directed', [('asc', 'Ascendant (oblique ascensions)'), ('mc', 'Midheaven (right ascensions)')],
			'The Ascendant moves through the bounds by the oblique ascensions of the birth latitude, the Midheaven by right ascensions.'),
		(CHOICE, 'ca_key', 'Key', [('ptolemy', 'Ptolemy: 1 degree = 1 year'), ('naibod', 'Naibod: 0\xb059\'08" = 1 year')],
			'How many years each degree of ascension stands for.'),
		(CHECKS, 'ca_rays', 'Participants', ['conjunction', 'sextile', 'square', 'trine', 'opposition'],
			'The bodies and rays of the planets that are listed as participants.'),
		(INT, 'ca_years', 'Years shown', 30, 150, 'How many years after the birth the table lists.'),
	]),
	('Heliacal phenomena', [
		(SECTION, 'Phasis'),
		(INT, 'hel_phasisdays', 'Phasis within (days)', 1, 30, 'A visibility event or station this close to the birth counts as phasis (7 days in the Hellenistic texts).'),
		(INT, 'hel_stationdays', 'Stations within (days)', 7, 60, 'Stations are listed when this close to the birth.'),
		(SECTION, 'Observer and atmosphere'),
		(FLOAT, 'hel_pressure', 'Air pressure (hPa, 0 = standard)', 0.0, 1100.0, 1.0, 0, 'Atmospheric pressure at the place; 0 uses the standard 1013.25 hPa.'),
		(FLOAT, 'hel_temperature', 'Temperature (\xb0C)', -40.0, 50.0, 1.0, 0, 'Air temperature at the place.'),
		(FLOAT, 'hel_humidity', 'Relative humidity (%)', 0.0, 100.0, 5.0, 0, 'Humid air lets less light through: planets are seen later.'),
		(INT, 'hel_age', 'Age of the observer', 10, 90, 'The eyes of older observers need a darker sky.'),
	]),
	('Fixed stars on the angles', [
		(SECTION, 'Stars on the angles'),
		(INT, 'fsa_minutes', 'At the birth: within (minutes)', 1, 120, 'Stars rising, culminating, setting or anticulminating this close to the time of birth.'),
		(INT, 'fsa_paranminutes', 'Paranatellonta: within (minutes)', 1, 30, 'A planet and a star on angles this close together on the birth day form a paranatellon (4 minutes is about one degree).'),
	]),
	('Places and time zones', [
		(SECTION, 'Search'),
		(CHECK, 'place_atlas', 'Search the offline atlas first', 'The atlas of 236,000 places in Res/atlas.db; works without internet.'),
		(CHECK, 'place_online', 'Search online (GeoNames) when the atlas has no such place', 'Needs internet; the free GeoNames service limits how many searches a user name may make.'),
		(TEXT, 'place_username', 'GeoNames user name', 'Make a free account at geonames.org and enter its name here, so your searches do not share the limit of all Morinus users.'),
		(SECTION, 'Time zone'),
		(CHECK, 'place_timezone', "Offer the birth date's time zone after choosing a place", 'The zone and daylight saving in force at the place on the birth date, for confirmation.'),
	]),
	('Windows and errors', [
		(SECTION, 'Windows'),
		(CHECK, 'win_remember', 'Open windows with their last size and position', 'Kept in Opts/windows.json.'),
		(SECTION, 'Errors'),
		(CHECK, 'err_show', 'Show a message when something goes wrong', 'The details are written to morinus-error.log in any case.'),
	]),
	('Traditional aspects', [
		(SECTION, 'Aspect rules'),
		(CHOICE, 'aspect_preset', 'Aspect preset',
			[('traditional', 'Traditional (course)'), ('legacy', 'Legacy Morinus'), ('custom', 'Custom planetary orbs')],
			'Traditional uses the course planetary orbs and Custom the values below; two planets are configured within the larger of their two orbs, and across a sign boundary only within three degrees. Legacy retains the original Morinus aspect algorithm.'),
		(SECTION, 'Custom planetary orbs'),
		(FLOAT, 'aspect_custom_saturn', 'Saturn orb', 0.0, 20.0, 0.5, 1, 'Used only with the Custom planetary orbs preset.'),
		(FLOAT, 'aspect_custom_jupiter', 'Jupiter orb', 0.0, 20.0, 0.5, 1, 'Used only with the Custom planetary orbs preset.'),
		(FLOAT, 'aspect_custom_mars', 'Mars orb', 0.0, 20.0, 0.5, 1, 'Used only with the Custom planetary orbs preset.'),
		(FLOAT, 'aspect_custom_sun', 'Sun orb', 0.0, 20.0, 0.5, 1, 'Used only with the Custom planetary orbs preset.'),
		(FLOAT, 'aspect_custom_venus', 'Venus orb', 0.0, 20.0, 0.5, 1, 'Used only with the Custom planetary orbs preset.'),
		(FLOAT, 'aspect_custom_mercury', 'Mercury orb', 0.0, 20.0, 0.5, 1, 'Used only with the Custom planetary orbs preset.'),
		(FLOAT, 'aspect_custom_moon', 'Moon orb', 0.0, 20.0, 0.5, 1, 'Used only with the Custom planetary orbs preset.'),
	]),
]


def show(parent, index, autosave):
	"""Shows options dialog index; True if the options were changed."""
	title, fields = DIALOGS[index]
	dlg = TradOptsDlg(parent, title, fields)
	dlg.CenterOnParent()
	changed = False
	if dlg.ShowModal() == wx.ID_OK:
		new = dlg.values()
		old = tradoptions.values()
		if any(old[k] != v for k, v in new.items()):
			tradoptions.set(new)
			changed = True
			if autosave:
				tradoptions.save()
	dlg.Destroy()
	return changed

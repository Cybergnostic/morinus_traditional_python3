"""Chart look: the colour theme, the weight of the lines and smooth drawing,
with a preview of the open chart."""

import i18n
import copy
import wx
import tradoptions
import themes
import graphchart

CUSTOM = 'Your colours (Options > Colors)'
LINES = [('fine', 'Fine: light ticks and dividers'), ('morinus', 'Morinus 6: heavy circles and ticks')]
QUALITY = [('standard', 'Standard (original rendering)'), ('high', 'High quality (2x glyphs and wheel)')]
PREVIEW = 380


class ChartLookDlg(wx.Dialog):

	def __init__(self, parent, options, horoscope):
		wx.Dialog.__init__(self, parent, -1, i18n.tr('Chart look'), style=wx.DEFAULT_DIALOG_STYLE)
		self.options = options
		self.horoscope = horoscope
		self.custom = themes.current(options) is None
		self.names = ([CUSTOM] if self.custom else []) + list(themes.NAMES)

		grid = wx.FlexGridSizer(0, 2, 8, 10)
		self.theme = wx.Choice(self, -1, choices=i18n.tr(self.names))
		self.theme.SetToolTip(i18n.tr('Ink: black on white. Instrument: soft ink lines, muted planet colours. Classic: the colours of Morinus 6. '
			'A theme sets all the colours of Options > Colors, where they can still be changed one by one.'))
		self.lines = wx.Choice(self, -1, choices=i18n.tr([text for value, text in LINES]))
		self.lines.SetToolTip(i18n.tr('Fine lines keep the circles and the house cusps strong and draw the degree ticks and the dividers of terms and decans lighter.'))
		self.smooth = wx.CheckBox(self, -1, i18n.tr('Smooth (antialiased) lines'))
		self.smooth.SetToolTip(i18n.tr('Draws the wheel with antialiasing on Windows; on Linux and macOS lines are always smooth.'))
		self.quality = wx.Choice(self, -1, choices=[title for value, title in QUALITY])
		self.quality.SetToolTip(i18n.tr('High quality draws at twice the resolution, then reduces to the same size. '
			'It improves symbols and labels, but uses more memory and is slower on large charts. '
			'Very large or tiny windows automatically use standard quality.'))
		for label, ctrl in (('Theme', self.theme), ('Lines', self.lines), ('', self.smooth), ('Rendering', self.quality)):
			grid.Add(wx.StaticText(self, -1, i18n.tr(label + ':' if label else '')), 0, wx.ALIGN_CENTER_VERTICAL)
			grid.Add(ctrl, 0)

		left = wx.BoxSizer(wx.VERTICAL)
		left.Add(grid, 0, wx.ALL, 10)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(left, 0)
		self.preview = None
		if horoscope is not None:
			self.preview = wx.StaticBitmap(self, -1, wx.Bitmap(PREVIEW, PREVIEW))
			hsizer.Add(self.preview, 0, wx.ALL, 10)

		btnsizer = wx.StdDialogButtonSizer()
		ok = wx.Button(self, wx.ID_OK)
		ok.SetDefault()
		btnsizer.AddButton(ok)
		btnsizer.AddButton(wx.Button(self, wx.ID_CANCEL))
		btnsizer.Realize()
		defaults = wx.Button(self, -1, i18n.tr('Defaults'))
		defaults.SetToolTip(i18n.tr('Ink theme, fine and smooth lines (saved only with OK)'))
		bottom = wx.BoxSizer(wx.HORIZONTAL)
		bottom.Add(defaults, 0, wx.ALIGN_CENTER_VERTICAL)
		bottom.AddStretchSpacer()
		bottom.Add(btnsizer, 0)
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		mvsizer.Add(hsizer, 0)
		mvsizer.Add(bottom, 0, wx.EXPAND | wx.ALL, 10)
		self.SetSizerAndFit(mvsizer)

		self.theme.SetSelection(0 if self.custom else self.names.index(themes.current(options)))
		self.lines.SetSelection([v for v, t in LINES].index(tradoptions.get('chart_lines')))
		self.smooth.SetValue(tradoptions.get('chart_smooth'))
		self.quality.SetSelection([v for v, title in QUALITY].index(tradoptions.get('chart_quality')))
		defaults.Bind(wx.EVT_BUTTON, self.onDefaults)
		for ctrl in (self.theme, self.lines, self.quality):
			ctrl.Bind(wx.EVT_CHOICE, self.onChange)
		self.smooth.Bind(wx.EVT_CHECKBOX, self.onChange)
		self.drawPreview()

	def onDefaults(self, event):
		self.theme.SetSelection(self.names.index('Ink'))
		self.lines.SetSelection(0)
		self.smooth.SetValue(tradoptions.DEFAULTS['chart_smooth'])
		self.quality.SetSelection([v for v, title in QUALITY].index(tradoptions.DEFAULTS['chart_quality']))
		self.drawPreview()

	def onChange(self, event):
		self.drawPreview()

	def themeName(self):
		name = self.names[self.theme.GetSelection()]
		return None if name == CUSTOM else name

	def lookValues(self):
		return {'chart_lines': LINES[self.lines.GetSelection()][0], 'chart_smooth': self.smooth.GetValue(),
			'chart_quality': QUALITY[self.quality.GetSelection()][0]}

	def drawPreview(self):
		if self.preview is None:
			return
		opts = copy.copy(self.options)
		if self.themeName():
			themes.apply(opts, self.themeName())
		saved = tradoptions.values()
		tradoptions.set(self.lookValues())
		try:
			bmp = graphchart.GraphChart(self.horoscope, (PREVIEW, PREVIEW), opts, False, None).drawChart()
		finally:
			tradoptions.set({k: saved[k] for k in self.lookValues()})
		self.preview.SetBitmap(bmp)


def show(parent, options, horoscope):
	"""Shows the dialog; returns (colours changed, look changed)."""
	dlg = ChartLookDlg(parent, options, horoscope)
	dlg.CenterOnParent()
	colours = look = False
	if dlg.ShowModal() == wx.ID_OK:
		name = dlg.themeName()
		if name and name != themes.current(options):
			themes.apply(options, name)
			colours = True
		new = dlg.lookValues()
		if any(tradoptions.get(k) != v for k, v in new.items()):
			tradoptions.set(new)
			look = True
	dlg.Destroy()
	return colours, look

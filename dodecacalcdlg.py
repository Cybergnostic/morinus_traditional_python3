"""Dodecatemoria calculator: the dodecatemorion (twelfth part) of any degree."""

import i18n
import wx

SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')


def dodecatemorion(lon):
	"""As dodecatemoria.Dodecatemoria.calc: the sign's start plus twelve times
	the degrees within it."""
	return (30.0 * (lon // 30.0) + 12.0 * (lon % 30.0)) % 360.0


def lonstr(lon):
	d = int(lon % 30.0)
	m = int(round((lon % 1.0) * 60.0))
	if m == 60:
		d, m = d + 1, 0
	return "%d\xb0%02d' %s" % (d, m, SIGNS[int(lon // 30.0) % 12])


class DodecaCalcDlg(wx.Dialog):

	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, i18n.tr('Dodecatemoria calculator'), style=wx.DEFAULT_DIALOG_STYLE)
		self.sign = wx.Choice(self, -1, choices=i18n.tr(SIGNS))
		self.sign.SetSelection(0)
		self.deg = wx.SpinCtrl(self, -1, min=0, max=29, initial=0)
		self.min = wx.SpinCtrl(self, -1, min=0, max=59, initial=0)
		self.result = wx.StaticText(self, -1, '')
		row = wx.BoxSizer(wx.HORIZONTAL)
		for ctrl, label in ((self.deg, '\xb0'), (self.min, "'"), (self.sign, '')):
			row.Add(ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
			if label:
				row.Add(wx.StaticText(self, -1, i18n.tr(label)), 0, wx.ALIGN_CENTER_VERTICAL)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(row, 0, wx.ALL, 8)
		sizer.Add(self.result, 0, wx.ALL, 10)
		sizer.Add(self.CreateStdDialogButtonSizer(wx.CLOSE), 0, wx.EXPAND | wx.ALL, 8)
		self.SetSizerAndFit(sizer)
		for ctrl in (self.deg, self.min):
			ctrl.Bind(wx.EVT_SPINCTRL, self.update)
			ctrl.Bind(wx.EVT_TEXT, self.update)
		self.sign.Bind(wx.EVT_CHOICE, self.update)
		self.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE), id=wx.ID_CLOSE)
		self.update(None)

	def update(self, event):
		lon = self.sign.GetSelection() * 30.0 + self.deg.GetValue() + self.min.GetValue() / 60.0
		self.result.SetLabel(i18n.tr('Dodecatemorion of %s:  %s') % (lonstr(lon), lonstr(dodecatemorion(lon))))
		self.Fit()

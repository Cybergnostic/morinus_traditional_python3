"""On GTK (Linux) controls need more room than on Windows, for which Morinus's
fixed sizes were chosen: when a dialog or window is first shown, lists, number
fields and spin controls narrower than their contents are widened and the
dialog is laid out again."""

import wx


def needed(c):
	"""The width a control needs for its contents, or None to leave it."""
	if isinstance(c, wx.TextCtrl):
		if c.IsMultiLine():
			return None
		sample = c.GetValue()
		maxim = getattr(c.GetValidator(), 'maxim', None)
		if maxim is not None and len(str(maxim)) > len(sample):
			sample = str(maxim)
		if not sample:
			return None
		return c.GetSizeFromTextSize(c.GetTextExtent(sample)).width
	if isinstance(c, (wx.ComboBox, wx.Choice, wx.SpinCtrl)):
		return c.GetBestSize().width
	return None


def fit(win):
	changed = False
	stack = list(win.GetChildren())
	while stack:
		c = stack.pop()
		stack.extend(c.GetChildren())
		try:
			w = needed(c)
		except Exception:
			continue
		if w is not None and c.GetSize().width < w:
			c.SetMinSize((w, c.GetMinSize().height))
			c.SetSize((w, c.GetSize().height))
			changed = True
	if changed and win.GetSizer() is not None:
		if isinstance(win, wx.Dialog):
			win.Fit()
		else:
			win.Layout()


def _once(win):
	if not getattr(win, '_gtkfit', False):
		win._gtkfit = True
		fit(win)


def install():
	if wx.Platform != '__WXGTK__':
		return
	showmodal = wx.Dialog.ShowModal
	show = wx.TopLevelWindow.Show

	def showModalFitted(self):
		_once(self)
		return showmodal(self)

	def showFitted(self, show_=True):
		if show_:
			_once(self)
		return show(self, show_)
	wx.Dialog.ShowModal = showModalFitted
	wx.TopLevelWindow.Show = showFitted

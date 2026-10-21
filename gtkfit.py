"""Morinus's fixed control sizes were chosen for Windows XP; on GTK (Linux) and
current Windows some controls need more room: when a dialog or window is first
shown, lists, number fields and spin controls narrower than their contents are
widened, sliders lower than they need are heightened, and the dialog is laid out again (on any platform; nothing is made
smaller)."""

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
		# sliders with labels need more height on current Windows (35 of 39 pixels)
		if isinstance(c, wx.Slider) and c.GetSize().height < c.GetBestSize().height:
			h = c.GetBestSize().height
			c.SetMinSize((c.GetMinSize().width, h))
			c.SetSize((c.GetSize().width, h))
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
	showmodal = wx.Dialog.ShowModal

	def showModalFitted(self):
		_once(self)
		return showmodal(self)
	wx.Dialog.ShowModal = showModalFitted
	# Dialog and Frame each have their own Show
	for cls in (wx.Dialog, wx.Frame):
		def showFitted(self, show_=True, _show=cls.Show):
			if show_:
				_once(self)
			return _show(self, show_)
		cls.Show = showFitted

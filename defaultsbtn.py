"""A Defaults button for Morinus's options dialogs: it fills the dialog with the
values the program comes with (options.def_*); they are kept only with OK."""

import copy
import wx


def defaults(options):
	"""A copy of the options with every value that has a default set to it."""
	d = copy.copy(options)
	for name in dir(options):
		if name.startswith('def_') and hasattr(options, name[4:]):
			setattr(d, name[4:], copy.deepcopy(getattr(options, name)))
	return d


def add(dlg, options):
	"""Puts Defaults beside the dialog's OK button; the dialog has fill(options)."""
	ok = dlg.FindWindowById(wx.ID_OK, dlg)
	sizer = ok.GetContainingSizer() if ok is not None else None
	if sizer is None:
		return
	btn = wx.Button(dlg, -1, 'Defaults')
	btn.SetToolTip('Fill in the values the program comes with (kept only with OK)')
	btn.SetHelpText('Fill in the values the program comes with (kept only with OK)')
	sizer.Insert(0, btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 20)
	dlg.Layout()
	dlg.Fit()
	btn.Bind(wx.EVT_BUTTON, lambda e: dlg.fill(defaults(options)))

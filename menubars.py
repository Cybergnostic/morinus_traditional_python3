"""Menu bars for the chart and table windows: a copy of a window's right-click
menu, so that its commands can be found without knowing to right-click.
Choosing a copied item sends the original item's command to the window, and
the copy takes the checks and enabled states of the original when opened."""

import wx


def mirror(frame, popup, target, label, skip=()):
	"""Gives frame a menu bar with a copy of popup, whose commands are handled
	by target; the items whose ids are in skip (those acting on the clicked
	place) stay in the right-click menu only. Call after popup is complete."""
	if not frame or frame.GetMenuBar() is not None:
		return
	links = []
	bar = wx.MenuBar()
	bar.Append(_copy(popup, frame, target, skip, links), label)
	frame.SetMenuBar(bar)

	def sync(event):
		for c, item in links:
			if c.GetItemLabel() != item.GetItemLabel():	# e.g. 'Zoom: 120%'
				c.SetItemLabel(item.GetItemLabel())
			if c.IsCheckable():
				c.Check(item.IsChecked())
			c.Enable(item.IsEnabled())
		event.Skip()
	frame.Bind(wx.EVT_MENU_OPEN, sync)


def later(window, label, skip=()):
	"""mirror() of window.pmenu once the constructors have finished adding to
	it. window is a frame, or a window in a frame of its own."""
	def go():
		if not window:
			return
		frame = window if isinstance(window, wx.Frame) else window.GetParent()
		if isinstance(frame, wx.Frame):
			mirror(frame, window.pmenu, window, label, skip)
	wx.CallAfter(go)


def _copy(menu, frame, target, skip, links):
	m = wx.Menu()
	for item in menu.GetMenuItems():
		if item.IsSeparator():
			if m.GetMenuItemCount():
				m.AppendSeparator()
			continue
		if item.GetId() in skip:
			continue
		if item.GetSubMenu() is not None:
			m.AppendSubMenu(_copy(item.GetSubMenu(), frame, target, skip, links), item.GetItemLabel())
			continue
		c = m.Append(wx.NewIdRef(), item.GetItemLabel(), item.GetHelp(), item.GetKind())
		links.append((c, item))
		frame.Bind(wx.EVT_MENU, lambda e, item=item: _forward(target, item, e), id=c.GetId())
	return m


def _forward(target, item, event):
	if item.GetKind() == wx.ITEM_CHECK:
		item.Check(not item.IsChecked())
	elif item.GetKind() == wx.ITEM_RADIO:
		item.Check(True)
	cmd = wx.CommandEvent(wx.wxEVT_MENU, item.GetId())
	cmd.SetInt(int(item.IsChecked()) if item.IsCheckable() else 0)
	cmd.SetEventObject(target)
	target.GetEventHandler().ProcessEvent(cmd)

"""Command search (Ctrl+K): finds any command of the menus, and the settings of
the Settings window, by words of its name, its menu or its help text. Up and
Down choose among the results, Enter runs one, Escape leaves."""

import wx
import settingswnd

MAXRESULTS = 12


def commands(frame):
	"""(label, where, help, run) of every enabled command of frame's menus and
	of the Settings window."""
	res = []

	def walk(menu, where):
		for item in menu.GetMenuItems():
			if item.IsSeparator():
				continue
			label = item.GetItemLabelText().rstrip('.').strip()
			if item.GetSubMenu() is not None:
				walk(item.GetSubMenu(), where + ' › ' + label)
			elif item.IsEnabled() and label:
				res.append((label, where, item.GetHelp(), lambda item=item: run(frame, item)))
	bar = frame.GetMenuBar()
	for i in range(bar.GetMenuCount()):
		walk(bar.GetMenu(i), bar.GetMenuLabelText(i))
	for cat, entries in settingswnd.CATEGORIES:
		for e in entries:
			where = 'Settings › ' + cat
			if e[0] == 'dialog':
				title = e[4] if len(e) > 4 else settingswnd.menutext(e[1])[0] if e[1] in settingswnd.mtexts.menutxts else e[1]
				res.append((title, where, e[3], lambda h=e[2]: getattr(frame, h)(wx.CommandEvent())))
			elif e[0] == 'trad':
				title = settingswnd.tradoptsdlg.DIALOGS[e[1]][0]
				res.append((title + ' options', where, '', lambda c=cat: settingswnd.show(frame, c)))
		res.append((cat, 'Settings', 'The settings of ' + cat.lower(), lambda c=cat: settingswnd.show(frame, c)))
	return res


def run(frame, item):
	"""Runs a menu item as if chosen."""
	if item.GetKind() == wx.ITEM_CHECK:
		item.Check(not item.IsChecked())
	elif item.GetKind() == wx.ITEM_RADIO:
		item.Check(True)
	evt = wx.CommandEvent(wx.wxEVT_MENU, item.GetId())
	evt.SetInt(int(item.IsChecked()) if item.IsCheckable() else 0)
	evt.SetEventObject(frame)
	frame.GetEventHandler().ProcessEvent(evt)


def search(cmds, query):
	"""The commands matching every word of query, best first."""
	words = query.lower().split()
	if not words:
		return []
	scored = []
	for n, c in enumerate(cmds):
		label, where, help = c[0].lower(), c[1].lower(), c[2].lower()
		text = ' '.join((label, where, help))
		if not all(w in text for w in words):
			continue
		score = 0 if label.startswith(words[0]) else 1 if all(w in label for w in words) else 2 if all(w in label + ' ' + where for w in words) else 3
		scored.append((score, n, c))
	scored.sort(key=lambda s: s[:2])
	return [c for s, n, c in scored[:MAXRESULTS]]


class CommandSearch(wx.SearchCtrl):

	def __init__(self, parent, frame, width=300):
		wx.SearchCtrl.__init__(self, parent, -1, size=(width, -1), style=wx.TE_PROCESS_ENTER)
		self.frame = frame
		self.SetDescriptiveText('Search commands  (Ctrl+K)')
		self.ShowCancelButton(True)
		self.SetToolTip('Type part of the name of any command or setting; Up and Down choose, Enter runs it')
		self.results = []
		self.popup = wx.PopupWindow(frame, wx.BORDER_SIMPLE)
		self.list = wx.ListBox(self.popup, -1, style=wx.LB_SINGLE)
		self.Bind(wx.EVT_TEXT, self.onText)
		self.Bind(wx.EVT_TEXT_ENTER, lambda e: self.runSelected())
		self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.leave())
		self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
		self.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
		self.list.Bind(wx.EVT_LISTBOX_DCLICK, lambda e: self.runSelected())
		self.list.Bind(wx.EVT_LEFT_UP, self.onListClick)

	def start(self):
		"""Ctrl+K: to the search box."""
		self.SetFocus()
		self.SelectAll()

	def onText(self, event):
		self.cmds = commands(self.frame) if self.GetValue().strip() else []
		self.results = search(self.cmds, self.GetValue())
		if not self.results:
			self.popup.Hide()
			return
		self.list.Set(['%s      — %s' % (c[0], c[1]) for c in self.results])
		self.list.SetSelection(0)
		w = max(self.GetSize().x, 420)
		h = len(self.results) * (self.list.GetCharHeight() * 3 // 2 + 2) + 6
		self.list.SetSize((w, h))
		self.popup.SetSize((w, h))
		pos = self.ClientToScreen((self.GetSize().x - w, self.GetSize().y + 2))
		self.popup.Position(pos, (0, 0))
		self.popup.Show()

	def onKey(self, event):
		key = event.GetKeyCode()
		if key in (wx.WXK_DOWN, wx.WXK_UP) and self.popup.IsShown():
			n = self.list.GetCount()
			sel = self.list.GetSelection() + (1 if key == wx.WXK_DOWN else -1)
			self.list.SetSelection(max(0, min(n - 1, sel)))
		elif key == wx.WXK_ESCAPE:
			self.leave()
		elif key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			self.runSelected()
		else:
			event.Skip()

	def onListClick(self, event):
		event.Skip()
		wx.CallAfter(self.runSelected)

	def onKillFocus(self, event):
		event.Skip()
		# a click on the results takes the focus first
		wx.CallLater(200, self.hideUnlessFocused)

	def hideUnlessFocused(self):
		if self and not self.HasFocus():
			self.popup.Hide()

	def runSelected(self):
		sel = self.list.GetSelection()
		if not self.results or sel == wx.NOT_FOUND:
			return
		cmd = self.results[sel]
		self.leave()
		cmd[3]()

	def leave(self):
		self.popup.Hide()
		self.ChangeValue('')
		self.results = []
		self.frame.SetFocus()

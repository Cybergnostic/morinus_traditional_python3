"""Searchable Morinus command palette (Ctrl+K), independent of the toolbar.

    Every enabled menu command and all Settings categories are searchable;
    keyboard navigation and run/close behavior are shared by all entry points.
"""
import wx
import settingswnd
import commandindex

MAXRESULTS = commandindex.MAX_RESULTS


def commands(frame):
    """Return (label, menu path, description, execute) for available actions."""
    res = []

    def walk(menu, where):
        for item in menu.GetMenuItems():
            if item.IsSeparator():
                continue
            label = item.GetItemLabelText().rstrip('.').strip()
            if item.GetSubMenu() is not None:
                walk(item.GetSubMenu(), where + ' › ' + label)
            elif item.IsEnabled() and label:
                res.append((label, where, item.GetHelp() or '',
                            lambda item=item: run(frame, item)))

    bar = frame.GetMenuBar()
    for i in range(bar.GetMenuCount()):
        walk(bar.GetMenu(i), bar.GetMenuLabelText(i).replace('&', ''))

    # a dialog that is also a menu command (e.g. Chart look) is listed once
    menu_labels = {commandindex.normalise(c[0]) for c in res}
    for category, entries in settingswnd.CATEGORIES:
        for entry in entries:
            where = 'Settings › ' + category
            if entry[0] == 'dialog':
                title = (entry[4] if len(entry) > 4 else
                         settingswnd.menutext(entry[1])[0] if entry[1] in settingswnd.mtexts.menutxts else entry[1])
                if commandindex.normalise(title) in menu_labels:
                    continue
                res.append((title, where, entry[3],
                            lambda handler=entry[2]: getattr(frame, handler)(wx.CommandEvent())))
            elif entry[0] == 'trad':
                title, fields = settingswnd.tradoptsdlg.DIALOGS[entry[1]]
                res.append((title + ' options', where, '',
                            lambda cat=category: settingswnd.show(frame, cat)))
                # Individual added-technique controls are directly searchable.
                for field in fields:
                    if field[0] == settingswnd.tradoptsdlg.SECTION:
                        continue
                    description = title + '. ' + field[-1]
                    if field[0] == settingswnd.tradoptsdlg.CHOICE:
                        description += ' ' + ' '.join(str(label) for value, label in field[3])
                    res.append((field[2], where + ' › ' + title, description,
                                lambda cat=category, group=title, label=field[2]:
                                    settingswnd.show(frame, cat, setting=(group, label))))
        res.append((category, 'Settings', 'Open the ' + category.lower() + ' settings',
                    lambda cat=category: settingswnd.show(frame, cat)))
    return res


def run(frame, item):
    """Dispatch exactly the same menu event as selecting the original item."""
    if item.GetKind() == wx.ITEM_CHECK:
        item.Check(not item.IsChecked())
    elif item.GetKind() == wx.ITEM_RADIO:
        item.Check(True)
    event = wx.CommandEvent(wx.wxEVT_MENU, item.GetId())
    event.SetInt(int(item.IsChecked()) if item.IsCheckable() else 0)
    event.SetEventObject(frame)
    frame.GetEventHandler().ProcessEvent(event)


def search(cmds, query):
    """Compatibility helper for existing users of this module."""
    return commandindex.search(cmds, query)


class CommandPalette(wx.Dialog):
    """Keyboard-first command search, not tied to any toolbar or popup focus."""
    def __init__(self, frame):
        super().__init__(frame, title='Find command', style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                         size=(760, 490))
        self.SetMinSize((520, 350))
        self.available = commands(frame)
        self.results = []
        self.selected_command = None

        self.query = wx.SearchCtrl(self, -1, style=wx.TE_PROCESS_ENTER)
        self.query.SetDescriptiveText('Search commands and settings')
        self.query.SetToolTip('Type words from the command, menu path, or description')
        self.query.ShowCancelButton(True)

        self.result_label = wx.StaticText(self, -1, 'Type to search menus and settings')
        self.list = wx.ListBox(self, -1, style=wx.LB_SINGLE)
        self.description = wx.StaticText(self, -1, 'Up / Down to select  ·  Enter to run  ·  Esc to close')
        self.description.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
        self.run_button = wx.Button(self, wx.ID_OK, 'Run')
        self.run_button.Enable(False)
        cancel = wx.Button(self, wx.ID_CANCEL, 'Cancel')

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.query, 0, wx.EXPAND | wx.ALL, 12)
        layout.Add(self.result_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        layout.Add(self.list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 12)
        layout.Add(self.description, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 12)
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.AddStretchSpacer()
        buttons.Add(self.run_button, 0, wx.RIGHT, 8)
        buttons.Add(cancel, 0)
        layout.Add(buttons, 0, wx.EXPAND | wx.ALL, 12)
        self.SetSizer(layout)

        self.query.Bind(wx.EVT_TEXT, self.onText)
        self.query.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onClear)
        self.list.Bind(wx.EVT_LISTBOX, self.onSelection)
        self.list.Bind(wx.EVT_LISTBOX_DCLICK, self.onRun)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
        self.run_button.Bind(wx.EVT_BUTTON, self.onRun)
        cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        self.CentreOnParent()
        wx.CallAfter(self.query.SetFocus)

    def onText(self, event):
        self.results = search(self.available, self.query.GetValue())
        self.list.Set(['%s    —    %s' % (label, path) for label, path, _, _ in self.results])
        self.result_label.SetLabel(
            '%d matching command%s' % (len(self.results), '' if len(self.results) == 1 else 's')
            if self.query.GetValue().strip() else 'Type to search menus and settings')
        if self.results:
            self.list.SetSelection(0)
        self.onSelection(None)

    def onClear(self, event):
        self.query.SetValue('')
        self.query.SetFocus()

    def onSelection(self, event):
        selection = self.list.GetSelection()
        valid = 0 <= selection < len(self.results)
        self.run_button.Enable(valid)
        if valid:
            cmd = self.results[selection]
            self.description.SetLabel(cmd[2] or cmd[1])
        else:
            self.description.SetLabel('Up / Down to select  ·  Enter to run  ·  Esc to close')
        self.Layout()

    def onKey(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        elif key in (wx.WXK_UP, wx.WXK_DOWN):
            if self.results:
                current = self.list.GetSelection()
                step = -1 if key == wx.WXK_UP else 1
                self.list.SetSelection(max(0, min(len(self.results) - 1, current + step)))
                self.onSelection(None)
        elif key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.onRun(None)
        else:
            event.Skip()

    def onRun(self, event):
        chosen = self.list.GetSelection()
        if 0 <= chosen < len(self.results):
            self.selected_command = self.results[chosen]
            self.EndModal(wx.ID_OK)

    def onCancel(self, event):
        self.EndModal(wx.ID_CANCEL)


def show(frame):
    """Open the palette and execute after it has closed (safe for modal commands)."""
    palette = CommandPalette(frame)
    try:
        accepted = palette.ShowModal() == wx.ID_OK
        command = palette.selected_command if accepted else None
    finally:
        palette.Destroy()
    if command is not None:
        wx.CallAfter(command[3])

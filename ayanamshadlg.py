# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, intvalidator, mtexts

class AyanamshaDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtsayanamshaeng['Ayanamsa'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        self.cb = wx.ComboBox(self, -1, mtexts.ayanamshalist[0], size=(250, -1), choices=mtexts.ayanamshalist, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        mvsizer.Add(self.cb, 1, wx.ALIGN_LEFT | wx.ALL, 10)
        btnsizer = wx.StdDialogButtonSizer()
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Ok'])
        btnOk.SetHelpText(mtexts.txtscommon['HelpOk'])
        btnOk.SetDefault()
        btnsizer.AddButton(btnOk)
        btn = wx.Button(self, wx.ID_CANCEL, mtexts.txtscommon['Cancel'])
        btn.SetHelpText(mtexts.txtscommon['HelpCancel'])
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        btnOk.SetFocus()

    def fill(self, options):
        self.cb.SetStringSelection(mtexts.ayanamshalist[options.ayanamsha])

    def check(self, options):
        changed = False
        sel = self.cb.GetCurrentSelection()
        if options.ayanamsha != sel:
            options.ayanamsha = sel
            changed = True
        return changed
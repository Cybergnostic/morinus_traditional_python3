# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import mtexts

class LanguagesDlg(wx.Dialog):

    def __init__(self, parent, langid):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtslangdlg['Languages'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        self.langcb = wx.ComboBox(self, -1, mtexts.langtexts[0], size=(100, -1), choices=mtexts.langtexts, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.langcb.SetStringSelection(mtexts.langtexts[langid])
        mvsizer.Add(self.langcb, 0, wx.GROW | wx.ALL, 20)
        btnsizer = wx.StdDialogButtonSizer()
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Ok'])
        btnsizer.AddButton(btnOk)
        btnOk.SetHelpText(mtexts.txtscommon['HelpOk'])
        btnOk.SetDefault()
        btn = wx.Button(self, wx.ID_CANCEL, mtexts.txtscommon['Cancel'])
        btnsizer.AddButton(btn)
        btn.SetHelpText(mtexts.txtscommon['HelpCancel'])
        btnsizer.Realize()
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        btnOk.SetFocus()

    def check(self, options):
        changed = False
        selid = self.langcb.GetCurrentSelection()
        if options.langid != selid:
            options.langid = selid
            changed = True
        return changed
# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import datetime
import wx
import intvalidator
import rangechecker
import util
import mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class GraphEphemDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtsgraphephemdlg['Ephemeris'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        rnge = 3000
        checker = rangechecker.RangeChecker()
        if checker.isExtended():
            rnge = 5000
        self.syear = wx.StaticBox(self, label=mtexts.txtsgraphephemdlg['Year'])
        yearsizer = wx.StaticBoxSizer(self.syear, wx.VERTICAL)
        self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,
                                                                                                  -1))
        yearsizer.Add(self.year, 0, wx.GROW | wx.ALL, 5)
        if checker.isExtended():
            self.year.SetHelpText(mtexts.txtsgraphephemdlg['HelpYear'])
        else:
            self.year.SetHelpText(mtexts.txtsgraphephemdlg['HelpYear2'])
        self.year.SetMaxLength(4)
        mhsizer.Add(yearsizer, 1, wx.GROW | wx.ALL, 5)
        mvsizer.Add(mhsizer, 0, wx.GROW | wx.ALL, 5)
        btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != '__WXMSW__':
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
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
        now = datetime.datetime.now()
        self.year.SetValue(str(now.year))
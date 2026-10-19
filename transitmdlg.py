# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, intvalidator, options, rangechecker, util, mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class TransitMonthDlg(wx.Dialog):

    def __init__(self, parent, time):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, -1, mtexts.txtstransitmdlg['Transit'].capitalize(), pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.PostCreate(pre)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        rnge = 3000
        checker = rangechecker.RangeChecker()
        if checker.isExtended():
            rnge = 5000
        self.stime = wx.StaticBox(self, label='')
        timesizer = wx.StaticBoxSizer(self.stime, wx.VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        fgsizer = wx.FlexGridSizer(1, 2)
        label = wx.StaticText(self, -1, mtexts.txtstransitmdlg['Year'] + ':')
        vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,
                                                                                                  -1))
        vsizer.Add(self.year, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        if checker.isExtended():
            self.year.SetHelpText(mtexts.txtstransitmdlg['HelpYear'])
        else:
            self.year.SetHelpText(mtexts.txtstransitmdlg['HelpYear2'])
        self.year.SetMaxLength(4)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtstransitmdlg['Month'] + ':')
        vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.month = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,
                                                                                                 -1))
        vsizer.Add(self.month, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.month.SetHelpText(mtexts.txtstransitmdlg['HelpMonth'])
        self.month.SetMaxLength(2)
        timesizer.Add(fgsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        mvsizer.Add(timesizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, 5)
        self.year.SetValue(str(time.year))
        self.month.SetValue(str(time.month))
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
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

    def onOK(self, event):
        if self.Validate() and self.stime.Validate():
            if util.checkDate(int(self.year.GetValue()), int(self.month.GetValue()), 1):
                self.Close()
                self.SetReturnCode(wx.ID_OK)
            else:
                dlgm = wx.MessageDialog(None, mtexts.txtstransitmdlg['InvalidDate'] + ' (' + self.year.GetValue() + '.' + self.month.GetValue() + '.)', mtexts.txtstransitmdlg['Error'], wx.OK | wx.ICON_EXCLAMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
        return
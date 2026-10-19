# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import intvalidator
import util
import rangechecker
import mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class SunTransitsDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtssuntransitsdlg['SunTransits'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.starget = wx.StaticBox(self, label='')
        targetsizer = wx.StaticBoxSizer(self.starget, wx.VERTICAL)
        self.ascrb = wx.RadioButton(self, -1, mtexts.txtssuntransitsdlg['Ascendant'], style=wx.RB_GROUP)
        targetsizer.Add(self.ascrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.mcrb = wx.RadioButton(self, -1, mtexts.txtssuntransitsdlg['MediumCoeli'])
        targetsizer.Add(self.mcrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.saturnrb = wx.RadioButton(self, -1, mtexts.txtscommon['Saturn'])
        targetsizer.Add(self.saturnrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.jupiterrb = wx.RadioButton(self, -1, mtexts.txtscommon['Jupiter'])
        targetsizer.Add(self.jupiterrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.marsrb = wx.RadioButton(self, -1, mtexts.txtscommon['Mars'])
        targetsizer.Add(self.marsrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.sunrb = wx.RadioButton(self, -1, mtexts.txtscommon['Sun'])
        targetsizer.Add(self.sunrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.venusrb = wx.RadioButton(self, -1, mtexts.txtscommon['Venus'])
        targetsizer.Add(self.venusrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.mercuryrb = wx.RadioButton(self, -1, mtexts.txtscommon['Mercury'])
        targetsizer.Add(self.mercuryrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.moonrb = wx.RadioButton(self, -1, mtexts.txtscommon['Moon'])
        targetsizer.Add(self.moonrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        mhsizer.Add(targetsizer, 0, wx.ALIGN_LEFT | wx.LEFT, 0)
        rnge = 3000
        checker = rangechecker.RangeChecker()
        if checker.isExtended():
            rnge = 5000
        self.stime = wx.StaticBox(self, label='')
        timesizer = wx.StaticBoxSizer(self.stime, wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtssuntransitsdlg['StartingDate'])
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        vsubsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer = wx.FlexGridSizer(0, 3, 0, 0)
        label = wx.StaticText(self, -1, mtexts.txtssuntransitsdlg['Year'] + ':')
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,
                                                                                                  -1))
        vsizer.Add(self.year, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        if checker.isExtended():
            self.year.SetHelpText(mtexts.txtssuntransitsdlg['HelpYear'])
        else:
            self.year.SetHelpText(mtexts.txtssuntransitsdlg['HelpYear2'])
        self.year.SetMaxLength(4)
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtssuntransitsdlg['Month'] + ':')
        vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.month = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,
                                                                                                 -1))
        self.month.SetHelpText(mtexts.txtssuntransitsdlg['HelpMonth'])
        self.month.SetMaxLength(2)
        vsizer.Add(self.month, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtssuntransitsdlg['Day'] + ':')
        vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.day = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 31), size=(50,
                                                                                               -1))
        self.day.SetHelpText(mtexts.txtssuntransitsdlg['HelpDay'])
        self.day.SetMaxLength(2)
        vsizer.Add(self.day, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsubsizer.Add(fgsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        timesizer.Add(vsubsizer, 0, wx.ALL, 5)
        mhsizer.Add(timesizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.LEFT, 5)
        mvsizer.Add(mhsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, 5)
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

    def onOK(self, event):
        if self.Validate() and self.stime.Validate():
            if util.checkDate(int(self.year.GetValue()), int(self.month.GetValue()), int(self.day.GetValue())):
                self.Close()
                self.SetReturnCode(wx.ID_OK)
            else:
                dlgm = wx.MessageDialog(None, mtexts.txtssuntransitsdlg['InvalidDate'] + ' (' + self.year.GetValue() + '.' + self.month.GetValue() + '.' + self.day.GetValue() + '.)', mtexts.txtssuntransitsdlg['Error'], wx.OK | wx.ICON_EXCLAMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
        return

    def initialize(self, chrt):
        year = chrt.time.year
        month = chrt.time.month
        day = chrt.time.day
        year, month, day = util.incrDay(year, month, day)
        self.ascrb.SetFocus()
        self.year.SetValue(str(year))
        self.month.SetValue(str(month))
        self.day.SetValue(str(day))
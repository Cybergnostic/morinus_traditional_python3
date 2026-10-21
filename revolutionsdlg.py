# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import intvalidator
import revolutions
import rangechecker
import util
import mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

def returnname(planet):
    """'Solar return', 'Lunar return', 'Mars return'... (planet: revolutions.Revolutions.SATURN...MOON)"""
    if planet == revolutions.Revolutions.SUN:
        return 'Solar return'
    if planet == revolutions.Revolutions.MOON:
        return 'Lunar return'
    return mtexts.txtscommon[('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')[planet]] + ' return'


class RevolutionsDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtsrevolutionsdlg['Revolutions'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        stype = wx.StaticBox(self, label='Return of')
        typesizer = wx.StaticBoxSizer(stype, wx.VERTICAL)
        self.pls = (
         mtexts.txtscommon['Saturn'], mtexts.txtscommon['Jupiter'], mtexts.txtscommon['Mars'], mtexts.txtscommon['Sun'], mtexts.txtscommon['Venus'], mtexts.txtscommon['Mercury'], mtexts.txtscommon['Moon'])
        self.typecb = wx.ComboBox(self, -1, self.pls[3], size=(100, -1), choices=self.pls, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        typesizer.Add(self.typecb, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        self.typecb.Bind(wx.EVT_COMBOBOX, lambda e: self.SetTitle(returnname(self.typecb.GetSelection())))
        mhsizer.Add(typesizer, 0, wx.GROW)
        rnge = 3000
        checker = rangechecker.RangeChecker()
        if checker.isExtended():
            rnge = 5000
        self.stime = wx.StaticBox(self, label='')
        timesizer = wx.StaticBoxSizer(self.stime, wx.VERTICAL)
        label = wx.StaticText(self, -1, 'First return after (midnight, UT)' if mtexts.txtsrevolutionsdlg['StartingDate'].startswith('Starting') else mtexts.txtsrevolutionsdlg['StartingDate'])
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        vsubsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer = wx.FlexGridSizer(0, 3, 0, 0)
        label = wx.StaticText(self, -1, mtexts.txtsrevolutionsdlg['Year'] + ':')
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,
                                                                                                  -1))
        vsizer.Add(self.year, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        if checker.isExtended():
            self.year.SetHelpText(mtexts.txtsrevolutionsdlg['HelpYear'])
        else:
            self.year.SetHelpText(mtexts.txtsrevolutionsdlg['HelpYear2'])
        self.year.SetMaxLength(4)
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsrevolutionsdlg['Month'] + ':')
        vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.month = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,
                                                                                                 -1))
        self.month.SetHelpText(mtexts.txtsrevolutionsdlg['HelpMonth'])
        self.month.SetMaxLength(2)
        vsizer.Add(self.month, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsrevolutionsdlg['Day'] + ':')
        vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.day = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 31), size=(50,
                                                                                               -1))
        self.day.SetHelpText(mtexts.txtsrevolutionsdlg['HelpDay'])
        self.day.SetMaxLength(2)
        vsizer.Add(self.day, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsubsizer.Add(fgsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        timesizer.Add(vsubsizer, 0, wx.ALL, 5)
        mhsizer.Add(timesizer, 0, wx.ALIGN_LEFT | wx.LEFT, 5)
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
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

    def onOK(self, event):
        if self.Validate() and self.stime.Validate():
            if util.checkDate(int(self.year.GetValue()), int(self.month.GetValue()), int(self.day.GetValue())):
                self.Close()
                self.SetReturnCode(wx.ID_OK)
            else:
                dlgm = wx.MessageDialog(None, mtexts.txtsrevolutionsdlg['InvalidDate'] + ' (' + self.year.GetValue() + '.' + self.month.GetValue() + '.' + self.day.GetValue() + '.)', mtexts.txtsrevolutionsdlg['Error'], wx.OK | wx.ICON_EXCLAMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
        return

    def setPlanet(self, planet):
        """The return of planet, named in the title."""
        self.typecb.SetSelection(planet)
        self.SetTitle(returnname(planet))

    def initialize(self, chrt):
        year = chrt.time.year
        month = chrt.time.month
        day = chrt.time.day
        year, month, day = util.incrDay(year, month, day)
        self.typecb.SetStringSelection(self.pls[revolutions.Revolutions.SUN])
        self.year.SetValue(str(year))
        self.month.SetValue(str(month))
        self.day.SetValue(str(day))
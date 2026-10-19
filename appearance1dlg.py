# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import planets
import chart
import options
import mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class Appearance1Dlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtsappearance1dlg['Appearance1'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        inchart = wx.StaticBox(self, label=mtexts.txtsappearance1dlg['InChart'])
        inchartsizer = wx.StaticBoxSizer(inchart, wx.VERTICAL)
        self.housesckb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['Houses'])
        inchartsizer.Add(self.housesckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.termsckb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['Terms'])
        inchartsizer.Add(self.termsckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.decansckb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['Decans'])
        inchartsizer.Add(self.decansckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.topocentricckb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['Topocentric'])
        inchartsizer.Add(self.topocentricckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.enableclickckb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['EnableClick'])
        inchartsizer.Add(self.enableclickckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.showdatackb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['ShowData'])
        inchartsizer.Add(self.showdatackb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.nonerb = wx.RadioButton(self, -1, mtexts.txtsappearance1dlg['None'], style=wx.RB_GROUP)
        self.Bind(wx.EVT_RADIOBUTTON, self.onNone, id=self.nonerb.GetId())
        inchartsizer.Add(self.nonerb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.fixedstarsrb = wx.RadioButton(self, -1, mtexts.txtsappearance1dlg['FixedStars'])
        self.Bind(wx.EVT_RADIOBUTTON, self.onFixedStars, id=self.fixedstarsrb.GetId())
        inchartsizer.Add(self.fixedstarsrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        vfssubsizer = wx.BoxSizer(wx.VERTICAL)
        self.fixedstarsnodesckb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['Nodes'])
        vfssubsizer.Add(self.fixedstarsnodesckb, 0, wx.ALL, 2)
        self.fixedstarshcsckb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['IntermHCs'])
        vfssubsizer.Add(self.fixedstarshcsckb, 0, wx.ALL, 2)
        self.fixedstarslofckb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['LoF'])
        vfssubsizer.Add(self.fixedstarslofckb, 0, wx.ALL, 2)
        inchartsizer.Add(vfssubsizer, 0, wx.ALIGN_LEFT | wx.LEFT, 12)
        self.antisrb = wx.RadioButton(self, -1, mtexts.txtsappearance1dlg['Antiscia'])
        self.Bind(wx.EVT_RADIOBUTTON, self.onAntis, id=self.antisrb.GetId())
        inchartsizer.Add(self.antisrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.lotrb = wx.RadioButton(self, -1, mtexts.txtsappearance1dlg['Lots'])
        self.Bind(wx.EVT_RADIOBUTTON, self.onArab, id=self.lotrb.GetId())
        inchartsizer.Add(self.lotrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.dodecrb = wx.RadioButton(self, -1, mtexts.txtsappearance1dlg['Dodecatemoria'])
        self.Bind(wx.EVT_RADIOBUTTON, self.onDodecatemoria, id=self.dodecrb.GetId())
        inchartsizer.Add(self.dodecrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        mhsizer.Add(inchartsizer, 0, wx.LEFT, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        color = wx.StaticBox(self, label=mtexts.txtsappearance1dlg['Color'])
        colorsizer = wx.StaticBoxSizer(color, wx.VERTICAL)
        self.bwrb = wx.RadioButton(self, -1, mtexts.txtsappearance1dlg['BlackAndWhite'], style=wx.RB_GROUP)
        colorsizer.Add(self.bwrb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 2)
        self.colorrb = wx.RadioButton(self, -1, mtexts.txtsappearance1dlg['InColor'])
        colorsizer.Add(self.colorrb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 2)
        vsizer.Add(colorsizer, 0, wx.GROW | wx.RIGHT, 5)
        ascmcsize = wx.StaticBox(self, label=mtexts.txtsappearance1dlg['MaxAscMCWidth'])
        ascmcsizesizer = wx.StaticBoxSizer(ascmcsize, wx.VERTICAL)
        self.ascmcsizeslider = wx.Slider(self, -1, 5, 2, 5, size=(140, -1), style=wx.SL_LABELS)
        ascmcsizesizer.Add(self.ascmcsizeslider, 1, wx.ALIGN_CENTRE, 5)
        vsizer.Add(ascmcsizesizer, 0, wx.GROW | wx.RIGHT, 5)
        tablesize = wx.StaticBox(self, label=mtexts.txtsappearance1dlg['TableSize'])
        tablesizesizer = wx.StaticBoxSizer(tablesize, wx.VERTICAL)
        self.sizeslider = wx.Slider(self, -1, 75, 50, 100, size=(140, -1), style=wx.SL_LABELS)
        tablesizesizer.Add(self.sizeslider, 1, wx.ALIGN_CENTRE, 5)
        vsizer.Add(tablesizesizer, 0, wx.GROW | wx.RIGHT, 5)
        netbook = wx.StaticBox(self, label='')
        netbooksizer = wx.StaticBoxSizer(netbook, wx.VERTICAL)
        self.netbookckb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['Netbook'])
        netbooksizer.Add(self.netbookckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        vsizer.Add(netbooksizer, 0, wx.GROW | wx.RIGHT, 5)
        fsoutorb = wx.StaticBox(self, label=mtexts.txtsappearance1dlg['FixedStars'])
        fsoutorbsizer = wx.StaticBoxSizer(fsoutorb, wx.VERTICAL)
        self.fsoutorbckb = wx.CheckBox(self, -1, mtexts.txtsappearance1dlg['FSOutOrb'])
        fsoutorbsizer.Add(self.fsoutorbckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.GROW, 2)
        vsizer.Add(fsoutorbsizer, 0, wx.GROW | wx.RIGHT, 5)
        mhsizer.Add(vsizer, 0, wx.GROW | wx.LEFT, 5)
        mvsizer.Add(mhsizer, 0, wx.GROW | wx.ALL, 0)
        btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != '__WXMSW__':
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Ok'])
        btnOk.SetHelpText(mtexts.txtscommon['HelpOk'])
        btnOk.SetDefault()
        btnsizer.AddButton(btnOk)
        btn = wx.Button(self, wx.ID_CANCEL, mtexts.txtscommon['Cancel'])
        btn.SetHelpText(mtexts.txtscommon['HelpCancel'])
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        btnOk.SetFocus()

    def onNone(self, event):
        self.enableSubFixedstars(False)

    def onFixedStars(self, event):
        self.enableSubFixedstars(True)

    def onAntis(self, event):
        self.enableSubFixedstars(False)

    def onDodecatemoria(self, event):
        self.enableSubFixedstars(False)

    def onArab(self, event):
        self.enableSubFixedstars(False)

    def onMidPts(self, event):
        self.enableSubFixedstars(False)

    def enableSubFixedstars(self, enable):
        self.fixedstarshcsckb.Enable(enable)
        self.fixedstarslofckb.Enable(enable)
        self.fixedstarsnodesckb.Enable(enable)

    def fill(self, opts):
        self.housesckb.SetValue(opts.houses)
        self.termsckb.SetValue(opts.showterms)
        self.decansckb.SetValue(opts.showdecans)
        self.topocentricckb.SetValue(opts.topocentric)
        self.enableclickckb.SetValue(opts.enableclick)
        self.showdatackb.SetValue(opts.showdata)
        if opts.bw:
            self.bwrb.SetValue(opts.bw)
        else:
            self.colorrb.SetValue(not opts.bw)
        self.ascmcsizeslider.SetValue(opts.maxascmcsize)
        self.sizeslider.SetValue(int(round(opts.tablesize * 100)))
        self.netbookckb.SetValue(opts.netbook)
        self.fsoutorbckb.SetValue(opts.showfixedstarsoutoforb)
        if opts.showobject == chart.Chart.SHOWNONE:
            self.nonerb.SetValue(True)
            self.enableSubFixedstars(False)
        elif opts.showobject == chart.Chart.SHOWFIXEDSTARS:
            self.fixedstarsrb.SetValue(True)
            self.enableSubFixedstars(True)
        elif opts.showobject == chart.Chart.SHOWANTIS:
            self.antisrb.SetValue(True)
            self.enableSubFixedstars(False)
        elif opts.showobject == chart.Chart.SHOWLOTS:
            self.lotrb.SetValue(True)
            self.enableSubFixedstars(False)
        elif opts.showobject == chart.Chart.SHOWDODECATEMORIA:
            self.dodecrb.SetValue(True)
            self.enableSubFixedstars(False)
        self.fixedstarshcsckb.SetValue(opts.showfixedstarshcs)
        self.fixedstarslofckb.SetValue(opts.showfixedstarslof)
        self.fixedstarsnodesckb.SetValue(opts.showfixedstarsnodes)

    def check(self, opts):
        changed = False
        if opts.houses != self.housesckb.GetValue():
            opts.houses = self.housesckb.GetValue()
            changed = True
        if opts.showterms != self.termsckb.GetValue():
            opts.showterms = self.termsckb.GetValue()
            changed = True
        if opts.showdecans != self.decansckb.GetValue():
            opts.showdecans = self.decansckb.GetValue()
            changed = True
        if opts.topocentric != self.topocentricckb.GetValue():
            opts.topocentric = self.topocentricckb.GetValue()
            changed = True
        if opts.enableclick != self.enableclickckb.GetValue():
            opts.enableclick = self.enableclickckb.GetValue()
            changed = True
        if opts.showdata != self.showdatackb.GetValue():
            opts.showdata = self.showdatackb.GetValue()
            changed = True
        if opts.bw != self.bwrb.GetValue():
            opts.bw = self.bwrb.GetValue()
            changed = True
        if opts.maxascmcsize != self.ascmcsizeslider.GetValue():
            opts.maxascmcsize = self.ascmcsizeslider.GetValue()
            changed = True
        if opts.tablesize != self.sizeslider.GetValue() / 100.0:
            opts.tablesize = self.sizeslider.GetValue() / 100.0
            changed = True
        if opts.netbook != self.netbookckb.GetValue():
            opts.netbook = self.netbookckb.GetValue()
            changed = True
        if opts.showfixedstarsoutoforb != self.fsoutorbckb.GetValue():
            opts.showfixedstarsoutoforb = self.fsoutorbckb.GetValue()
            changed = True
        if self.nonerb.GetValue():
            if opts.showobject != chart.Chart.SHOWNONE:
                opts.showobject = chart.Chart.SHOWNONE
                changed = True
        elif self.fixedstarsrb.GetValue():
            if opts.showobject != chart.Chart.SHOWFIXEDSTARS:
                opts.showobject = chart.Chart.SHOWFIXEDSTARS
                changed = True
        elif self.antisrb.GetValue():
            if opts.showobject != chart.Chart.SHOWANTIS:
                opts.showobject = chart.Chart.SHOWANTIS
                changed = True
        elif self.lotrb.GetValue():
            if opts.showobject != chart.Chart.SHOWLOTS:
                opts.showobject = chart.Chart.SHOWLOTS
                changed = True
        elif self.dodecrb.GetValue():
            if opts.showobject != chart.Chart.SHOWDODECATEMORIA:
                opts.showobject = chart.Chart.SHOWDODECATEMORIA
                changed = True
        if opts.showfixedstarshcs != self.fixedstarshcsckb.GetValue():
            opts.showfixedstarshcs = self.fixedstarshcsckb.GetValue()
            changed = True
        if opts.showfixedstarslof != self.fixedstarslofckb.GetValue():
            opts.showfixedstarslof = self.fixedstarslofckb.GetValue()
            changed = True
        if opts.showfixedstarsnodes != self.fixedstarsnodesckb.GetValue():
            opts.showfixedstarsnodes = self.fixedstarsnodesckb.GetValue()
            changed = True
        return changed
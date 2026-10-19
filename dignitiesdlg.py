# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, copy, planets, chart, mtexts

class DignitiesDlg(wx.Dialog):

    def __init__(self, parent, options):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtsdignitiesdlg['Dignities'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        self.options = options
        self.dignities = copy.deepcopy(self.options.dignities)
        self.baseid = wx.NewId()
        self.ID_Saturn = self.baseid
        self.ID_Jupiter = wx.NewId()
        self.ID_Mars = wx.NewId()
        self.ID_Sun = wx.NewId()
        self.ID_Venus = wx.NewId()
        self.ID_Mercury = wx.NewId()
        self.ID_Moon = wx.NewId()
        self.dombaseid = wx.NewId()
        self.ID_Domicile = self.dombaseid
        self.ID_Exaltatio = wx.NewId()
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        splanets = wx.StaticBox(self, label='')
        splanetssizer = wx.StaticBoxSizer(splanets, wx.VERTICAL)
        self.saturnrb = wx.RadioButton(self, self.ID_Saturn, mtexts.txtscommon['Saturn'], style=wx.RB_GROUP)
        splanetssizer.Add(self.saturnrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.jupiterrb = wx.RadioButton(self, self.ID_Jupiter, mtexts.txtscommon['Jupiter'])
        splanetssizer.Add(self.jupiterrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.marsrb = wx.RadioButton(self, self.ID_Mars, mtexts.txtscommon['Mars'])
        splanetssizer.Add(self.marsrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.sunrb = wx.RadioButton(self, self.ID_Sun, mtexts.txtscommon['Sun'])
        splanetssizer.Add(self.sunrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.venusrb = wx.RadioButton(self, self.ID_Venus, mtexts.txtscommon['Venus'])
        splanetssizer.Add(self.venusrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.mercuryrb = wx.RadioButton(self, self.ID_Mercury, mtexts.txtscommon['Mercury'])
        splanetssizer.Add(self.mercuryrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.moonrb = wx.RadioButton(self, self.ID_Moon, mtexts.txtscommon['Moon'])
        splanetssizer.Add(self.moonrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        mhsizer.Add(splanetssizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        sdomicile = wx.StaticBox(self, label='')
        sdomicilesizer = wx.StaticBoxSizer(sdomicile, wx.VERTICAL)
        self.domicilerb = wx.RadioButton(self, self.ID_Domicile, mtexts.txtsdignitiesdlg['Domicile'], style=wx.RB_GROUP)
        sdomicilesizer.Add(self.domicilerb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.exaltatiorb = wx.RadioButton(self, self.ID_Exaltatio, mtexts.txtsdignitiesdlg['Exaltation'])
        sdomicilesizer.Add(self.exaltatiorb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        mhsizer.Add(sdomicilesizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.arsigns = []
        ssigns = wx.StaticBox(self, label='')
        ssignssizer = wx.StaticBoxSizer(ssigns, wx.VERTICAL)
        signstxt = (mtexts.txtscommon['Aries'], mtexts.txtscommon['Taurus'], mtexts.txtscommon['Gemini'], mtexts.txtscommon['Cancer'], mtexts.txtscommon['Leo'], mtexts.txtscommon['Virgo'], mtexts.txtscommon['Libra'], mtexts.txtscommon['Scorpio'], mtexts.txtscommon['Sagittarius'], mtexts.txtscommon['Capricorn'], mtexts.txtscommon['Aquarius'], mtexts.txtscommon['Pisces'])
        for i in range(chart.Chart.SIGN_NUM):
            ckb = wx.CheckBox(self, -1, signstxt[i])
            self.arsigns.append(ckb)
            ssignssizer.Add(ckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)

        mhsizer.Add(ssignssizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        mvsizer.Add(mhsizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        btnsizer = wx.StdDialogButtonSizer()
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Ok'])
        btnOk.SetDefault()
        btnsizer.AddButton(btnOk)
        btn = wx.Button(self, wx.ID_CANCEL, mtexts.txtscommon['Cancel'])
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        btnOk.SetFocus()
        self.saturnrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
        self.jupiterrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
        self.marsrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
        self.sunrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
        self.venusrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
        self.mercuryrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
        self.moonrb.Bind(wx.EVT_RADIOBUTTON, self.onBtn)
        self.plid = self.ID_Saturn - self.baseid
        self.domicilerb.Bind(wx.EVT_RADIOBUTTON, self.onDomicile)
        self.exaltatiorb.Bind(wx.EVT_RADIOBUTTON, self.onDomicile)
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.domid = self.ID_Domicile - self.dombaseid
        for i in range(chart.Chart.SIGN_NUM):
            self.arsigns[i].SetValue(self.dignities[self.plid][0][i])

    def onBtn(self, event):
        rid = event.GetId() - self.baseid
        if rid == self.plid:
            return
        for i in range(chart.Chart.SIGN_NUM):
            self.dignities[self.plid][self.domid][i] = self.arsigns[i].GetValue()

        for i in range(chart.Chart.SIGN_NUM):
            self.arsigns[i].SetValue(self.dignities[rid][self.domid][i])

        self.plid = rid

    def onDomicile(self, event):
        rid = event.GetId() - self.dombaseid
        if rid == self.domid:
            return
        for i in range(chart.Chart.SIGN_NUM):
            self.dignities[self.plid][self.domid][i] = self.arsigns[i].GetValue()

        for i in range(chart.Chart.SIGN_NUM):
            self.arsigns[i].SetValue(self.dignities[self.plid][rid][i])

        self.domid = rid

    def onOK(self, event):
        for i in range(chart.Chart.SIGN_NUM):
            self.dignities[self.plid][self.domid][i] = self.arsigns[i].GetValue()

        self.Close()
        self.SetReturnCode(wx.ID_OK)

    def check(self, options):
        changed = False
        NODES = 2
        for i in range(planets.Planets.PLANETS_NUM):
            for d in range(2):
                for s in range(chart.Chart.SIGN_NUM):
                    if options.dignities[i][d][s] != self.dignities[i][d][s]:
                        options.dignities[i][d][s] = self.dignities[i][d][s]
                        changed = True

        return changed
# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, mtexts

class MenuSelDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtsmenuseldlg['MenuSel'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        shoroscope = wx.StaticBox(self, label=mtexts.menutxts['MHoroscope'])
        shoroscopesizer = wx.StaticBoxSizer(shoroscope, wx.VERTICAL)
        self.arhoroscope = []
        hortxts = (mtexts.menutxts['HMNew'], mtexts.menutxts['HMData'], mtexts.menutxts['HMHereAndNow'], mtexts.menutxts['HMLoad'], mtexts.menutxts['HMSave'], mtexts.menutxts['HMSaveAsBmp'], mtexts.menutxts['HMSynastry'], mtexts.menutxts['HMFindTime'], mtexts.menutxts['HMEphemeris'], mtexts.menutxts['HMClose'], mtexts.menutxts['HMExit'])
        horoscopetxts = []
        for i in range(len(hortxts)):
            idx = hortxts[i].find('\t')
            s = hortxts[i]
            if idx != -1:
                s = hortxts[i][0:idx]
            horoscopetxts.append(s)

        for i in range(len(horoscopetxts)):
            ckb = wx.CheckBox(self, -1, horoscopetxts[i])
            self.arhoroscope.append(ckb)
            shoroscopesizer.Add(ckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)

        mhsizer.Add(shoroscopesizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        val = len(hortxts) - 1
        self.arhoroscope[0].Enable(False)
        self.arhoroscope[(val - 1)].Enable(False)
        self.arhoroscope[val].Enable(False)
        stables = wx.StaticBox(self, label=mtexts.menutxts['MTable'])
        stablessizer = wx.StaticBoxSizer(stables, wx.VERTICAL)
        self.artables = []
        tabtxts = (mtexts.menutxts['TMPositions'], mtexts.menutxts['TMAlmutenZodiacal'], mtexts.menutxts['TMAlmutenChart'], mtexts.menutxts['TMAlmutenTopical'], mtexts.menutxts['TMMisc'], mtexts.menutxts['TMMunPos'], mtexts.menutxts['TMAntiscia'], mtexts.menutxts['TMAspects'], mtexts.menutxts['TMMidpoints'], mtexts.menutxts['TMRiseSet'], mtexts.menutxts['TMSpeeds'], mtexts.menutxts['TMZodPars'], mtexts.menutxts['TMFixStars'], mtexts.menutxts['TMFixStarsAsps'], mtexts.menutxts['TMLots'], mtexts.menutxts['TMStrip'], mtexts.menutxts['TMPlanetaryHours'], mtexts.menutxts['TMExactTransits'], mtexts.menutxts['TMProfections'], mtexts.menutxts['TMUserSpeculum'], mtexts.menutxts['TMFirdaria'], mtexts.menutxts['TMPrimaryDirs'])
        tablestxts = []
        for i in range(len(tabtxts)):
            idx = tabtxts[i].find('\t')
            s = tabtxts[i]
            if idx != -1:
                s = tabtxts[i][0:idx]
            tablestxts.append(s)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        for i in range(11):
            ckb = wx.CheckBox(self, -1, tablestxts[i])
            self.artables.append(ckb)
            vsizer.Add(ckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)

        hsizer.Add(vsizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(11, len(tablestxts)):
            ckb = wx.CheckBox(self, -1, tablestxts[i])
            self.artables.append(ckb)
            vsizer.Add(ckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)

        hsizer.Add(vsizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        stablessizer.Add(hsizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        mhsizer.Add(stablessizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        scharts = wx.StaticBox(self, label=mtexts.menutxts['MCharts'])
        schartssizer = wx.StaticBoxSizer(scharts, wx.VERTICAL)
        self.archarts = []
        ctxts = (mtexts.menutxts['PMTransits'], mtexts.menutxts['PMRevolutions'], mtexts.menutxts['PMSunTransits'], mtexts.menutxts['PMSecondaryDirs'], mtexts.menutxts['PMElections'], mtexts.menutxts['PMSquareChart'], mtexts.menutxts['PMSyzygy'], mtexts.menutxts['PMSyzygy2'], mtexts.menutxts['PMProfections'], mtexts.menutxts['PMHelioChart'])
        chartstxts = []
        for i in range(len(ctxts)):
            idx = ctxts[i].find('\t')
            s = ctxts[i]
            if idx != -1:
                s = ctxts[i][0:idx]
            chartstxts.append(s)

        for i in range(len(chartstxts)):
            ckb = wx.CheckBox(self, -1, chartstxts[i])
            self.archarts.append(ckb)
            schartssizer.Add(ckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)

        mhsizer.Add(schartssizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
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

    def fill(self, opts):
        ars = (
         self.arhoroscope, self.artables, self.archarts)
        for j in range(len(ars)):
            for i in range(len(ars[j])):
                ars[j][i].SetValue(opts.menusels[j][i])

    def check(self, opts):
        changed = False
        ars = (
         self.arhoroscope, self.artables, self.archarts)
        for j in range(len(ars)):
            for i in range(len(ars[j])):
                if ars[j][i].GetValue() != opts.menusels[j][i]:
                    opts.menusels[j][i] = ars[j][i].GetValue()
                    changed = True

        return changed
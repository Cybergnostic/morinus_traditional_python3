# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import mtexts

class MenuSelDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtsmenuseldlg['MenuSel'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        soptions = wx.StaticBox(self, label=mtexts.menutxts['MOptions'])
        soptionssizer = wx.StaticBoxSizer(soptions, wx.VERTICAL)
        self.aroptions = []
        otxts = (mtexts.menutxts['OMAppearance1'], mtexts.menutxts['OMAppearance2'], mtexts.menutxts['OMDignities'], mtexts.menutxts['OMTriplicities'], mtexts.menutxts['OMTerms'], mtexts.menutxts['OMDecans'], mtexts.menutxts['OMChartAlmuten'], mtexts.menutxts['OMTopical'], mtexts.menutxts['OMAyanamsha'], mtexts.menutxts['OMColors'], mtexts.menutxts['OMHouseSystem'], mtexts.menutxts['OMNodes'], mtexts.menutxts['OMOrbs'], mtexts.menutxts['OMPrimaryDirs'], mtexts.menutxts['OMPrimaryKeys'], mtexts.menutxts['OMPDsInChartOpt'], mtexts.menutxts['OMLots'], mtexts.menutxts['OMSyzygy'], mtexts.menutxts['OMFixedStarsOpt'], mtexts.menutxts['OMProfectionsOpt'], mtexts.menutxts['OMFirdariaOpt'], mtexts.menutxts['OMDefLocationOpt'], mtexts.menutxts['OMMenuSelFirst'], mtexts.menutxts['OMMenuSelSecond'], mtexts.menutxts['OMLanguages'], mtexts.menutxts['OMAutoSave'], mtexts.menutxts['OMSave'], mtexts.menutxts['OMReload'])
        optionstxts = []
        for i in range(len(otxts)):
            idx = otxts[i].find('\t')
            s = otxts[i]
            if idx != -1:
                s = otxts[i][0:idx]
            optionstxts.append(s)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        for i in range(12):
            ckb = wx.CheckBox(self, -1, optionstxts[i])
            self.aroptions.append(ckb)
            vsizer.Add(ckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)

        hsizer.Add(vsizer, 0, wx.GROW | wx.ALL, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(12, len(optionstxts)):
            ckb = wx.CheckBox(self, -1, optionstxts[i])
            self.aroptions.append(ckb)
            vsizer.Add(ckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)

        val = len(optionstxts) - 1
        self.aroptions[(val - 5)].Enable(False)
        self.aroptions[(val - 4)].Enable(False)
        self.aroptions[(val - 2)].Enable(False)
        self.aroptions[(val - 1)].Enable(False)
        self.aroptions[val].Enable(False)
        hsizer.Add(vsizer, 0, wx.GROW | wx.ALL, 5)
        soptionssizer.Add(hsizer, 0, wx.GROW | wx.LEFT, 5)
        mhsizer.Add(soptionssizer, 0, wx.GROW | wx.LEFT, 5)
        shelp = wx.StaticBox(self, label=mtexts.menutxts['MHelp'])
        shelpsizer = wx.StaticBoxSizer(shelp, wx.VERTICAL)
        self.arhelp = []
        htxts = (mtexts.menutxts['HEMHelp'], mtexts.menutxts['HEMAbout'])
        helptxts = []
        for i in range(len(htxts)):
            idx = htxts[i].find('\t')
            s = htxts[i]
            if idx != -1:
                s = htxts[i][0:idx]
            helptxts.append(s)

        for i in range(len(helptxts)):
            ckb = wx.CheckBox(self, -1, helptxts[i])
            self.arhelp.append(ckb)
            shelpsizer.Add(ckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)

        mhsizer.Add(shelpsizer, 0, wx.GROW | wx.LEFT, 5)
        mvsizer.Add(mhsizer, 0, wx.GROW | wx.ALL, 5)
        btnsizer = wx.StdDialogButtonSizer()
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Ok'])
        btnOk.SetDefault()
        btnsizer.AddButton(btnOk)
        btn = wx.Button(self, wx.ID_CANCEL, mtexts.txtscommon['Cancel'])
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        btnOk.SetFocus()

    def fill(self, opts):
        ars = (
         self.aroptions, self.arhelp)
        for j in range(len(ars)):
            for i in range(len(ars[j])):
                ars[j][i].SetValue(opts.menusels[(j + 3)][i])

    def check(self, opts):
        changed = False
        ars = (
         self.aroptions, self.arhelp)
        for j in range(len(ars)):
            for i in range(len(ars[j])):
                if ars[j][i].GetValue() != opts.menusels[(j + 3)][i]:
                    opts.menusels[(j + 3)][i] = ars[j][i].GetValue()
                    changed = True

        return changed
# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, copy, floatvalidator, planets, mtexts

class OrbsDlg(wx.Dialog):
    MAXPLANETORB = 17.0
    MAXPLANETPORB = 3.0
    MAXHOUSEORB = 6.0
    MAXDAYNIGHTORB = 7.0
    MAXFIXEDSTARORB = 10.0

    def __init__(self, parent, options, nofixedstars):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtsorbsdlg['Orbs'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        self.options = options
        self.nofixedstars = nofixedstars
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        splanets = wx.StaticBox(self, label='')
        splanetssizer = wx.StaticBoxSizer(splanets, wx.VERTICAL)
        gsizer = wx.GridSizer(7, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Saturn'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.saturnorb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETORB), size=(50,
                                                                                                                             -1))
        self.saturnorb.SetMaxLength(4)
        gsizer.Add(self.saturnorb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Jupiter'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.jupiterorb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETORB), size=(50,
                                                                                                                              -1))
        self.jupiterorb.SetMaxLength(4)
        gsizer.Add(self.jupiterorb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Mars'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.marsorb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETORB), size=(50,
                                                                                                                           -1))
        self.marsorb.SetMaxLength(4)
        gsizer.Add(self.marsorb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Sun'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.sunorb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETORB), size=(50,
                                                                                                                          -1))
        self.sunorb.SetMaxLength(4)
        gsizer.Add(self.sunorb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Venus'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.venusorb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETORB), size=(50,
                                                                                                                            -1))
        self.venusorb.SetMaxLength(4)
        gsizer.Add(self.venusorb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Mercury'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mercuryorb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETORB), size=(50,
                                                                                                                              -1))
        self.mercuryorb.SetMaxLength(4)
        gsizer.Add(self.mercuryorb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Moon'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.moonorb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETORB), size=(50,
                                                                                                                           -1))
        self.moonorb.SetMaxLength(4)
        gsizer.Add(self.moonorb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        splanetssizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        mhsizer.Add(splanetssizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.arplsorbs = (
         self.saturnorb, self.jupiterorb, self.marsorb, self.sunorb, self.venusorb, self.mercuryorb, self.moonorb)
        spplanets = wx.StaticBox(self, label=mtexts.txtsorbsdlg['Parallels'])
        spplanetssizer = wx.StaticBoxSizer(spplanets, wx.VERTICAL)
        gsizer = wx.GridSizer(7, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Saturn'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.saturnporb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETPORB), size=(50,
                                                                                                                               -1))
        self.saturnporb.SetMaxLength(3)
        gsizer.Add(self.saturnporb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Jupiter'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.jupiterporb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETPORB), size=(50,
                                                                                                                                -1))
        self.jupiterporb.SetMaxLength(3)
        gsizer.Add(self.jupiterporb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Mars'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.marsporb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETPORB), size=(50,
                                                                                                                             -1))
        self.marsporb.SetMaxLength(3)
        gsizer.Add(self.marsporb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Sun'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.sunporb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETPORB), size=(50,
                                                                                                                            -1))
        self.sunporb.SetMaxLength(3)
        gsizer.Add(self.sunporb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Venus'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.venusporb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETPORB), size=(50,
                                                                                                                              -1))
        self.venusporb.SetMaxLength(3)
        gsizer.Add(self.venusporb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Mercury'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mercuryporb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETPORB), size=(50,
                                                                                                                                -1))
        self.mercuryporb.SetMaxLength(3)
        gsizer.Add(self.mercuryporb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Moon'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.moonporb = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXPLANETPORB), size=(50,
                                                                                                                             -1))
        self.moonporb.SetMaxLength(3)
        gsizer.Add(self.moonporb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        spplanetssizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        mhsizer.Add(spplanetssizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.arpplsorbs = (
         self.saturnporb, self.jupiterporb, self.marsporb, self.sunporb, self.venusporb, self.mercuryporb, self.moonporb)
        self.scusps = wx.StaticBox(self, label=mtexts.txtsorbsdlg['PlanetsInHouse'])
        scuspssizer = wx.StaticBoxSizer(self.scusps, wx.VERTICAL)
        gsizer = wx.GridSizer(2, 2)
        label = wx.StaticText(self, -1, mtexts.txtsorbsdlg['AscMC'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.cuspascmc = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXHOUSEORB), size=(50,
                                                                                                                            -1))
        gsizer.Add(self.cuspascmc, 0, wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.LEFT, 5)
        self.cuspascmc.SetMaxLength(4)
        label = wx.StaticText(self, -1, mtexts.txtsorbsdlg['Interm'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.cuspinter = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXHOUSEORB), size=(50,
                                                                                                                            -1))
        gsizer.Add(self.cuspinter, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.cuspinter.SetMaxLength(4)
        scuspssizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(scuspssizer, 0)
        self.sdaynight = wx.StaticBox(self, label='')
        sdaynightsizer = wx.StaticBoxSizer(self.sdaynight, wx.VERTICAL)
        gsizer = wx.GridSizer(1, 2)
        label = wx.StaticText(self, -1, mtexts.txtsorbsdlg['DayNight'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.daynight = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXDAYNIGHTORB), size=(50,
                                                                                                                              -1))
        gsizer.Add(self.daynight, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.daynight.SetMaxLength(3)
        sdaynightsizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vsizer.Add(sdaynightsizer, 0)
        self.fixedstars = self.options.fixedstars.copy()
        self.prevselection = 0
        sfsorbs = wx.StaticBox(self, label=mtexts.txtsorbsdlg['FixedStars'])
        sfsorbssizer = wx.StaticBoxSizer(sfsorbs, wx.VERTICAL)
        gsizer = wx.GridSizer(2, 2)
        self.fsnames = list(self.options.fixedstars.keys())
        if self.nofixedstars:
            seltxt = ''
            arseltxt = []
        else:
            seltxt = self.fsnames[0]
            arseltxt = self.fsnames
        self.fscb = wx.ComboBox(self, -1, seltxt, size=(100, -1), choices=arseltxt, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        if self.nofixedstars:
            self.fscb.Enable(False)
        gsizer.Add(self.fscb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.fsorbstxt = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXFIXEDSTARORB), size=(50,
                                                                                                                                -1))
        self.fsorbstxt.SetMaxLength(4)
        if not self.nofixedstars:
            self.fsorbstxt.SetValue(str(self.fixedstars[self.fsnames[0]]))
        else:
            self.fsorbstxt.Enable(False)
        gsizer.Add(self.fsorbstxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        ID_All = wx.NewId()
        self.btnAll = wx.Button(self, ID_All, mtexts.txtsorbsdlg['All'], size=(100,
                                                                               -1))
        if self.nofixedstars:
            self.btnAll.Enable(False)
        gsizer.Add(self.btnAll, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.maxval = 6.0
        self.fsorbtxt = wx.TextCtrl(self, -1, '', validator=floatvalidator.FloatValidator(0.0, OrbsDlg.MAXFIXEDSTARORB), size=(50,
                                                                                                                               -1))
        self.fsorbtxt.SetMaxLength(4)
        if not self.nofixedstars:
            self.fsorbtxt.SetValue(str(self.options.fixedstarsorb))
        else:
            self.fsorbtxt.Enable(False)
        gsizer.Add(self.fsorbtxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sfsorbssizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vsizer.Add(sfsorbssizer, 0)
        mhsizer.Add(vsizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        mvsizer.Add(mhsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
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
        self.Bind(wx.EVT_COMBOBOX, self.onSelect, id=self.fscb.GetId())
        self.Bind(wx.EVT_BUTTON, self.onAll, id=ID_All)
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

    def onOK(self, event):
        if self.Validate():
            self.fixedstars[self.fsnames[self.prevselection]] = float(self.fsorbstxt.GetValue())
            self.Close()
            self.SetReturnCode(wx.ID_OK)

    def onSelect(self, evnt):
        if float(self.fsorbstxt.GetValue()) >= self.maxval:
            s = mtexts.txtsorbsdlg['RangeError'] + '%2.1f' % self.maxval
            dlgm = wx.MessageDialog(None, s, mtexts.txtsorbsdlg['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
        else:
            self.fixedstars[self.fsnames[self.prevselection]] = float(self.fsorbstxt.GetValue())
        idx = evnt.GetSelection()
        self.fsorbstxt.SetValue(str(self.fixedstars[self.fsnames[idx]]))
        self.prevselection = idx
        return

    def onAll(self, evnt):
        if float(self.fsorbtxt.GetValue()) >= self.maxval:
            s = mtexts.txtsorbsdlg['RangeError'] + '%2.1f' % self.maxval
            dlgm = wx.MessageDialog(None, s, mtexts.txtsorbsdlg['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        else:
            dlg = wx.MessageDialog(self, mtexts.txtscommon['AreYouSure'], mtexts.txtscommon['Confirm'], wx.YES_NO | wx.ICON_QUESTION)
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                for name in self.fsnames:
                    self.fixedstars[name] = float(self.fsorbtxt.GetValue())

                self.fsorbstxt.SetValue(str(float(self.fsorbtxt.GetValue())))
            self.fsorbtxt.SetValue(str(float(self.fsorbtxt.GetValue())))
            dlg.Destroy()
            return

    def fill(self, opts):
        for i in range(planets.Planets.PLANETS_NUM):
            self.arplsorbs[i].SetValue(str(opts.orbs[i]))

        for i in range(planets.Planets.PLANETS_NUM):
            self.arpplsorbs[i].SetValue(str(opts.orbsplanetspar[i]))

        self.cuspascmc.SetValue(str(opts.orbscuspAscMC))
        self.cuspinter.SetValue(str(opts.orbscuspH))
        self.daynight.SetValue(str(opts.daynightorb))

    def check(self, opts):
        changed = False
        for i in range(planets.Planets.PLANETS_NUM):
            if opts.orbs[i] != float(self.arplsorbs[i].GetValue()):
                opts.orbs[i] = float(self.arplsorbs[i].GetValue())
                changed = True

        for i in range(planets.Planets.PLANETS_NUM):
            if opts.orbsplanetspar[i] != float(self.arpplsorbs[i].GetValue()):
                opts.orbsplanetspar[i] = float(self.arpplsorbs[i].GetValue())
                changed = True

        if opts.orbscuspAscMC != float(self.cuspascmc.GetValue()):
            opts.orbscuspAscMC = float(self.cuspascmc.GetValue())
            changed = True
        if opts.orbscuspH != float(self.cuspinter.GetValue()):
            opts.orbscuspH = float(self.cuspinter.GetValue())
            changed = True
        if opts.daynightorb != float(self.daynight.GetValue()):
            opts.daynightorb = float(self.daynight.GetValue())
            changed = True
        if not self.nofixedstars:
            for k in self.fixedstars.keys():
                if self.fixedstars[k] != opts.fixedstars[k]:
                    opts.fixedstars[k] = self.fixedstars[k]
                    changed = True

        return changed
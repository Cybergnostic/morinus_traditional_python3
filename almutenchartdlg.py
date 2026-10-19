# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import intvalidator
import mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class AlmutenChartDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtsalmutenchartdlg['AlmutenOfTheChart'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sessential = wx.StaticBox(self, label=mtexts.txtsalmutenchartdlg['Essential'])
        essentialsizer = wx.StaticBoxSizer(self.sessential, wx.VERTICAL)
        self.stype = wx.StaticBox(self, label=mtexts.txtsalmutenchartdlg['Triplicities'])
        typesizer = wx.StaticBoxSizer(self.stype, wx.VERTICAL)
        self.onetriprb = wx.RadioButton(self, -1, mtexts.txtsalmutenchartdlg['OneRuler'], style=wx.RB_GROUP)
        typesizer.Add(self.onetriprb, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.threetriprb = wx.RadioButton(self, -1, mtexts.txtsalmutenchartdlg['AllThree'])
        typesizer.Add(self.threetriprb, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        essentialsizer.Add(typesizer, 0, wx.GROW | wx.ALL, 5)
        self.sorb = wx.StaticBox(self, label='')
        orbsizer = wx.StaticBoxSizer(self.sorb, wx.VERTICAL)
        self.useorb = wx.CheckBox(self, -1, mtexts.txtsalmutenchartdlg['UseDayNightOrbAlmutens'])
        orbsizer.Add(self.useorb, 0, wx.ALL, 5)
        essentialsizer.Add(orbsizer, 0, wx.GROW | wx.LEFT | wx.RIGHT, 5)
        self.sscores = wx.StaticBox(self, label=mtexts.txtsalmutenchartdlg['RulershipScores'])
        scoressizer = wx.StaticBoxSizer(self.sscores, wx.VERTICAL)
        gsizer = wx.GridSizer(0, 2, 0, 0)
        label = wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['Domicile'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.domicil = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 5), size=(40,
                                                                                                  -1))
        gsizer.Add(self.domicil, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.domicil.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanFive'])
        self.domicil.SetMaxLength(1)
        label = wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['Exaltation'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.exal = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 5), size=(40,
                                                                                               -1))
        gsizer.Add(self.exal, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.exal.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanFive'])
        self.exal.SetMaxLength(1)
        label = wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['Triplicity'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.tripl = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 5), size=(40,
                                                                                                -1))
        gsizer.Add(self.tripl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.tripl.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanFive'])
        self.tripl.SetMaxLength(1)
        label = wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['Term'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.term = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 5), size=(40,
                                                                                               -1))
        gsizer.Add(self.term, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.term.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanFive'])
        self.term.SetMaxLength(1)
        label = wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['Decan'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.decan = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 5), size=(40,
                                                                                                -1))
        gsizer.Add(self.decan, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.decan.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanFive'])
        self.decan.SetMaxLength(1)
        scoressizer.Add(gsizer, 0, wx.ALL, 5)
        essentialsizer.Add(scoressizer, 1, wx.GROW | wx.ALL, 5)
        mhsizer.Add(essentialsizer, 0, wx.GROW | wx.ALL, 5)
        self.saccidental = wx.StaticBox(self, label=mtexts.txtsalmutenchartdlg['Accidental'])
        accidentalsizer = wx.StaticBoxSizer(self.saccidental, wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.useaccidental = wx.CheckBox(self, -1, mtexts.txtsalmutenchartdlg['Use'])
        vsizer.Add(self.useaccidental, 0, wx.ALL, 5)
        self.shouses = wx.StaticBox(self, label=mtexts.txtsalmutenchartdlg['HouseScores'])
        housessizer = wx.StaticBoxSizer(self.shouses, wx.HORIZONTAL)
        self.houselabels = []
        gsizer = wx.GridSizer(0, 2, 0, 0)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC1'] + ':'))
        gsizer.Add(self.houselabels[0], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc1 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                               -1))
        gsizer.Add(self.hc1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc1.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc1.SetMaxLength(2)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC2'] + ':'))
        gsizer.Add(self.houselabels[1], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc2 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                               -1))
        gsizer.Add(self.hc2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc2.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc2.SetMaxLength(2)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC3'] + ':'))
        gsizer.Add(self.houselabels[2], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc3 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                               -1))
        gsizer.Add(self.hc3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc3.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc3.SetMaxLength(2)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC4'] + ':'))
        gsizer.Add(self.houselabels[3], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc4 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                               -1))
        gsizer.Add(self.hc4, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc4.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc4.SetMaxLength(2)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC5'] + ':'))
        gsizer.Add(self.houselabels[4], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc5 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                               -1))
        gsizer.Add(self.hc5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc5.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc5.SetMaxLength(2)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC6'] + ':'))
        gsizer.Add(self.houselabels[5], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc6 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                               -1))
        gsizer.Add(self.hc6, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc6.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc6.SetMaxLength(2)
        housessizer.Add(gsizer, 0, wx.ALL, 5)
        gsizer = wx.GridSizer(0, 2, 0, 0)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC7'] + ':'))
        gsizer.Add(self.houselabels[6], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc7 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                               -1))
        gsizer.Add(self.hc7, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc7.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc7.SetMaxLength(2)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC8'] + ':'))
        gsizer.Add(self.houselabels[7], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc8 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                               -1))
        gsizer.Add(self.hc8, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc8.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc8.SetMaxLength(2)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC9'] + ':'))
        gsizer.Add(self.houselabels[8], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc9 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                               -1))
        gsizer.Add(self.hc9, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc9.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc9.SetMaxLength(2)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC10'] + ':'))
        gsizer.Add(self.houselabels[9], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc10 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                                -1))
        gsizer.Add(self.hc10, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc10.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc10.SetMaxLength(2)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC11'] + ':'))
        gsizer.Add(self.houselabels[10], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc11 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                                -1))
        gsizer.Add(self.hc11, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc11.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc11.SetMaxLength(2)
        self.houselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['HC12'] + ':'))
        gsizer.Add(self.houselabels[11], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc12 = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                                -1))
        gsizer.Add(self.hc12, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hc12.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanTwelve'])
        self.hc12.SetMaxLength(2)
        housessizer.Add(gsizer, 0, wx.ALL, 5)
        vsizer.Add(housessizer, 0, wx.ALL, 5)
        accidentalsizer.Add(vsizer, 0, wx.ALL, 5)
        self.sphase = wx.StaticBox(self, label=mtexts.txtsalmutenchartdlg['SunPhaseScores'])
        phasessizer = wx.StaticBoxSizer(self.sphase, wx.HORIZONTAL)
        self.phaselabels = []
        gsizer = wx.GridSizer(0, 2, 0, 0)
        self.phaselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['Strong'] + ':'))
        gsizer.Add(self.phaselabels[0], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.strong = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 5), size=(40,
                                                                                                 -1))
        gsizer.Add(self.strong, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.strong.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanFive'])
        self.strong.SetMaxLength(1)
        self.phaselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['Medium'] + ':'))
        gsizer.Add(self.phaselabels[1], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.medium = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 5), size=(40,
                                                                                                 -1))
        gsizer.Add(self.medium, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.medium.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanFive'])
        self.medium.SetMaxLength(1)
        self.phaselabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['Weak'] + ':'))
        gsizer.Add(self.phaselabels[2], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.weak = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 5), size=(40,
                                                                                               -1))
        gsizer.Add(self.weak, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.weak.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanFive'])
        self.weak.SetMaxLength(1)
        phasessizer.Add(gsizer, 0, wx.ALL, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(phasessizer, 0, wx.ALL, 0)
        self.sdayhour = wx.StaticBox(self, label=mtexts.txtsalmutenchartdlg['RulerScores'])
        dayhoursizer = wx.StaticBoxSizer(self.sdayhour, wx.HORIZONTAL)
        self.dayhourlabels = []
        gsizer = wx.GridSizer(0, 2, 0, 0)
        self.dayhourlabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['Day'] + ':'))
        gsizer.Add(self.dayhourlabels[0], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.dayruler = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 10), size=(40,
                                                                                                    -1))
        gsizer.Add(self.dayruler, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.dayruler.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanNine'])
        self.dayruler.SetMaxLength(1)
        self.dayhourlabels.append(wx.StaticText(self, -1, mtexts.txtsalmutenchartdlg['Hour'] + ':'))
        gsizer.Add(self.dayhourlabels[1], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hourruler = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 10), size=(40,
                                                                                                     -1))
        gsizer.Add(self.hourruler, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.hourruler.SetHelpText(mtexts.txtsalmutenchartdlg['HelpLessThanNine'])
        self.hourruler.SetMaxLength(1)
        dayhoursizer.Add(gsizer, 0, wx.ALL, 5)
        vsizer.Add(dayhoursizer, 1, wx.GROW | wx.ALL, 0)
        accidentalsizer.Add(vsizer, 1, wx.GROW | wx.RIGHT | wx.BOTTOM, 5)
        mhsizer.Add(accidentalsizer, 0, wx.GROW | wx.ALL, 5)
        self.useexaltation = wx.CheckBox(self, -1, mtexts.txtsalmutenchartdlg['MercuryInVirgo'])
        mvsizer.Add(mhsizer, 0, wx.ALL, 5)
        mvsizer.Add(self.useexaltation, 0, wx.ALL, 5)
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
        self.Bind(wx.EVT_RADIOBUTTON, self.onOneTrip, id=self.onetriprb.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.onThreeTrip, id=self.threetriprb.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.onUseAccidental, id=self.useaccidental.GetId())
        btnOk.SetFocus()

    def onOneTrip(self, event):
        self.useorb.Enable(True)

    def onThreeTrip(self, event):
        self.useorb.Enable(False)

    def onUseAccidental(self, event):
        val = self.useaccidental.GetValue()
        self.enableAccidentals(val)

    def enableAccidentals(self, val):
        self.shouses.Enable(val)
        for label in self.houselabels:
            label.Enable(val)

        ar = (self.hc1, self.hc2, self.hc3, self.hc4, self.hc5, self.hc6, self.hc7, self.hc8, self.hc9, self.hc10, self.hc11, self.hc12)
        num = len(ar)
        for i in range(num):
            ar[i].Enable(val)

        for label in self.phaselabels:
            label.Enable(val)

        ar = (self.strong, self.medium, self.weak)
        num = len(ar)
        for i in range(num):
            ar[i].Enable(val)

        self.sphase.Enable(val)
        for label in self.dayhourlabels:
            label.Enable(val)

        ar = (self.dayruler, self.hourruler)
        num = len(ar)
        for i in range(num):
            ar[i].Enable(val)

        self.sdayhour.Enable(val)

    def fill(self, opts):
        if opts.oneruler:
            self.onetriprb.SetValue(True)
        else:
            self.threetriprb.SetValue(True)
        self.useorb.SetValue(opts.usedaynightorb)
        ar = (
         self.domicil, self.exal, self.tripl, self.term, self.decan)
        num = len(ar)
        for i in range(num):
            ar[i].SetValue(str(opts.dignityscores[i]))

        self.useaccidental.SetValue(opts.useaccidental)
        ar = (
         self.hc1, self.hc2, self.hc3, self.hc4, self.hc5, self.hc6, self.hc7, self.hc8, self.hc9, self.hc10, self.hc11, self.hc12)
        num = len(ar)
        for i in range(num):
            ar[i].SetValue(str(opts.housescores[i]))

        ar = (self.strong, self.medium, self.weak)
        num = len(ar)
        for i in range(num):
            ar[i].SetValue(str(opts.sunphases[i]))

        ar = (self.dayruler, self.hourruler)
        num = len(ar)
        for i in range(num):
            ar[i].SetValue(str(opts.dayhourscores[i]))

        if not opts.oneruler:
            self.useorb.Enable(False)
        if not opts.useaccidental:
            self.enableAccidentals(False)
        self.useexaltation.SetValue(opts.useexaltationmercury)

    def check(self, opts):
        changed = False
        if opts.oneruler != self.onetriprb.GetValue():
            opts.oneruler = self.onetriprb.GetValue()
            changed = True
        if opts.usedaynightorb != self.useorb.GetValue():
            opts.usedaynightorb = self.useorb.GetValue()
            changed = True
        ar = (self.domicil, self.exal, self.tripl, self.term, self.decan)
        num = len(ar)
        for i in range(num):
            if opts.dignityscores[i] != int(ar[i].GetValue()):
                opts.dignityscores[i] = int(ar[i].GetValue())
                changed = True

        if opts.useaccidental != self.useaccidental.GetValue():
            opts.useaccidental = self.useaccidental.GetValue()
            changed = True
        ar = (self.hc1, self.hc2, self.hc3, self.hc4, self.hc5, self.hc6, self.hc7, self.hc8, self.hc9, self.hc10, self.hc11, self.hc12)
        num = len(ar)
        for i in range(num):
            if opts.housescores[i] != int(ar[i].GetValue()):
                opts.housescores[i] = int(ar[i].GetValue())
                changed = True

        ar = (
         self.strong, self.medium, self.weak)
        num = len(ar)
        for i in range(num):
            if opts.sunphases[i] != int(ar[i].GetValue()):
                opts.sunphases[i] = int(ar[i].GetValue())
                changed = True

        ar = (
         self.dayruler, self.hourruler)
        num = len(ar)
        for i in range(num):
            if opts.dayhourscores[i] != int(ar[i].GetValue()):
                opts.dayhourscores[i] = int(ar[i].GetValue())
                changed = True

        if opts.useexaltationmercury != self.useexaltation.GetValue():
            opts.useexaltationmercury = self.useexaltation.GetValue()
            changed = True
        return changed
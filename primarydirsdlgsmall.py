# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import primdirs
import fixedstarspddlg
import userpddlg
import mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class PrimDirsDlgSmall(wx.Dialog):

    def __init__(self, parent, options, ephepath):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtsprimdirsdlg['PrimaryDirs'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        self.options = options
        self.ephepath = ephepath
        self.fsselections = self.options.pdfixedstarssel[:]
        self.userlons = options.pduserlon[:]
        self.userlats = options.pduserlat[:]
        self.southern = options.pdusersouthern
        self.user2lons = options.pduser2lon[:]
        self.user2lats = options.pduser2lat[:]
        self.southern2 = options.pduser2southern
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        stype = wx.StaticBox(self, label='')
        typesizer = wx.StaticBoxSizer(stype, wx.VERTICAL)
        self.placidiansemiarcrb = wx.RadioButton(self, -1, mtexts.txtsprimdirsdlg['PlacidianSemiArc'], style=wx.RB_GROUP)
        typesizer.Add(self.placidiansemiarcrb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.placidiansemiarcrb.SetHelpText(mtexts.txtsprimdirsdlg['HelpPlacidianSemiArc'])
        self.placidianutprb = wx.RadioButton(self, -1, mtexts.txtsprimdirsdlg['PlacidianUnderThePole'])
        typesizer.Add(self.placidianutprb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.placidianutprb.SetHelpText(mtexts.txtsprimdirsdlg['HelpPlacidianUnderThePole'])
        self.regiomontanrb = wx.RadioButton(self, -1, mtexts.txtsprimdirsdlg['Regiomontanian'])
        typesizer.Add(self.regiomontanrb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.regiomontanrb.SetHelpText(mtexts.txtsprimdirsdlg['HelpRegiomontanian'])
        self.Bind(wx.EVT_RADIOBUTTON, self.onPlacidian, id=self.placidiansemiarcrb.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.onPlacidianUTP, id=self.placidianutprb.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.onRegiomontan, id=self.regiomontanrb.GetId())
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(typesizer, 1, wx.GROW | wx.ALIGN_LEFT | wx.TOP, 2)
        vzodsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsprimdirsdlg['UseSZ'] + ':')
        vzodsizer.Add(label, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.szneitherrb = wx.RadioButton(self, -1, mtexts.txtsprimdirsdlg['SZNeither'], style=wx.RB_GROUP)
        self.szneitherrb.SetHelpText(mtexts.txtsprimdirsdlg['HelpSZNeither'])
        vzodsizer.Add(self.szneitherrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.szpromissorrb = wx.RadioButton(self, -1, mtexts.txtsprimdirsdlg['SZPromissor'])
        self.szpromissorrb.SetHelpText(mtexts.txtsprimdirsdlg['HelpSZPromissor'])
        vzodsizer.Add(self.szpromissorrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.szsignificatorrb = wx.RadioButton(self, -1, mtexts.txtsprimdirsdlg['SZSignificator'])
        self.szsignificatorrb.SetHelpText(mtexts.txtsprimdirsdlg['HelpSZSignificator'])
        vzodsizer.Add(self.szsignificatorrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.szbothrb = wx.RadioButton(self, -1, mtexts.txtsprimdirsdlg['SZBoth'])
        self.szbothrb.SetHelpText(mtexts.txtsprimdirsdlg['HelpSZBoth'])
        vzodsizer.Add(self.szbothrb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        hzodsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.szbianchinickb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['Bianchini'])
        hzodsizer.Add(self.szbianchinickb, 0, wx.ALIGN_LEFT | wx.LEFT, 20)
        vzodsizer.Add(hzodsizer, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        ssubtype = wx.StaticBox(self, label='')
        subtypesizer = wx.StaticBoxSizer(ssubtype, wx.VERTICAL)
        self.mundanerb = wx.RadioButton(self, -1, mtexts.txtsprimdirsdlg['Mundane'], style=wx.RB_GROUP)
        subtypesizer.Add(self.mundanerb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.mundanerb.SetHelpText(mtexts.txtsprimdirsdlg['HelpMundane'])
        self.zodiacalrb = wx.RadioButton(self, -1, mtexts.txtsprimdirsdlg['Zodiacal'])
        self.zodiacalrb.SetHelpText(mtexts.txtsprimdirsdlg['HelpZodiacal'])
        subtypesizer.Add(self.zodiacalrb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        subtypesizer.Add(vzodsizer, 0, wx.ALIGN_LEFT | wx.LEFT, 20)
        self.Bind(wx.EVT_RADIOBUTTON, self.onMundane, id=self.mundanerb.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.onZodiacal, id=self.zodiacalrb.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.onSZNeither, id=self.szneitherrb.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.onSZPromissor, id=self.szpromissorrb.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.onSZSignificator, id=self.szsignificatorrb.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.onSZBoth, id=self.szbothrb.GetId())
        vsizer.Add(subtypesizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.BOTTOM, 2)
        self.zodopt = wx.StaticBox(self, label=mtexts.txtsprimdirsdlg['ZodiacalOpts'])
        zodoptsizer = wx.StaticBoxSizer(self.zodopt, wx.VERTICAL)
        self.aspspromstosigsckb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['ZodAspsPromsToSigs1'])
        zodoptsizer.Add(self.aspspromstosigsckb, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.RIGHT, 2)
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        self.labelzodopt1 = wx.StaticText(self, -1, mtexts.txtsprimdirsdlg['ZodAspsPromsToSigs2'])
        vsubsizer.Add(self.labelzodopt1, 0, wx.ALIGN_LEFT | wx.LEFT, 30)
        zodoptsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.promstosigaspsckb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['ZodPromsToSigAsps1'])
        zodoptsizer.Add(self.promstosigaspsckb, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.RIGHT, 2)
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        self.labelzodopt2 = wx.StaticText(self, -1, mtexts.txtsprimdirsdlg['ZodPromsToSigAsps2'])
        vsubsizer.Add(self.labelzodopt2, 0, wx.ALIGN_LEFT | wx.LEFT, 30)
        zodoptsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.ascmchcsaspromsckb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['ZodAscMCHCsAsProms'])
        zodoptsizer.Add(self.ascmchcsaspromsckb, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.RIGHT, 2)
        vsizer.Add(zodoptsizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.BOTTOM, 2)
        mhsizer.Add(vsizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.LEFT, 0)
        sapply = wx.StaticBox(self, label='')
        applysizer = wx.StaticBoxSizer(sapply, wx.VERTICAL)
        fgsizer = wx.FlexGridSizer(0, 3, 0, 0)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsprimdirsdlg['Promissors'])
        vsizer.Add(label, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.promsaturnckb = wx.CheckBox(self, -1, mtexts.txtscommon['Saturn'])
        vsizer.Add(self.promsaturnckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.promjupiterckb = wx.CheckBox(self, -1, mtexts.txtscommon['Jupiter'])
        vsizer.Add(self.promjupiterckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.prommarsckb = wx.CheckBox(self, -1, mtexts.txtscommon['Mars'])
        vsizer.Add(self.prommarsckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.promsunckb = wx.CheckBox(self, -1, mtexts.txtscommon['Sun'])
        vsizer.Add(self.promsunckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.promvenusckb = wx.CheckBox(self, -1, mtexts.txtscommon['Venus'])
        vsizer.Add(self.promvenusckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.prommercuryckb = wx.CheckBox(self, -1, mtexts.txtscommon['Mercury'])
        vsizer.Add(self.prommercuryckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.prommoonckb = wx.CheckBox(self, -1, mtexts.txtscommon['Moon'])
        vsizer.Add(self.prommoonckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        self.secmotionckb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['SecondaryMotion'])
        vsubsizer.Add(self.secmotionckb, 0)
        self.secmotionitercb = wx.ComboBox(self, -1, mtexts.smiterList[0], size=(100,
                                                                                 -1), choices=mtexts.smiterList, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        vsubsizer.Add(self.secmotionitercb, 0)
        hsubsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.LEFT, 15)
        vsizer.Add(hsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.promanodeckb = wx.CheckBox(self, -1, mtexts.txtscommon['ANode'])
        vsizer.Add(self.promanodeckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.promdnodeckb = wx.CheckBox(self, -1, mtexts.txtscommon['DNode'])
        vsizer.Add(self.promdnodeckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.promantsckb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['Antiscia'])
        vsizer.Add(self.promantsckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.prommidpointsckb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['MidPoints'])
        vsizer.Add(self.prommidpointsckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.promlofckb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['LoF'])
        vsizer.Add(self.promlofckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.promtermsckb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['Terms'])
        vsizer.Add(self.promtermsckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.promfixedstarsckb = wx.CheckBox(self, -1, '')
        hsizer.Add(self.promfixedstarsckb, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        ID_FixedStars = wx.NewId()
        self.btnFixedStars = wx.Button(self, ID_FixedStars, mtexts.txtsprimdirsdlg['FixedStars'])
        if not options.pdfixedstars:
            self.btnFixedStars.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onFixedStars, id=ID_FixedStars)
        self.Bind(wx.EVT_CHECKBOX, self.onFixedStarsCheck, id=self.promfixedstarsckb.GetId())
        hsizer.Add(self.btnFixedStars, 0, wx.ALIGN_LEFT)
        vsizer.Add(hsizer, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.Bind(wx.EVT_CHECKBOX, self.onPromMoon, id=self.prommoonckb.GetId())
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.conjunctionckb = wx.CheckBox(self, -1, mtexts.txtscommon['Conjunction'])
        vsizer.Add(self.conjunctionckb, 0, wx.ALIGN_LEFT | wx.TOP, 20)
        self.sextilckb = wx.CheckBox(self, -1, mtexts.txtscommon['Sextile'])
        vsizer.Add(self.sextilckb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        self.quadratckb = wx.CheckBox(self, -1, mtexts.txtscommon['Square'])
        vsizer.Add(self.quadratckb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        self.trigonckb = wx.CheckBox(self, -1, mtexts.txtscommon['Trine'])
        vsizer.Add(self.trigonckb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        self.oppositionckb = wx.CheckBox(self, -1, mtexts.txtscommon['Opposition'])
        vsizer.Add(self.oppositionckb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        self.mundaneparckb = wx.CheckBox(self, -1, mtexts.txtscommon['Parallel'])
        vsizer.Add(self.mundaneparckb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        self.raptparckb = wx.CheckBox(self, -1, mtexts.txtscommon['RaptParallel'])
        vsizer.Add(self.raptparckb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        suser = wx.StaticBox(self, label=mtexts.txtsprimdirsdlg['Promissors'])
        usersizer = wx.StaticBoxSizer(suser, wx.VERTICAL)
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.userckb = wx.CheckBox(self, -1, '')
        hsizer.Add(self.userckb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        ID_User = wx.NewId()
        self.btnUser = wx.Button(self, ID_User, mtexts.txtscommon['User'])
        self.Bind(wx.EVT_BUTTON, self.onUser, id=ID_User)
        self.Bind(wx.EVT_CHECKBOX, self.onUserCheck, id=self.userckb.GetId())
        hsizer.Add(self.btnUser, 0, wx.ALIGN_LEFT)
        vsubsizer.Add(hsizer, 0, wx.ALIGN_LEFT | wx.TOP | wx.BOTTOM, 2)
        usersizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        vsizer.Add(usersizer, 0, wx.ALIGN_LEFT | wx.TOP, 10)
        suser2 = wx.StaticBox(self, label=mtexts.txtsprimdirsdlg['Significators'])
        user2sizer = wx.StaticBoxSizer(suser2, wx.VERTICAL)
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.user2ckb = wx.CheckBox(self, -1, '')
        hsizer.Add(self.user2ckb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        ID_User2 = wx.NewId()
        self.btnUser2 = wx.Button(self, ID_User2, mtexts.txtscommon['User'])
        self.Bind(wx.EVT_BUTTON, self.onUser2, id=ID_User2)
        self.Bind(wx.EVT_CHECKBOX, self.onUser2Check, id=self.user2ckb.GetId())
        hsizer.Add(self.btnUser2, 0, wx.ALIGN_LEFT)
        vsubsizer.Add(hsizer, 0, wx.ALIGN_LEFT | wx.TOP | wx.BOTTOM, 2)
        user2sizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        vsizer.Add(user2sizer, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsprimdirsdlg['Significators'])
        vsizer.Add(label, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigascckb = wx.CheckBox(self, -1, 'Asc')
        vsizer.Add(self.sigascckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigmcckb = wx.CheckBox(self, -1, 'MC')
        vsizer.Add(self.sigmcckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sighousecuspsckb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['HouseCusps'])
        vsizer.Add(self.sighousecuspsckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigsaturnckb = wx.CheckBox(self, -1, mtexts.txtscommon['Saturn'])
        vsizer.Add(self.sigsaturnckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigjupiterckb = wx.CheckBox(self, -1, mtexts.txtscommon['Jupiter'])
        vsizer.Add(self.sigjupiterckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigmarsckb = wx.CheckBox(self, -1, mtexts.txtscommon['Mars'])
        vsizer.Add(self.sigmarsckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigsunckb = wx.CheckBox(self, -1, mtexts.txtscommon['Sun'])
        vsizer.Add(self.sigsunckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigvenusckb = wx.CheckBox(self, -1, mtexts.txtscommon['Venus'])
        vsizer.Add(self.sigvenusckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigmercuryckb = wx.CheckBox(self, -1, mtexts.txtscommon['Mercury'])
        vsizer.Add(self.sigmercuryckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigmoonckb = wx.CheckBox(self, -1, mtexts.txtscommon['Moon'])
        vsizer.Add(self.sigmoonckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.siganodeckb = wx.CheckBox(self, -1, mtexts.txtscommon['ANode'])
        vsizer.Add(self.siganodeckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigdnodeckb = wx.CheckBox(self, -1, mtexts.txtscommon['DNode'])
        vsizer.Add(self.sigdnodeckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.siglofckb = wx.CheckBox(self, -1, mtexts.txtsprimdirsdlg['LoF'])
        vsizer.Add(self.siglofckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.sigsyzckb = wx.CheckBox(self, -1, mtexts.txtscommon['Syzygy'])
        vsizer.Add(self.sigsyzckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        applysizer.Add(fgsizer, 0, wx.ALIGN_LEFT, 2)
        mhsizer.Add(applysizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 2)
        mvsizer.Add(mhsizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.LEFT, 2)
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
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, 2)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        btnOk.SetFocus()

    def onPlacidian(self, event):
        self.mundanerb.Enable(True)
        mun = self.mundanerb.GetValue()
        bianchini = False
        if not mun:
            if self.szbothrb.GetValue():
                bianchini = True
        if mun:
            self.enableSubZods(False, bianchini)
            self.enableZodOpts(False)
            self.enableZods(False)
            self.siglofckb.Enable(True)
            self.raptparckb.Enable(True)

    def onPlacidianUTP(self, event):
        self.mundanerb.Enable(False)
        self.zodiacalrb.SetValue(True)
        bianchini = False
        if self.szbothrb.GetValue():
            bianchini = True
        self.enableSubZods(True, bianchini)
        self.enableZodOpts(True)
        self.enableZods(True)
        self.siglofckb.Enable(True)
        self.raptparckb.Enable(False)

    def onRegiomontan(self, event):
        self.mundanerb.Enable(True)
        mun = self.mundanerb.GetValue()
        self.siglofckb.Enable(not mun)
        bianchini = False
        if not mun:
            if self.szbothrb.GetValue():
                bianchini = True
        if mun:
            self.enableSubZods(False, bianchini)
            self.enableZodOpts(False)
            self.enableZods(False)
            self.siglofckb.Enable(True)
        self.raptparckb.Enable(False)

    def onMundane(self, event):
        self.enableSubZods(False)
        self.enableZodOpts(False)
        self.enableZods(False)
        plac = self.placidiansemiarcrb.GetValue()
        self.siglofckb.Enable(plac)
        self.raptparckb.Enable(plac)

    def onZodiacal(self, event):
        bianchini = False
        if self.szbothrb.GetValue():
            bianchini = True
        self.enableSubZods(True, bianchini)
        self.enableZodOpts(True)
        self.enableZods(True)
        self.siglofckb.Enable(True)
        self.raptparckb.Enable(False)

    def onSZNeither(self, event):
        self.szbianchinickb.Enable(False)

    def onSZPromissor(self, event):
        self.szbianchinickb.Enable(False)
        self.szbianchinickb.SetValue(False)

    def onSZSignificator(self, event):
        self.szbianchinickb.Enable(False)
        self.szbianchinickb.SetValue(False)

    def onSZBoth(self, event):
        self.szbianchinickb.Enable(True)

    def onPromMoon(self, event):
        self.secmotionckb.Enable(self.prommoonckb.GetValue())
        self.secmotionitercb.Enable(self.prommoonckb.GetValue())

    def enableSubZods(self, val, bianchini=False):
        self.szneitherrb.Enable(val)
        self.szpromissorrb.Enable(val)
        self.szsignificatorrb.Enable(val)
        self.szbothrb.Enable(val)
        self.szbianchinickb.Enable(bianchini)

    def enableZodOpts(self, val):
        self.zodopt.Enable(val)
        self.aspspromstosigsckb.Enable(val)
        self.promstosigaspsckb.Enable(val)
        self.ascmchcsaspromsckb.Enable(val)
        self.labelzodopt1.Enable(val)
        self.labelzodopt2.Enable(val)

    def enableZods(self, val):
        self.promlofckb.Enable(val)
        self.promtermsckb.Enable(val)
        self.promfixedstarsckb.Enable(val)
        self.sigsyzckb.Enable(val)
        if val:
            if self.promfixedstarsckb.GetValue():
                self.btnFixedStars.Enable(True)
            else:
                self.btnFixedStars.Enable(False)
        else:
            self.btnFixedStars.Enable(False)

    def onFixedStarsCheck(self, event):
        self.btnFixedStars.Enable(self.promfixedstarsckb.GetValue())

    def onFixedStars(self, event):
        if not self.parent.checkFixedStars():
            return
        if len(self.options.fixedstars) == 0:
            dlgm = wx.MessageDialog(self, mtexts.txtscommon['NoSelFixedStars'], '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        dlg = fixedstarspddlg.FixedStarsPDDlg(self, self.options, self.fsselections, self.ephepath)
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            sels = dlg.getSelections()
            self.fsselections = sels[:]
        dlg.Destroy()

    def onUserCheck(self, event):
        self.btnUser.Enable(self.userckb.GetValue())

    def onUser(self, event):
        dlg = userpddlg.UserPDDlg(self, mtexts.txtscommon['User'])
        dlg.CenterOnParent()
        dlg.initialize(self.userlons, self.userlats, self.southern)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.userlons, self.userlats, self.southern):
                self.userlons[0] = int(dlg.londeg.GetValue())
                self.userlons[1] = int(dlg.lonmin.GetValue())
                self.userlons[2] = int(dlg.lonsec.GetValue())
                self.userlats[0] = int(dlg.latdeg.GetValue())
                self.userlats[1] = int(dlg.latmin.GetValue())
                self.userlats[2] = int(dlg.latsec.GetValue())
                self.southern = dlg.southernckb.GetValue()
        dlg.Destroy()

    def onUser2Check(self, event):
        self.btnUser2.Enable(self.user2ckb.GetValue())

    def onUser2(self, event):
        dlg = userpddlg.UserPDDlg(self, mtexts.txtscommon['User'])
        dlg.CenterOnParent()
        dlg.initialize(self.user2lons, self.user2lats, self.southern2)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.user2lons, self.user2lats, self.southern2):
                self.user2lons[0] = int(dlg.londeg.GetValue())
                self.user2lons[1] = int(dlg.lonmin.GetValue())
                self.user2lons[2] = int(dlg.lonsec.GetValue())
                self.user2lats[0] = int(dlg.latdeg.GetValue())
                self.user2lats[1] = int(dlg.latmin.GetValue())
                self.user2lats[2] = int(dlg.latsec.GetValue())
                self.southern2 = dlg.southernckb.GetValue()
        dlg.Destroy()

    def fill(self, options):
        self.promfixedstarsckb.SetValue(options.pdfixedstars)
        self.secmotionckb.SetValue(options.pdsecmotion)
        self.secmotionitercb.SetStringSelection(mtexts.smiterList[options.pdsecmotioniter])
        ckbs = [
         self.sigascckb, self.sigmcckb]
        for i in range(len(ckbs)):
            ckbs[i].SetValue(options.sigascmc[i])

        self.sighousecuspsckb.SetValue(options.sighouses)
        ckbs = [
         self.sigsaturnckb, self.sigjupiterckb, self.sigmarsckb, self.sigsunckb, self.sigvenusckb, self.sigmercuryckb, self.sigmoonckb, self.siganodeckb, self.sigdnodeckb]
        for i in range(len(ckbs)):
            ckbs[i].SetValue(options.sigplanets[i])

        self.siglofckb.SetValue(options.pdlof[1])
        self.sigsyzckb.SetValue(options.pdsyzygy)
        ckbs = [
         self.promsaturnckb, self.promjupiterckb, self.prommarsckb, self.promsunckb, self.promvenusckb, self.prommercuryckb, self.prommoonckb, self.promanodeckb, self.promdnodeckb]
        for i in range(len(ckbs)):
            ckbs[i].SetValue(options.promplanets[i])

        self.promlofckb.SetValue(options.pdlof[0])
        self.promtermsckb.SetValue(options.pdterms)
        self.promantsckb.SetValue(options.pdantiscia)
        self.prommidpointsckb.SetValue(options.pdmidpoints)
        self.secmotionckb.Enable(self.prommoonckb.GetValue())
        self.secmotionitercb.Enable(self.prommoonckb.GetValue())
        ckbs = [
         self.conjunctionckb, self.sextilckb, self.quadratckb, self.trigonckb, self.oppositionckb]
        for i in range(len(ckbs)):
            ckbs[i].SetValue(options.pdaspects[i])

        ckbs = [self.mundaneparckb, self.raptparckb]
        for i in range(len(ckbs)):
            ckbs[i].SetValue(options.pdparallels[i])

        self.userckb.SetValue(options.pduser)
        self.btnUser.Enable(options.pduser)
        self.user2ckb.SetValue(options.pduser2)
        self.btnUser2.Enable(options.pduser2)
        if options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC:
            self.placidiansemiarcrb.SetValue(True)
        else:
            if options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
                self.placidianutprb.SetValue(True)
                self.mundanerb.Enable(False)
            elif options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
                self.regiomontanrb.SetValue(True)
            elif options.primarydir == primdirs.PrimDirs.CAMPANIAN:
                self.placidiansemiarcrb.SetValue(True)
        if options.subprimarydir == primdirs.PrimDirs.MUNDANE:
            self.mundanerb.SetValue(True)
            self.enableSubZods(False, False)
            self.enableZodOpts(False)
            self.enableZods(False)
            if options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC:
                self.raptparckb.Enable(True)
                self.siglofckb.Enable(True)
            else:
                self.siglofckb.Enable(False)
                self.raptparckb.Enable(False)
        elif options.subprimarydir == primdirs.PrimDirs.ZODIACAL:
            self.zodiacalrb.SetValue(True)
            self.enableZods(True)
            self.enableZodOpts(True)
            self.raptparckb.Enable(False)
            self.siglofckb.Enable(True)
        elif options.subprimarydir == primdirs.PrimDirs.BOTH:
            self.enableZods(True)
            self.enableZodOpts(True)
            if options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC:
                self.raptparckb.Enable(True)
            else:
                self.raptparckb.Enable(False)
            self.siglofckb.Enable(True)
        if options.subzodiacal == primdirs.PrimDirs.SZNEITHER:
            self.szneitherrb.SetValue(True)
            self.szbianchinickb.Enable(False)
        elif options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR:
            self.szpromissorrb.SetValue(True)
            self.szbianchinickb.Enable(False)
        elif options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR:
            self.szsignificatorrb.SetValue(True)
            self.szbianchinickb.Enable(False)
        elif options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            self.szbothrb.SetValue(True)
        self.szbianchinickb.SetValue(options.bianchini)
        ckbs = [
         self.aspspromstosigsckb, self.promstosigaspsckb]
        for i in range(len(ckbs)):
            ckbs[i].SetValue(options.zodpromsigasps[i])

        self.ascmchcsaspromsckb.SetValue(options.ascmchcsasproms)

    def check(self, options):
        changed = False
        changedU1 = False
        changedU2 = False
        if self.placidiansemiarcrb.GetValue():
            if options.primarydir != primdirs.PrimDirs.PLACIDIANSEMIARC:
                options.primarydir = primdirs.PrimDirs.PLACIDIANSEMIARC
                changed = True
        elif self.placidianutprb.GetValue():
            if options.primarydir != primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
                options.primarydir = primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE
                changed = True
        elif self.regiomontanrb.GetValue():
            if options.primarydir != primdirs.PrimDirs.REGIOMONTAN:
                options.primarydir = primdirs.PrimDirs.REGIOMONTAN
                changed = True
        if self.mundanerb.GetValue():
            if options.subprimarydir != primdirs.PrimDirs.MUNDANE:
                options.subprimarydir = primdirs.PrimDirs.MUNDANE
                changed = True
        else:
            if self.zodiacalrb.GetValue():
                if options.subprimarydir != primdirs.PrimDirs.ZODIACAL:
                    options.subprimarydir = primdirs.PrimDirs.ZODIACAL
                    changed = True
        if self.szneitherrb.GetValue():
            if options.subzodiacal != primdirs.PrimDirs.SZNEITHER:
                options.subzodiacal = primdirs.PrimDirs.SZNEITHER
                changed = True
        else:
            if self.szpromissorrb.GetValue():
                if options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR:
                    options.subzodiacal = primdirs.PrimDirs.SZPROMISSOR
                    changed = True
            else:
                if self.szsignificatorrb.GetValue():
                    if options.subzodiacal != primdirs.PrimDirs.SZSIGNIFICATOR:
                        options.subzodiacal = primdirs.PrimDirs.SZSIGNIFICATOR
                        changed = True
                else:
                    if self.szbothrb.GetValue():
                        if options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                            options.subzodiacal = primdirs.PrimDirs.SZBOTH
                            changed = True
        if options.bianchini != self.szbianchinickb.GetValue():
            options.bianchini = self.szbianchinickb.GetValue()
            changed = True
        ckbs = [self.aspspromstosigsckb, self.promstosigaspsckb]
        for i in range(len(ckbs)):
            if ckbs[i].GetValue() != options.zodpromsigasps[i]:
                options.zodpromsigasps[i] = ckbs[i].GetValue()
                changed = True

        if self.ascmchcsaspromsckb.GetValue() != options.ascmchcsasproms:
            options.ascmchcsasproms = self.ascmchcsaspromsckb.GetValue()
            changed = True
        ckbs = [self.sigascckb, self.sigmcckb]
        for i in range(len(ckbs)):
            if ckbs[i].GetValue() != options.sigascmc[i]:
                options.sigascmc[i] = ckbs[i].GetValue()
                changed = True

        if self.sighousecuspsckb.GetValue() != options.sighouses:
            options.sighouses = self.sighousecuspsckb.GetValue()
            changed = True
        ckbs = [self.sigsaturnckb, self.sigjupiterckb, self.sigmarsckb, self.sigsunckb, self.sigvenusckb, self.sigmercuryckb, self.sigmoonckb, self.siganodeckb, self.sigdnodeckb]
        for i in range(len(ckbs)):
            if ckbs[i].GetValue() != options.sigplanets[i]:
                options.sigplanets[i] = ckbs[i].GetValue()
                changed = True

        if options.pdlof[1] != self.siglofckb.GetValue():
            options.pdlof[1] = self.siglofckb.GetValue()
            changed = True
        if options.pdsyzygy != self.sigsyzckb.GetValue():
            options.pdsyzygy = self.sigsyzckb.GetValue()
            changed = True
        ckbs = [self.promsaturnckb, self.promjupiterckb, self.prommarsckb, self.promsunckb, self.promvenusckb, self.prommercuryckb, self.prommoonckb, self.promanodeckb, self.promdnodeckb]
        for i in range(len(ckbs)):
            if ckbs[i].GetValue() != options.promplanets[i]:
                options.promplanets[i] = ckbs[i].GetValue()
                changed = True

        if self.prommidpointsckb.GetValue() != options.pdmidpoints:
            options.pdmidpoints = self.prommidpointsckb.GetValue()
            changed = True
        if options.pdantiscia != self.promantsckb.GetValue():
            options.pdantiscia = self.promantsckb.GetValue()
            changed = True
        if options.pdlof[0] != self.promlofckb.GetValue():
            options.pdlof[0] = self.promlofckb.GetValue()
            changed = True
        if options.pdterms != self.promtermsckb.GetValue():
            options.pdterms = self.promtermsckb.GetValue()
            changed = True
        ckbs = [self.conjunctionckb, self.sextilckb, self.quadratckb, self.trigonckb, self.oppositionckb]
        for i in range(len(ckbs)):
            if ckbs[i].GetValue() != options.pdaspects[i]:
                options.pdaspects[i] = ckbs[i].GetValue()
                changed = True

        ckbs = [
         self.mundaneparckb, self.raptparckb]
        for i in range(len(ckbs)):
            if ckbs[i].GetValue() != options.pdparallels[i]:
                options.pdparallels[i] = ckbs[i].GetValue()
                changed = True

        if self.secmotionckb.GetValue() != options.pdsecmotion:
            options.pdsecmotion = self.secmotionckb.GetValue()
            changed = True
        if self.secmotionitercb.GetCurrentSelection() != options.pdsecmotioniter:
            options.pdsecmotioniter = self.secmotionitercb.GetCurrentSelection()
            changed = True
        if self.promfixedstarsckb.GetValue() != options.pdfixedstars:
            options.pdfixedstars = self.promfixedstarsckb.GetValue()
            changed = True
        num = len(self.options.pdfixedstarssel)
        for i in range(num):
            if self.fsselections[i] != self.options.pdfixedstarssel[i]:
                self.options.pdfixedstarssel[i] = self.fsselections[i]
                changed = True

        if self.userckb.GetValue() != options.pduser:
            options.pduser = self.userckb.GetValue()
            changed = True
            changedU1 = True
        for i in range(3):
            if options.pduserlon[i] != self.userlons[i]:
                options.pduserlon[i] = self.userlons[i]
                changed = True
                changedU1 = True
            if options.pduserlat[i] != self.userlats[i]:
                options.pduserlat[i] = self.userlats[i]
                changed = True
                changedU1 = True

        if self.options.pdusersouthern != self.southern:
            options.pdusersouthern = self.southern
            changed = True
            changedU1 = True
        if self.user2ckb.GetValue() != options.pduser2:
            options.pduser2 = self.user2ckb.GetValue()
            changed = True
            changedU2 = True
        for i in range(3):
            if options.pduser2lon[i] != self.user2lons[i]:
                options.pduser2lon[i] = self.user2lons[i]
                changed = True
                changedU2 = True
            if options.pduser2lat[i] != self.user2lats[i]:
                options.pduser2lat[i] = self.user2lats[i]
                changed = True
                changedU2 = True

        if self.options.pduser2southern != self.southern2:
            options.pduser2southern = self.southern2
            changed = True
            changedU2 = True
        return (changed, changedU1, changedU2)
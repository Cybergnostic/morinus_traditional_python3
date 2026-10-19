# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import planets
import placspec
import regiospec
import chart
import mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class Appearance2Dlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtsappearance2dlg['Appearance2'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        placidian = wx.StaticBox(self, label=mtexts.txtsappearance2dlg['Placidian'])
        placidiansizer = wx.StaticBoxSizer(placidian, wx.VERTICAL)
        self.longckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Longitude'])
        placidiansizer.Add(self.longckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.latckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Latitude'])
        placidiansizer.Add(self.latckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.rectascckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Rectascension'])
        placidiansizer.Add(self.rectascckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.declckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Declination'])
        placidiansizer.Add(self.declckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.ascdifflatckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['AscDiffLat'])
        placidiansizer.Add(self.ascdifflatckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.semiarcusckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Semiarcus'])
        placidiansizer.Add(self.semiarcusckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.meridiandistckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Meridiandist'])
        placidiansizer.Add(self.meridiandistckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.horizondistckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Horizondist'])
        placidiansizer.Add(self.horizondistckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.temporalhourckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['TemporalHour'])
        placidiansizer.Add(self.temporalhourckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.hourlydistckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['HourlyDist'])
        placidiansizer.Add(self.hourlydistckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.pmpckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['PMP'])
        self.pmpckb.SetHelpText(mtexts.txtsappearance2dlg['HelpPMP'])
        placidiansizer.Add(self.pmpckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.ascdiffpoleckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['AscDiffPole'])
        placidiansizer.Add(self.ascdiffpoleckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.poleheightckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['PoleHeight'])
        placidiansizer.Add(self.poleheightckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.ascdescoblckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['AODO'])
        placidiansizer.Add(self.ascdescoblckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        mhsizer.Add(placidiansizer, 0, wx.ALIGN_TOP | wx.RIGHT, 5)
        regiomontan = wx.StaticBox(self, label=mtexts.txtsappearance2dlg['Regiomontanian'])
        regiomontansizer = wx.StaticBoxSizer(regiomontan, wx.VERTICAL)
        self.reglongckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Longitude'])
        regiomontansizer.Add(self.reglongckb, 0, wx.ALIGN_LEFT | wx.ALL | wx.TOP, 2)
        self.reglatckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Latitude'])
        regiomontansizer.Add(self.reglatckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.regrectascckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Rectascension'])
        regiomontansizer.Add(self.regrectascckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.regdeclckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Declination'])
        regiomontansizer.Add(self.regdeclckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.regmeridiandistckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Meridiandist'])
        regiomontansizer.Add(self.regmeridiandistckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.reghorizondistckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Horizondist'])
        regiomontansizer.Add(self.reghorizondistckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.regzdckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['ZD'])
        self.regzdckb.SetHelpText(mtexts.txtsappearance2dlg['HelpZD'])
        regiomontansizer.Add(self.regzdckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.regpoleckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Pole'])
        regiomontansizer.Add(self.regpoleckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.regqckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['Q'])
        self.regqckb.SetHelpText(mtexts.txtsappearance2dlg['HelpQ'])
        regiomontansizer.Add(self.regqckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.regwckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['WReg'])
        self.regwckb.SetHelpText(mtexts.txtsappearance2dlg['HelpW'])
        regiomontansizer.Add(self.regwckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        self.cmpckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['CMP'])
        self.cmpckb.SetHelpText(mtexts.txtsappearance2dlg['HelpCMP'])
        regiomontansizer.Add(self.cmpckb, 0, wx.ALIGN_LEFT | wx.ALL, 2)
        mhsizer.Add(regiomontansizer, 1, wx.GROW | wx.RIGHT, 5)
        mvsizer.Add(mhsizer, 0, wx.GROW | wx.ALL, 5)
        ra = wx.StaticBox(self, label=mtexts.txtsappearance2dlg['Rectascension'])
        rasizer = wx.StaticBoxSizer(ra, wx.VERTICAL)
        self.intimeckb = wx.CheckBox(self, -1, mtexts.txtsappearance2dlg['InTime'])
        rasizer.Add(self.intimeckb, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        mvsizer.Add(rasizer, 0, wx.GROW | wx.ALIGN_TOP | wx.RIGHT, 5)
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

    def fill(self, options):
        self.longckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.LON])
        self.latckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.LAT])
        self.rectascckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.RA])
        self.declckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.DECL])
        self.ascdifflatckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.ADLAT])
        self.semiarcusckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.SA])
        self.meridiandistckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.MD])
        self.horizondistckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.HD])
        self.temporalhourckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.TH])
        self.hourlydistckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.HOD])
        self.pmpckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.PMP])
        self.ascdiffpoleckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.ADPH])
        self.poleheightckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.POH])
        self.ascdescoblckb.SetValue(options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.AODO])
        self.reglongckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.LON])
        self.reglatckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.LAT])
        self.regrectascckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.RA])
        self.regdeclckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.DECL])
        self.regmeridiandistckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.RMD])
        self.reghorizondistckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.RHD])
        self.regzdckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.ZD])
        self.regpoleckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.POLE])
        self.regqckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.Q])
        self.regwckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.W])
        self.cmpckb.SetValue(options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.CMP])
        self.intimeckb.SetValue(options.intime)

    def check(self, options):
        changed = False
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.LON] != self.longckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.LON] = self.longckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.LAT] != self.latckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.LAT] = self.latckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.RA] != self.rectascckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.RA] = self.rectascckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.DECL] != self.declckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.DECL] = self.declckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.ADLAT] != self.ascdifflatckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.ADLAT] = self.ascdifflatckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.SA] != self.semiarcusckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.SA] = self.semiarcusckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.MD] != self.meridiandistckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.MD] = self.meridiandistckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.HD] != self.horizondistckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.HD] = self.horizondistckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.TH] != self.temporalhourckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.TH] = self.temporalhourckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.HOD] != self.hourlydistckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.HOD] = self.hourlydistckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.PMP] != self.pmpckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.PMP] = self.pmpckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.ADPH] != self.ascdiffpoleckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.ADPH] = self.ascdiffpoleckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.POH] != self.poleheightckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.POH] = self.poleheightckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.AODO] != self.ascdescoblckb.GetValue():
            options.speculums[planets.Planet.PLACIDIAN][placspec.PlacidianSpeculum.AODO] = self.ascdescoblckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.LON] != self.reglongckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.LON] = self.reglongckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.LAT] != self.reglatckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.LAT] = self.reglatckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.RA] != self.regrectascckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.RA] = self.regrectascckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.DECL] != self.regdeclckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.DECL] = self.regdeclckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.RMD] != self.regmeridiandistckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.RMD] = self.regmeridiandistckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.RHD] != self.reghorizondistckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.RHD] = self.reghorizondistckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.ZD] != self.regzdckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.ZD] = self.regzdckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.POLE] != self.regpoleckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.POLE] = self.regpoleckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.Q] != self.regqckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.Q] = self.regqckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.W] != self.regwckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.W] = self.regwckb.GetValue()
            changed = True
        if options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.CMP] != self.cmpckb.GetValue():
            options.speculums[planets.Planet.REGIOMONTANIAN][regiospec.RegiomontanianSpeculum.CMP] = self.cmpckb.GetValue()
            changed = True
        if options.intime != self.intimeckb.GetValue():
            options.intime = self.intimeckb.GetValue()
            changed = True
        return changed
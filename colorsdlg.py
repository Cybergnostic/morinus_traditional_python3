# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, chart, planets, mtexts

class ColorsDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtscolorsdlg['Colors'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        schart = wx.StaticBox(self, label=mtexts.txtscolorsdlg['Chart'])
        chartsizer = wx.StaticBoxSizer(schart, wx.VERTICAL)
        gsizer = wx.GridSizer(5, 2)
        ID_BTN_Frame = wx.NewId()
        self.baseid = ID_BTN_Frame
        label = wx.StaticText(self, -1, mtexts.txtscolorsdlg['Frame'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnFrame = wx.Button(self, ID_BTN_Frame, '', size=(60, -1))
        gsizer.Add(self.btnFrame, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Signs = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscolorsdlg['Signs'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnSigns = wx.Button(self, ID_BTN_Signs, '', size=(60, -1))
        gsizer.Add(self.btnSigns, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_AscMC = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscolorsdlg['AscMC'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnAscMC = wx.Button(self, ID_BTN_AscMC, '', size=(60, -1))
        gsizer.Add(self.btnAscMC, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Houses = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscolorsdlg['Houses'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnHouses = wx.Button(self, ID_BTN_Houses, '', size=(60, -1))
        gsizer.Add(self.btnHouses, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_HouseNumbers = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscolorsdlg['Housenames'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnHouseNumbers = wx.Button(self, ID_BTN_HouseNumbers, '', size=(60, -1))
        gsizer.Add(self.btnHouseNumbers, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        chartsizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vsizer.Add(chartsizer, 0, wx.LEFT, 5)
        saux = wx.StaticBox(self, label='')
        auxsizer = wx.StaticBoxSizer(saux, wx.VERTICAL)
        gsizer = wx.GridSizer(1, 2)
        ID_BTN_Aux = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscolorsdlg['Auxiliary'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnAux = wx.Button(self, ID_BTN_Aux, '', size=(60, -1))
        gsizer.Add(self.btnAux, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        auxsizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vsizer.Add(auxsizer, 1, wx.GROW | wx.LEFT, 5)
        mhsizer.Add(vsizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        planetsbox = wx.StaticBox(self, label=mtexts.txtscolorsdlg['Planets'])
        planetssizer = wx.StaticBoxSizer(planetsbox, wx.VERTICAL)
        gsizer = wx.GridSizer(10, 2)
        self.pltxts = []
        ID_BTN_Saturn = wx.NewId()
        self.pltxts.append(wx.StaticText(self, -1, mtexts.txtscommon['Saturn'] + ':'))
        gsizer.Add(self.pltxts[0], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnSaturn = wx.Button(self, ID_BTN_Saturn, '', size=(60, -1))
        gsizer.Add(self.btnSaturn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Jupiter = wx.NewId()
        self.pltxts.append(wx.StaticText(self, -1, mtexts.txtscommon['Jupiter'] + ':'))
        gsizer.Add(self.pltxts[1], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnJupiter = wx.Button(self, ID_BTN_Jupiter, '', size=(60, -1))
        gsizer.Add(self.btnJupiter, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Mars = wx.NewId()
        self.pltxts.append(wx.StaticText(self, -1, mtexts.txtscommon['Mars'] + ':'))
        gsizer.Add(self.pltxts[2], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnMars = wx.Button(self, ID_BTN_Mars, '', size=(60, -1))
        gsizer.Add(self.btnMars, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Sun = wx.NewId()
        self.pltxts.append(wx.StaticText(self, -1, mtexts.txtscommon['Sun'] + ':'))
        gsizer.Add(self.pltxts[3], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnSun = wx.Button(self, ID_BTN_Sun, '', size=(60, -1))
        gsizer.Add(self.btnSun, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Venus = wx.NewId()
        self.pltxts.append(wx.StaticText(self, -1, mtexts.txtscommon['Venus'] + ':'))
        gsizer.Add(self.pltxts[4], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnVenus = wx.Button(self, ID_BTN_Venus, '', size=(60, -1))
        gsizer.Add(self.btnVenus, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Mercury = wx.NewId()
        self.pltxts.append(wx.StaticText(self, -1, mtexts.txtscommon['Mercury'] + ':'))
        gsizer.Add(self.pltxts[5], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnMercury = wx.Button(self, ID_BTN_Mercury, '', size=(60, -1))
        gsizer.Add(self.btnMercury, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Moon = wx.NewId()
        self.pltxts.append(wx.StaticText(self, -1, mtexts.txtscommon['Moon'] + ':'))
        gsizer.Add(self.pltxts[6], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnMoon = wx.Button(self, ID_BTN_Moon, '', size=(60, -1))
        gsizer.Add(self.btnMoon, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Nodes = wx.NewId()
        self.pltxts.append(wx.StaticText(self, -1, mtexts.txtscommon['Nodes'] + ':'))
        gsizer.Add(self.pltxts[7], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnNodes = wx.Button(self, ID_BTN_Nodes, '', size=(60, -1))
        gsizer.Add(self.btnNodes, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_LoF = wx.NewId()
        self.pltxts.append(wx.StaticText(self, -1, mtexts.txtscommon['LoF'] + ':'))
        gsizer.Add(self.pltxts[8], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnLoF = wx.Button(self, ID_BTN_LoF, '', size=(60, -1))
        gsizer.Add(self.btnLoF, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        planetssizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        mhsizer.Add(planetssizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        aspects = wx.StaticBox(self, label=mtexts.txtscommon['Aspects'])
        aspectsizer = wx.StaticBoxSizer(aspects, wx.VERTICAL)
        gsizer = wx.GridSizer(11, 2)
        ID_BTN_Conjunctio = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscommon['Conjunction'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnConjunctio = wx.Button(self, ID_BTN_Conjunctio, '', size=(60, -1))
        gsizer.Add(self.btnConjunctio, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Sextil = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscommon['Sextile'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnSextil = wx.Button(self, ID_BTN_Sextil, '', size=(60, -1))
        gsizer.Add(self.btnSextil, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Quadrat = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscommon['Square'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnQuadrat = wx.Button(self, ID_BTN_Quadrat, '', size=(60, -1))
        gsizer.Add(self.btnQuadrat, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Trigon = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscommon['Trine'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnTrigon = wx.Button(self, ID_BTN_Trigon, '', size=(60, -1))
        gsizer.Add(self.btnTrigon, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Oppositio = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscommon['Opposition'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnOppositio = wx.Button(self, ID_BTN_Oppositio, '', size=(60, -1))
        gsizer.Add(self.btnOppositio, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        aspectsizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(aspectsizer, 0, wx.TOP, 5)
        general = wx.StaticBox(self, label=mtexts.txtscolorsdlg['General'])
        generalsizer = wx.StaticBoxSizer(general, wx.VERTICAL)
        gsizer = wx.GridSizer(4, 2)
        ID_BTN_Background = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscolorsdlg['Background'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnBackground = wx.Button(self, ID_BTN_Background, '', size=(60, -1))
        gsizer.Add(self.btnBackground, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Table = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscolorsdlg['Table'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnTable = wx.Button(self, ID_BTN_Table, '', size=(60, -1))
        gsizer.Add(self.btnTable, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        ID_BTN_Texts = wx.NewId()
        label = wx.StaticText(self, -1, mtexts.txtscolorsdlg['Texts'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.btnTexts = wx.Button(self, ID_BTN_Texts, '', size=(60, -1))
        gsizer.Add(self.btnTexts, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        generalsizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vsizer.Add(generalsizer, 0, wx.TOP, 5)
        mhsizer.Add(vsizer, 0, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        mvsizer.Add(mhsizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.arBtn = [
         self.btnFrame, self.btnSigns, self.btnAscMC, self.btnHouses, self.btnHouseNumbers, self.btnAux, self.btnSaturn, self.btnJupiter, self.btnMars, self.btnSun, self.btnVenus, self.btnMercury, self.btnMoon, self.btnNodes, self.btnLoF, self.btnConjunctio, self.btnSextil, self.btnQuadrat, self.btnTrigon, self.btnOppositio, self.btnBackground, self.btnTable, self.btnTexts]
        wx.EVT_BUTTON(self, ID_BTN_Frame, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Signs, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_AscMC, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Houses, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_HouseNumbers, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Aux, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Saturn, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Jupiter, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Mars, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Sun, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Venus, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Mercury, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Moon, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Nodes, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_LoF, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Conjunctio, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Sextil, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Quadrat, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Trigon, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Oppositio, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Background, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Table, self.onBtn)
        wx.EVT_BUTTON(self, ID_BTN_Texts, self.onBtn)
        btnsizer = wx.StdDialogButtonSizer()
        okbtn = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Ok'])
        okbtn.SetDefault()
        btnsizer.AddButton(okbtn)
        cancelbtn = wx.Button(self, wx.ID_CANCEL, mtexts.txtscommon['Cancel'])
        btnsizer.AddButton(cancelbtn)
        btnsizer.Realize()
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        okbtn.SetFocus()

    def onBtn(self, event):
        btnid = event.GetId() - self.baseid
        data = wx.ColourData()
        data.SetChooseFull(True)
        data.SetColour(self.arBtn[btnid].GetBackgroundColour())
        dlg = wx.ColourDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            self.arBtn[btnid].SetBackgroundColour(data.GetColour())
        dlg.Destroy()

    def fill(self, options):
        self.btnFrame.SetBackgroundColour(options.clrframe)
        self.btnSigns.SetBackgroundColour(options.clrsigns)
        self.btnAscMC.SetBackgroundColour(options.clrAscMC)
        self.btnHouses.SetBackgroundColour(options.clrhouses)
        self.btnHouseNumbers.SetBackgroundColour(options.clrhousenumbers)
        self.btnAux.SetBackgroundColour(options.clraux)
        self.btnSaturn.SetBackgroundColour(options.clrplanets[planets.Planets.SATURN])
        self.btnJupiter.SetBackgroundColour(options.clrplanets[planets.Planets.JUPITER])
        self.btnMars.SetBackgroundColour(options.clrplanets[planets.Planets.MARS])
        self.btnSun.SetBackgroundColour(options.clrplanets[planets.Planets.SUN])
        self.btnVenus.SetBackgroundColour(options.clrplanets[planets.Planets.VENUS])
        self.btnMercury.SetBackgroundColour(options.clrplanets[planets.Planets.MERCURY])
        self.btnMoon.SetBackgroundColour(options.clrplanets[planets.Planets.MOON])
        self.btnNodes.SetBackgroundColour(options.clrplanets[planets.Planets.ANODE])
        self.btnLoF.SetBackgroundColour(options.clrLoF)
        self.btnConjunctio.SetBackgroundColour(options.clraspect[chart.Chart.CONIUNCTIO])
        self.btnSextil.SetBackgroundColour(options.clraspect[chart.Chart.SEXTIL])
        self.btnQuadrat.SetBackgroundColour(options.clraspect[chart.Chart.QUADRAT])
        self.btnTrigon.SetBackgroundColour(options.clraspect[chart.Chart.TRIGON])
        self.btnOppositio.SetBackgroundColour(options.clraspect[chart.Chart.OPPOSITIO])
        self.btnBackground.SetBackgroundColour(options.clrbackground)
        self.btnTable.SetBackgroundColour(options.clrtable)
        self.btnTexts.SetBackgroundColour(options.clrtexts)

    def check(self, options):
        changed = False
        if options.clrframe != self.btnFrame.GetBackgroundColour().Get(False):
            options.clrframe = self.btnFrame.GetBackgroundColour().Get(False)
            changed = True
        if options.clrsigns != self.btnSigns.GetBackgroundColour().Get(False):
            options.clrsigns = self.btnSigns.GetBackgroundColour().Get(False)
            changed = True
        if options.clrAscMC != self.btnAscMC.GetBackgroundColour().Get(False):
            options.clrAscMC = self.btnAscMC.GetBackgroundColour().Get(False)
            changed = True
        if options.clrhouses != self.btnHouses.GetBackgroundColour().Get(False):
            options.clrhouses = self.btnHouses.GetBackgroundColour().Get(False)
            changed = True
        if options.clrhousenumbers != self.btnHouseNumbers.GetBackgroundColour().Get(False):
            options.clrhousenumbers = self.btnHouseNumbers.GetBackgroundColour().Get(False)
            changed = True
        if options.clraux != self.btnAux.GetBackgroundColour().Get(False):
            options.clraux = self.btnAux.GetBackgroundColour().Get(False)
            changed = True
        if options.clrplanets[planets.Planets.SATURN] != self.btnSaturn.GetBackgroundColour().Get(False):
            options.clrplanets[planets.Planets.SATURN] = self.btnSaturn.GetBackgroundColour().Get(False)
            changed = True
        if options.clrplanets[planets.Planets.JUPITER] != self.btnJupiter.GetBackgroundColour().Get(False):
            options.clrplanets[planets.Planets.JUPITER] = self.btnJupiter.GetBackgroundColour().Get(False)
            changed = True
        if options.clrplanets[planets.Planets.MARS] != self.btnMars.GetBackgroundColour().Get(False):
            options.clrplanets[planets.Planets.MARS] = self.btnMars.GetBackgroundColour().Get(False)
            changed = True
        if options.clrplanets[planets.Planets.SUN] != self.btnSun.GetBackgroundColour().Get(False):
            options.clrplanets[planets.Planets.SUN] = self.btnSun.GetBackgroundColour().Get(False)
            changed = True
        if options.clrplanets[planets.Planets.VENUS] != self.btnVenus.GetBackgroundColour().Get(False):
            options.clrplanets[planets.Planets.VENUS] = self.btnVenus.GetBackgroundColour().Get(False)
            changed = True
        if options.clrplanets[planets.Planets.MERCURY] != self.btnMercury.GetBackgroundColour().Get(False):
            options.clrplanets[planets.Planets.MERCURY] = self.btnMercury.GetBackgroundColour().Get(False)
            changed = True
        if options.clrplanets[planets.Planets.MOON] != self.btnMoon.GetBackgroundColour().Get(False):
            options.clrplanets[planets.Planets.MOON] = self.btnMoon.GetBackgroundColour().Get(False)
            changed = True
        if options.clrplanets[planets.Planets.ANODE] != self.btnNodes.GetBackgroundColour().Get(False):
            options.clrplanets[planets.Planets.ANODE] = self.btnNodes.GetBackgroundColour().Get(False)
            changed = True
        if options.clrLoF != self.btnLoF.GetBackgroundColour().Get(False):
            options.clrLoF = self.btnLoF.GetBackgroundColour().Get(False)
            changed = True
        if options.clraspect[chart.Chart.CONIUNCTIO] != self.btnConjunctio.GetBackgroundColour().Get(False):
            options.clraspect[chart.Chart.CONIUNCTIO] = self.btnConjunctio.GetBackgroundColour().Get(False)
            changed = True
        if options.clraspect[chart.Chart.SEXTIL] != self.btnSextil.GetBackgroundColour().Get(False):
            options.clraspect[chart.Chart.SEXTIL] = self.btnSextil.GetBackgroundColour().Get(False)
            changed = True
        if options.clraspect[chart.Chart.QUADRAT] != self.btnQuadrat.GetBackgroundColour().Get(False):
            options.clraspect[chart.Chart.QUADRAT] = self.btnQuadrat.GetBackgroundColour().Get(False)
            changed = True
        if options.clraspect[chart.Chart.TRIGON] != self.btnTrigon.GetBackgroundColour().Get(False):
            options.clraspect[chart.Chart.TRIGON] = self.btnTrigon.GetBackgroundColour().Get(False)
            changed = True
        if options.clraspect[chart.Chart.OPPOSITIO] != self.btnOppositio.GetBackgroundColour().Get(False):
            options.clraspect[chart.Chart.OPPOSITIO] = self.btnOppositio.GetBackgroundColour().Get(False)
            changed = True
        if options.clrbackground != self.btnBackground.GetBackgroundColour().Get(False):
            options.clrbackground = self.btnBackground.GetBackgroundColour().Get(False)
            changed = True
        if options.clrtable != self.btnTable.GetBackgroundColour().Get(False):
            options.clrtable = self.btnTable.GetBackgroundColour().Get(False)
            changed = True
        if options.clrtexts != self.btnTexts.GetBackgroundColour().Get(False):
            options.clrtexts = self.btnTexts.GetBackgroundColour().Get(False)
            changed = True
        return changed
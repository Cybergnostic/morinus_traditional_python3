# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import intvalidator
import placesdlg
import mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class DefaultLocDlg(wx.Dialog):
    PLUSCHOICES = ('+', '-')

    def __init__(self, parent, langid, netbook):
        self.langid = langid
        self.netbook = netbook
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtsdeflocdlgopts['DefaultLocation'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        fgsizer = wx.FlexGridSizer(0, 4, 0, 0)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.splace = wx.StaticBox(self, label='')
        placesizer = wx.StaticBoxSizer(self.splace, wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdeflocdlgopts['Long'] + ':')
        fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdeflocdlgopts['Deg'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.londeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 180), size=(40,
                                                                                                   -1))
        self.londeg.SetHelpText(mtexts.txtsdeflocdlgopts['HelpLonDeg'])
        self.londeg.SetMaxLength(3)
        vvsizer.Add(self.londeg, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdeflocdlgopts['Min'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.lonmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.lonmin.SetHelpText(mtexts.txtsdeflocdlgopts['HelpMin'])
        self.lonmin.SetMaxLength(2)
        vvsizer.Add(self.lonmin, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        self.placerbE = wx.RadioButton(self, -1, mtexts.txtsdeflocdlgopts['E'], style=wx.RB_GROUP)
        vvsizer.Add(self.placerbE, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        self.placerbW = wx.RadioButton(self, -1, mtexts.txtsdeflocdlgopts['W'])
        vvsizer.Add(self.placerbW, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        label = wx.StaticText(self, -1, mtexts.txtsdeflocdlgopts['Lat'] + ':')
        fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdeflocdlgopts['Deg'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.latdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 90), size=(40,
                                                                                                  -1))
        self.latdeg.SetHelpText(mtexts.txtsdeflocdlgopts['HelpLatDeg'])
        self.latdeg.SetMaxLength(2)
        vvsizer.Add(self.latdeg, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdeflocdlgopts['Min'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.latmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.latmin.SetHelpText(mtexts.txtsdeflocdlgopts['HelpMin'])
        self.latmin.SetMaxLength(2)
        vvsizer.Add(self.latmin, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        self.placerbN = wx.RadioButton(self, -1, mtexts.txtsdeflocdlgopts['N'], style=wx.RB_GROUP)
        vvsizer.Add(self.placerbN, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        self.placerbS = wx.RadioButton(self, -1, mtexts.txtsdeflocdlgopts['S'])
        vvsizer.Add(self.placerbS, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsizer.Add(fgsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        ID_PlaceButton = wx.NewId()
        placebtn = wx.Button(self, ID_PlaceButton, mtexts.txtsdeflocdlgopts['Place'] + ':', size=(100,
                                                                                                  -1))
        vsizer.Add(placebtn, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.name = wx.TextCtrl(self, -1, '', size=(170, -1))
        self.name.SetHelpText(mtexts.txtsdeflocdlgopts['HelpPlace'])
        self.name.SetMaxLength(20)
        vsizer.Add(self.name, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        placesizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
        vvsubsizer = wx.BoxSizer(wx.VERTICAL)
        vvsubsizer.Add(placesizer, 0, wx.ALIGN_LEFT | wx.RIGHT, 5)
        hsubsizer.Add(vvsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        self.szone = wx.StaticBox(self, label='')
        zonesizer = wx.StaticBoxSizer(self.szone, wx.VERTICAL)
        hhsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.gmtlabel = wx.StaticText(self, -1, mtexts.txtsdeflocdlgopts['GMT'])
        hhsizer.Add(self.gmtlabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.pluscb = wx.ComboBox(self, -1, DefaultLocDlg.PLUSCHOICES[0], size=(50,
                                                                                -1), choices=DefaultLocDlg.PLUSCHOICES, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        hhsizer.Add(self.pluscb, 0, wx.LEFT, 5)
        zonesizer.Add(hhsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        fgsizer = wx.FlexGridSizer(0, 2, 0, 0)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        self.zhourlabel = wx.StaticText(self, -1, mtexts.txtsdeflocdlgopts['Hour'] + ':')
        vvsizer.Add(self.zhourlabel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.zhour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                                 -1))
        self.zhour.SetHelpText(mtexts.txtsdeflocdlgopts['HelpZoneHour'])
        self.zhour.SetMaxLength(2)
        vvsizer.Add(self.zhour, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        self.zminutelabel = wx.StaticText(self, -1, mtexts.txtsdeflocdlgopts['Min'] + ':')
        vvsizer.Add(self.zminutelabel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.zminute = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                   -1))
        self.zminute.SetHelpText(mtexts.txtsdeflocdlgopts['HelpMin'])
        self.zminute.SetMaxLength(2)
        vvsizer.Add(self.zminute, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        zonesizer.Add(fgsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.daylightckb = wx.CheckBox(self, -1, mtexts.txtsdeflocdlgopts['Daylight'])
        zonesizer.Add(self.daylightckb, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.daylightckb.SetHelpText(mtexts.txtsdeflocdlgopts['HelpDaylight'])
        vvsubsizer = wx.BoxSizer(wx.VERTICAL)
        vvsubsizer.Add(zonesizer, 2, wx.ALIGN_LEFT | wx.ALL, 0)
        self.sphs = wx.StaticBox(self, label=mtexts.txtsdeflocdlgopts['Altitude'])
        hourssizer = wx.StaticBoxSizer(self.sphs, wx.VERTICAL)
        self.alt = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 10000), size=(60,
                                                                                                  -1))
        self.alt.SetHelpText(mtexts.txtsdeflocdlgopts['HelpAltitude'])
        self.alt.SetMaxLength(5)
        hhsubsizer = wx.BoxSizer(wx.HORIZONTAL)
        hhsubsizer.Add(self.alt, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        label = wx.StaticText(self, -1, 'm')
        hhsubsizer.Add(label, 0, wx.ALIGN_CENTER | wx.LEFT, 2)
        hourssizer.Add(hhsubsizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vvsubsizer.Add(hourssizer, 1, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 0)
        hsubsizer.Add(vvsubsizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 0)
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        vsubsizer.Add(hsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        mhsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, 5)
        mvsizer.Add(mhsizer, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT, 5)
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
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.onPlaceButton, id=ID_PlaceButton)
        self.name.SetFocus()

    def onOK(self, event):
        if self.Validate() and self.splace.Validate() and self.szone.Validate() and self.sphs:
            self.Close()
            self.SetReturnCode(wx.ID_OK)

    def onPlaceButton(self, event):
        pdlg = placesdlg.PlacesDlg(self, self.langid, self.netbook)
        val = pdlg.ShowModal()
        if val == wx.ID_OK:
            if pdlg.li.currentItem != -1:
                place = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.PLACE)
                lon = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.LON)
                lat = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.LAT)
                zone = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.ZONE)
                alt = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.ALT)
                self.name.SetValue(place.strip())
                idx = lon.find('E')
                if idx == -1:
                    idx = lon.find('W')
                    self.placerbW.SetValue(True)
                else:
                    self.placerbE.SetValue(True)
                fr = 0
                if lon[0] == '0':
                    fr = 1
                self.londeg.SetValue(lon[fr:idx])
                idx += 1
                if lon[idx] == '0':
                    idx += 1
                self.lonmin.SetValue(lon[idx:])
                idx = lat.find('N')
                if idx == -1:
                    idx = lat.find('S')
                    self.placerbS.SetValue(True)
                else:
                    self.placerbN.SetValue(True)
                fr = 0
                if lat[0] == '0':
                    fr = 1
                self.latdeg.SetValue(lat[fr:idx])
                idx += 1
                if lat[idx] == '0':
                    idx += 1
                self.latmin.SetValue(lat[idx:])
                self.pluscb.SetStringSelection(zone[0])
                zone = zone[1:]
                idx = zone.find(':')
                self.zhour.SetValue(zone[0:idx])
                idx += 1
                if zone[idx] == '0':
                    idx += 1
                self.zminute.SetValue(zone[idx:])
                self.alt.SetValue(alt)
        pdlg.Destroy()

    def fill(self, opts):
        self.name.SetValue(opts.deflocname)
        idx = 0
        if not opts.deflocplus:
            idx = 1
        self.pluscb.SetStringSelection(DefaultLocDlg.PLUSCHOICES[idx])
        self.zhour.SetValue(str(opts.defloczhour))
        self.zminute.SetValue(str(opts.defloczminute))
        self.daylightckb.SetValue(opts.deflocdst)
        self.londeg.SetValue(str(opts.defloclondeg))
        self.lonmin.SetValue(str(opts.defloclonmin))
        if opts.defloceast:
            self.placerbE.SetValue(True)
        else:
            self.placerbW.SetValue(True)
        self.latdeg.SetValue(str(opts.defloclatdeg))
        self.latmin.SetValue(str(opts.defloclatmin))
        if opts.deflocnorth:
            self.placerbN.SetValue(True)
        else:
            self.placerbS.SetValue(True)
        self.alt.SetValue(str(opts.deflocalt))

    def check(self, opts):
        changed = False
        idx = 0
        if not opts.deflocplus:
            idx = 1
        if self.pluscb.GetCurrentSelection() != idx:
            if self.pluscb.GetCurrentSelection() == 0:
                opts.deflocplus = True
            else:
                opts.deflocplus = False
            changed = True
        if int(self.zhour.GetValue()) != opts.defloczhour:
            opts.defloczhour = int(self.zhour.GetValue())
            changed = True
        if int(self.zminute.GetValue()) != opts.defloczminute:
            opts.defloczminute = int(self.zminute.GetValue())
            changed = True
        if opts.deflocdst != self.daylightckb.GetValue():
            opts.deflocdst = self.daylightckb.GetValue()
            changed = True
        if self.name.GetValue() != opts.deflocname:
            opts.deflocname = self.name.GetValue()
            changed = True
        if int(self.londeg.GetValue()) != opts.defloclondeg:
            opts.defloclondeg = int(self.londeg.GetValue())
            changed = True
        if int(self.lonmin.GetValue()) != opts.defloclonmin:
            opts.defloclonmin = int(self.lonmin.GetValue())
            changed = True
        if self.placerbE.GetValue() != opts.defloceast:
            opts.defloceast = self.placerbE.GetValue()
            changed = True
        if int(self.latdeg.GetValue()) != opts.defloclatdeg:
            opts.defloclatdeg = int(self.latdeg.GetValue())
            changed = True
        if int(self.latmin.GetValue()) != opts.defloclatmin:
            opts.defloclatmin = int(self.latmin.GetValue())
            changed = True
        if self.placerbN.GetValue() != opts.deflocnorth:
            opts.deflocnorth = self.placerbN.GetValue()
            changed = True
        if int(self.alt.GetValue()) != opts.deflocalt:
            opts.deflocalt = int(self.alt.GetValue())
            changed = True
        return changed
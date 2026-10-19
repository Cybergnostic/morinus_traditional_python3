# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import sys
import wx
import intvalidator
import placedb
import placeslistdlg
import geonames
import mtexts
import util
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class PlaceListCtrl(wx.ListCtrl):
    PLACE = 0
    LON = 1
    LAT = 2
    ZONE = 3
    ALT = 4
    COLNUM = ALT + 1

    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        self.placedata = {}
        self.load()
        self.Populate()
        self.Id = ID
        self.changed = False

    def Populate(self):
        self.InsertColumn(PlaceListCtrl.PLACE, mtexts.txtsplacesdlg['Place'])
        self.InsertColumn(PlaceListCtrl.LON, mtexts.txtsplacesdlg['Long'] + '.')
        self.InsertColumn(PlaceListCtrl.LAT, mtexts.txtsplacesdlg['Lat'] + '.')
        self.InsertColumn(PlaceListCtrl.ZONE, mtexts.txtsplacesdlg['Zone'])
        self.InsertColumn(PlaceListCtrl.ALT, mtexts.txtsplacesdlg['Alt'] + '.')
        items = list(self.placedata.items())
        for key, data in items:
            index = self.InsertItem(sys.maxsize, data[0])
            self.SetItem(index, PlaceListCtrl.PLACE, data[0])
            self.SetItem(index, PlaceListCtrl.LON, data[1])
            self.SetItem(index, PlaceListCtrl.LAT, data[2])
            self.SetItem(index, PlaceListCtrl.ZONE, data[3])
            self.SetItem(index, PlaceListCtrl.ALT, data[4])
            self.SetItemData(index, key)

        self.SetColumnWidth(PlaceListCtrl.PLACE, 200)
        self.SetColumnWidth(PlaceListCtrl.LON, 60)
        self.SetColumnWidth(PlaceListCtrl.LAT, 60)
        self.SetColumnWidth(PlaceListCtrl.ZONE, 60)
        self.SetColumnWidth(PlaceListCtrl.ALT, 60)
        self.currentItem = -1
        if len(self.placedata):
            self.currentItem = 0
            self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

    def GetListCtrl(self):
        return self

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        event.Skip()

    def OnColClick(self, event):
        event.Skip()

    def OnAdd(self, item):
        num = self.GetItemCount()
        self.InsertItem(num, item[PlaceListCtrl.PLACE])
        for i in range(1, len(item)):
            self.SetItem(num, i, item[i])

        self.currentItem = num
        self.EnsureVisible(self.currentItem)
        self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self.changed = True

    def OnRemove(self):
        if self.currentItem != -1:
            dlg = wx.MessageDialog(self, mtexts.txtscommon['AreYouSure'], mtexts.txtscommon['Confirm'], wx.YES_NO | wx.ICON_QUESTION)
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                self.DeleteItem(self.currentItem)
                if self.GetItemCount() == 0:
                    self.currentItem = -1
                elif self.currentItem >= self.GetItemCount():
                    self.currentItem = self.GetItemCount() - 1
                    self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                else:
                    self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                self.changed = True
            dlg.Destroy()

    def OnRemoveAll(self):
        if self.currentItem != -1:
            dlg = wx.MessageDialog(self, mtexts.txtscommon['AreYouSure'], mtexts.txtscommon['Confirm'], wx.YES_NO | wx.ICON_QUESTION)
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                self.DeleteAllItems()
                self.currentItem = -1
                self.changed = True
            dlg.Destroy()

    def load(self):
        pdb = placedb.PlaceDB()
        pdb.read()
        idx = 1
        for p in pdb.placedb:
            self.placedata[idx] = (
             p.name, p.lon, p.lat, p.tz, p.alt)
            idx += 1

    def save(self):
        if self.changed:
            pdb = placedb.PlaceDB()
            for i in range(self.GetItemCount()):
                pdb.add(self.getColumnText(i, PlaceListCtrl.PLACE), self.getColumnText(i, PlaceListCtrl.LON), self.getColumnText(i, PlaceListCtrl.LAT), self.getColumnText(i, PlaceListCtrl.ZONE), self.getColumnText(i, PlaceListCtrl.ALT))

            pdb.sort()
            pdb.write()
            self.changed = False


class PlacesDlg(wx.Dialog):
    PLUSCHOICES = ('+', '-')

    def __init__(self, parent, langid, netbook):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtsplacesdlg['Places'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.langid = langid
        self.netbook = netbook
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        fgsizer = wx.FlexGridSizer(0, 4, 0, 0)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.splace = wx.StaticBox(self, label='')
        placesizer = wx.StaticBoxSizer(self.splace, wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsplacesdlg['Long'] + ':')
        fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsplacesdlg['Deg'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.londeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 180), size=(40,
                                                                                                   -1))
        self.londeg.SetValue('0')
        self.londeg.SetHelpText(mtexts.txtsplacesdlg['HelpLonDeg'])
        self.londeg.SetMaxLength(3)
        vvsizer.Add(self.londeg, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsplacesdlg['Min'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.lonmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.lonmin.SetValue('0')
        self.lonmin.SetHelpText(mtexts.txtsplacesdlg['HelpMin'])
        self.lonmin.SetMaxLength(2)
        vvsizer.Add(self.lonmin, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        self.placerbE = wx.RadioButton(self, -1, mtexts.txtsplacesdlg['E'], style=wx.RB_GROUP)
        vvsizer.Add(self.placerbE, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        self.placerbW = wx.RadioButton(self, -1, mtexts.txtsplacesdlg['W'])
        vvsizer.Add(self.placerbW, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, mtexts.txtsplacesdlg['Lat'] + ':')
        fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsplacesdlg['Deg'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.latdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 90), size=(40,
                                                                                                  -1))
        self.latdeg.SetValue('0')
        self.latdeg.SetHelpText(mtexts.txtsplacesdlg['HelpLatDeg'])
        self.latdeg.SetMaxLength(2)
        vvsizer.Add(self.latdeg, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsplacesdlg['Min'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.latmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.latmin.SetValue('0')
        self.latmin.SetHelpText(mtexts.txtsplacesdlg['HelpMin'])
        self.latmin.SetMaxLength(2)
        vvsizer.Add(self.latmin, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        self.placerbN = wx.RadioButton(self, -1, mtexts.txtsplacesdlg['N'], style=wx.RB_GROUP)
        vvsizer.Add(self.placerbN, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        self.placerbS = wx.RadioButton(self, -1, mtexts.txtsplacesdlg['S'])
        vvsizer.Add(self.placerbS, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsizer.Add(fgsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        label = wx.StaticText(self, -1, mtexts.txtsplacesdlg['Place'] + ':')
        vsizer.Add(label, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.birthplace = wx.TextCtrl(self, -1, '', size=(170, -1))
        self.birthplace.SetHelpText(mtexts.txtsplacesdlg['HelpPlace'])
        self.birthplace.SetMaxLength(20)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.birthplace, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        ID_Search = wx.NewId()
        btnSearch = wx.Button(self, ID_Search, mtexts.txtsplacesdlg['Search'])
        hsizer.Add(btnSearch, 0, wx.ALIGN_CENTER)
        vsizer.Add(hsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        placesizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        vsubsizer.Add(placesizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.RIGHT, 5)
        maxonlinesize = wx.StaticBox(self, label=mtexts.txtsplacesdlg['MaxNumberOnlineSearch'])
        maxonlinesizesizer = wx.StaticBoxSizer(maxonlinesize, wx.VERTICAL)
        self.sizeslider = wx.Slider(self, -1, 2, 2, 100, size=(250, -1), style=wx.SL_LABELS)
        maxonlinesizesizer.Add(self.sizeslider, 1, wx.ALIGN_CENTRE, 5)
        vsubsizer.Add(maxonlinesizesizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.RIGHT, 5)
        self.szone = wx.StaticBox(self, label=mtexts.txtsplacesdlg['Zone'])
        zonesizer = wx.StaticBoxSizer(self.szone, wx.VERTICAL)
        hhsizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, mtexts.txtsplacesdlg['GMT'])
        hhsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.pluscb = wx.ComboBox(self, -1, PlacesDlg.PLUSCHOICES[0], size=(50, -1), choices=PlacesDlg.PLUSCHOICES, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.pluscb.SetStringSelection(PlacesDlg.PLUSCHOICES[0])
        hhsizer.Add(self.pluscb, 0, wx.LEFT, 5)
        zonesizer.Add(hhsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        fgsizer = wx.FlexGridSizer(0, 2, 0, 0)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsplacesdlg['Hour'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.zhour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                                 -1))
        self.zhour.SetValue('0')
        self.zhour.SetHelpText(mtexts.txtsplacesdlg['HelpZoneHour'])
        self.zhour.SetMaxLength(2)
        vvsizer.Add(self.zhour, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsplacesdlg['Min'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.zminute = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                   -1))
        self.zminute.SetValue('0')
        self.zminute.SetHelpText(mtexts.txtsplacesdlg['HelpMin'])
        self.zminute.SetMaxLength(2)
        vvsizer.Add(self.zminute, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        zonesizer.Add(fgsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hhsubsizer = wx.BoxSizer(wx.HORIZONTAL)
        hhsubsizer.Add(zonesizer, 0, wx.ALIGN_LEFT | wx.RIGHT, 5)
        self.salt = wx.StaticBox(self, label=mtexts.txtsplacesdlg['Alt'])
        altsizer = wx.StaticBoxSizer(self.salt, wx.VERTICAL)
        self.alt = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 10000), size=(60,
                                                                                                  -1))
        self.alt.SetHelpText(mtexts.txtsplacesdlg['HelpAltitude'])
        self.alt.SetMaxLength(5)
        self.alt.SetValue('0')
        hhhsubsizer = wx.BoxSizer(wx.HORIZONTAL)
        hhhsubsizer.Add(self.alt, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        label = wx.StaticText(self, -1, 'm')
        hhhsubsizer.Add(label, 0, wx.ALIGN_CENTER | wx.TOP, 2)
        altsizer.Add(hhhsubsizer, 0, wx.GROW | wx.TOP, 20)
        hhsubsizer.Add(altsizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.RIGHT, 5)
        vsubsizer.Add(hhsubsizer, 0, wx.GROW | wx.ALIGN_LEFT)
        sbtns = wx.StaticBox(self, label='')
        btnssizer = wx.StaticBoxSizer(sbtns, wx.VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        ID_Add = wx.NewId()
        btnAdd = wx.Button(self, ID_Add, mtexts.txtsplacesdlg['Add'])
        vsizer.Add(btnAdd, 0, wx.GROW | wx.ALL, 5)
        if not self.netbook:
            ID_Remove = wx.NewId()
            btnRemove = wx.Button(self, ID_Remove, mtexts.txtsplacesdlg['Remove'])
            vsizer.Add(btnRemove, 0, wx.GROW | wx.ALL, 5)
            ID_RemoveAll = wx.NewId()
            btnRemoveAll = wx.Button(self, ID_RemoveAll, mtexts.txtsplacesdlg['RemoveAll'])
            vsizer.Add(btnRemoveAll, 0, wx.GROW | wx.ALL, 5)
        btnssizer.Add(vsizer, 0, wx.GROW | wx.ALL, 5)
        vsubsizer.Add(btnssizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.RIGHT, 5)
        mhsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        splaces = wx.StaticBox(self, label='')
        placessizer = wx.StaticBoxSizer(splaces, wx.VERTICAL)
        ID_Places = wx.NewId()
        self.li = PlaceListCtrl(self, ID_Places, size=(465, -1), style=wx.LC_VRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL)
        placessizer.Add(self.li, 1, wx.GROW | wx.ALL, 5)
        mhsizer.Add(placessizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 0)
        mvsizer.Add(mhsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.OnSearch, id=ID_Search)
        self.Bind(wx.EVT_BUTTON, self.OnAdd, id=ID_Add)
        if not self.netbook:
            self.Bind(wx.EVT_BUTTON, self.OnRemove, id=ID_Remove)
            self.Bind(wx.EVT_BUTTON, self.OnRemoveAll, id=ID_RemoveAll)
        btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != '__WXMSW__':
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Ok'])
        btnOk.SetHelpText(mtexts.txtscommon['HelpOk'])
        btnOk.SetDefault()
        btnsizer.AddButton(btnOk)
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        btn = wx.Button(self, wx.ID_CANCEL, mtexts.txtscommon['Cancel'])
        btn.SetHelpText(mtexts.txtscommon['HelpCancel'])
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        btnOk.SetFocus()

    def OnSearch(self, event):
        txt = self.birthplace.GetValue()
        if txt == '':
            dlg = wx.MessageDialog(self, mtexts.txtsplacesdlg['PlaceEmpty'], '', wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if len(txt) < 3:
            dlg = wx.MessageDialog(self, mtexts.txtsplacesdlg['TooFewChars'], '', wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return
        wait = wx.BusyCursor()
        maxnum = self.sizeslider.GetValue()
        geo = geonames.Geonames(self.birthplace.GetValue().encode('utf-8'), maxnum, self.langid)
        if geo.get_location_info():
            if len(geo.li) == 1:
                self.fillFields(geo.li[0])
            else:
                pldlg = placeslistdlg.PlacesListDlg(self, geo.li)
                val = pldlg.ShowModal()
                if val == wx.ID_OK:
                    if pldlg.li.currentItem != -1:
                        self.fillFields(geo.li[pldlg.li.currentItem])
                pldlg.Destroy()
        else:
            dlg = wx.MessageDialog(self, mtexts.txtsplacesdlg['NotFound'], '', wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()

    def fillFields(self, it):
        self.birthplace.SetValue(it[geonames.Geonames.NAME])
        east = True
        lon = it[geonames.Geonames.LON]
        if lon < 0.0:
            east = False
            lon *= -1
        d, m, s = util.decToDeg(lon)
        self.londeg.SetValue(str(d))
        self.lonmin.SetValue(str(m))
        if east:
            self.placerbE.SetValue(True)
        else:
            self.placerbW.SetValue(True)
        north = True
        lat = it[geonames.Geonames.LAT]
        if lat < 0.0:
            north = False
            lat *= -1
        d, m, s = util.decToDeg(lat)
        self.latdeg.SetValue(str(d))
        self.latmin.SetValue(str(m))
        if north:
            self.placerbN.SetValue(True)
        else:
            self.placerbS.SetValue(True)
        plus = True
        gmtoffs = it[geonames.Geonames.GMTOFFS]
        if gmtoffs < 0.0:
            plus = False
            gmtoffs *= -1
        gmtoffshour = int(gmtoffs)
        gmtoffsmin = int((gmtoffs - gmtoffshour) * 60.0)
        self.zhour.SetValue(str(gmtoffshour))
        self.zminute.SetValue(str(gmtoffsmin))
        val = 0
        if not plus:
            val = 1
        self.pluscb.SetStringSelection(PlacesDlg.PLUSCHOICES[val])
        alt = int(it[geonames.Geonames.ALTITUDE])
        if alt < 0:
            alt = 0
        self.alt.SetValue(str(alt))

    def OnAdd(self, event):
        if self.Validate() and self.splace.Validate() and self.szone.Validate() and self.salt.Validate():
            item = []
            item.append(self.birthplace.GetValue())
            dirtxt = 'E'
            if self.placerbW.GetValue():
                dirtxt = 'W'
            lon = self.londeg.GetValue().zfill(2) + dirtxt + self.lonmin.GetValue().zfill(2)
            item.append(lon)
            dirtxt = 'N'
            if self.placerbS.GetValue():
                dirtxt = 'S'
            lat = self.latdeg.GetValue().zfill(2) + dirtxt + self.latmin.GetValue().zfill(2)
            item.append(lat)
            sign = '+'
            if self.pluscb.GetCurrentSelection() == 1:
                sign = '-'
            zone = sign + self.zhour.GetValue() + ':' + self.zminute.GetValue().zfill(2)
            item.append(zone)
            alt = self.alt.GetValue()
            item.append(alt)
            self.li.OnAdd(item)

    def OnRemove(self, event):
        self.li.OnRemove()

    def OnRemoveAll(self, event):
        self.li.OnRemoveAll()

    def onOK(self, event):
        self.li.save()
        self.Close()
        self.SetReturnCode(wx.ID_OK)
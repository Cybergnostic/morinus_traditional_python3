# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import sys
import wx
import intvalidator
import placedb
import geonames
import mtexts
import util
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class PlaceListCtrl(wx.ListCtrl):
    PLACE = 0
    COUNTRY = 1
    LON = 2
    LAT = 3
    ZONE = 4
    ALT = 5
    COLNUM = ALT + 1

    def __init__(self, parent, li, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        self.placedata = {}
        self.load(li)
        self.Populate()
        self.Id = ID
        self.changed = False

    def Populate(self):
        self.InsertColumn(PlaceListCtrl.PLACE, mtexts.txtsplacesdlg['Place'])
        self.InsertColumn(PlaceListCtrl.COUNTRY, mtexts.txtsplacesdlg['Country'])
        self.InsertColumn(PlaceListCtrl.LON, mtexts.txtsplacesdlg['Long'] + '.')
        self.InsertColumn(PlaceListCtrl.LAT, mtexts.txtsplacesdlg['Lat'] + '.')
        self.InsertColumn(PlaceListCtrl.ZONE, mtexts.txtsplacesdlg['Zone'])
        self.InsertColumn(PlaceListCtrl.ALT, mtexts.txtsplacesdlg['Alt'] + '.')
        self.fillRows()
        self.SetColumnWidth(PlaceListCtrl.PLACE, 200)
        self.SetColumnWidth(PlaceListCtrl.COUNTRY, 180)
        self.SetColumnWidth(PlaceListCtrl.LON, 60)
        self.SetColumnWidth(PlaceListCtrl.LAT, 60)
        self.SetColumnWidth(PlaceListCtrl.ZONE, 60)
        self.SetColumnWidth(PlaceListCtrl.ALT, 60)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

    def reload(self, li):
        """Shows another list of places (the atlas search as you type)."""
        self.DeleteAllItems()
        self.placedata = {}
        self.load(li)
        self.fillRows()

    def fillRows(self):
        items = list(self.placedata.items())
        for key, data in items:
            index = self.InsertItem(self.GetItemCount(), data[0])
            self.SetItem(index, PlaceListCtrl.PLACE, data[0])
            self.SetItem(index, PlaceListCtrl.COUNTRY, data[1])
            self.SetItem(index, PlaceListCtrl.LON, data[2])
            self.SetItem(index, PlaceListCtrl.LAT, data[3])
            self.SetItem(index, PlaceListCtrl.ZONE, data[4])
            self.SetItem(index, PlaceListCtrl.ALT, data[5])
            self.SetItemData(index, key)

        self.currentItem = -1
        if len(self.placedata):
            self.currentItem = 0
            self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def GetListCtrl(self):
        return self

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemSelected(self, event):
        self.currentItem = event.GetIndex()
        event.Skip()

    def OnColClick(self, event):
        event.Skip()

    def load(self, li):
        idx = 1
        for it in li:
            dirtxt = 'E'
            lon = it[geonames.Geonames.LON]
            if lon < 0.0:
                dirtxt = 'W'
                lon *= -1
            d, m, s = util.decToDeg(lon)
            lontxt = str(d).zfill(2) + dirtxt + str(m).zfill(2)
            dirtxt = 'N'
            lat = it[geonames.Geonames.LAT]
            if lat < 0.0:
                dirtxt = 'S'
                lat *= -1
            d, m, s = util.decToDeg(lat)
            lattxt = str(d).zfill(2) + dirtxt + str(m).zfill(2)
            gmtoffs = it[geonames.Geonames.GMTOFFS]
            signtxt = '+'
            if gmtoffs < 0.0:
                signtxt = '-'
                gmtoffs *= -1
            frac = int((gmtoffs - int(gmtoffs)) * 60.0)
            gmtoffstxt = signtxt + str(int(gmtoffs)) + ':' + str(frac).zfill(2)
            self.placedata[idx] = (
             it[geonames.Geonames.NAME], it[geonames.Geonames.COUNTRYNAME], lontxt, lattxt, gmtoffstxt, str(it[geonames.Geonames.ALTITUDE]))
            idx += 1


class PlacesListDlg(wx.Dialog):

    def __init__(self, parent, li, search=None, query=''):
        """With search (the atlas search), a field above the list searches
        again as you type; self.places is the list shown."""
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtsplacesdlg['Places'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.places = li
        self.search = search
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        if search is not None:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            hsizer.Add(wx.StaticText(self, -1, mtexts.txtsplacesdlg['Place'] + ':'), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.query = wx.TextCtrl(self, -1, query, size=(300, -1))
            self.query.SetHelpText('Name, or name, region or country (e.g. Springfield, Illinois)')
            hsizer.Add(self.query, 1, wx.ALL, 5)
            hsizer.Add(wx.StaticText(self, -1, 'Atlas: GeoNames (CC BY 4.0)'), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            mvsizer.Add(hsizer, 0, wx.GROW | wx.LEFT | wx.RIGHT | wx.TOP, 5)
            self.query.Bind(wx.EVT_TEXT, self.onQuery)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        splaces = wx.StaticBox(self, label='')
        placessizer = wx.StaticBoxSizer(splaces, wx.VERTICAL)
        ID_Places = wx.NewId()
        self.li = PlaceListCtrl(self, li, ID_Places, size=(650, 300), style=wx.LC_VRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL)
        placessizer.Add(self.li, 1, wx.GROW | wx.ALL, 5)
        mhsizer.Add(placessizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 0)
        mvsizer.Add(mhsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != '__WXMSW__':
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Ok'])
        btnOk.SetHelpText(mtexts.txtscommon['HelpOk'])
        btnOk.SetDefault()
        btnsizer.AddButton(btnOk)
        btn = wx.Button(self, wx.ID_CANCEL, mtexts.txtscommon['Cancel'])
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        btnOk.SetFocus()
        self.li.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onActivated)

    def onQuery(self, event):
        txt = self.query.GetValue()
        if len(txt.strip()) >= 2:
            self.places = self.search(txt)
            self.li.reload(self.places)

    def onActivated(self, event):
        # double-click (or Enter) on a place chooses it
        self.li.currentItem = event.GetIndex()
        self.EndModal(wx.ID_OK)
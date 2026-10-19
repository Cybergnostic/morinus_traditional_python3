# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import sys, os, wx, limchecklistctrlmixin, chart, mtexts, astrology, util

class FixedStars:

    class FixedStar:
        NAME = 0
        NOMNAME = 1

        def __init__(self, name, nomname):
            self.name = name
            self.nomname = nomname

    def __init__(self, ephepath):
        self.ephepath = ephepath
        self.jd = astrology.swe_julday(1950, 1, 1, 0.0, astrology.SE_GREG_CAL)
        self.data = []
        self.fname = os.path.join(self.ephepath, 'fixstars.cat')

    def read(self, names):
        for n in names:
            ret, name, dat, serr = astrology.swe_fixstar_ut(',' + n, self.jd, 0)
            nam = name[0].strip()
            nomnam = ''
            DELIMITER = ','
            if nam.find(DELIMITER) != -1:
                snam = nam.split(DELIMITER)
                nam = snam[0].strip()
                nomnam = snam[1].strip()
            self.data.append(FixedStars.FixedStar(nam, nomnam))

        return True


provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class FixedStarListCtrl(wx.ListCtrl, limchecklistctrlmixin.LimCheckListCtrlMixin):
    NUM = 0
    NAME = 1
    NOMNAME = 2
    MAX_SEL_NUM = 40

    def __init__(self, parent, ephepath, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        limchecklistctrlmixin.LimCheckListCtrlMixin.__init__(self, FixedStarListCtrl.MAX_SEL_NUM)
        self.parent = parent
        self.ephepath = ephepath
        self.fixedstardata = {}
        self.Id = ID
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

    def fill(self, names, sels):
        wx.WindowDisabler()
        wx.BeginBusyCursor()
        self.load(names)
        self.Populate()
        items = self.fixedstardata.iteritems()
        for k, v in items:
            for i in range(len(sels)):
                if sels[i]:
                    self.CheckItem(i)

        wx.EndBusyCursor()

    def Populate(self):
        self.InsertColumn(FixedStarListCtrl.NUM, '')
        self.InsertColumn(FixedStarListCtrl.NAME, mtexts.txtsfixedstarspddlg['Name'])
        self.InsertColumn(FixedStarListCtrl.NOMNAME, mtexts.txtsfixedstarspddlg['Nomencl'] + '.')
        items = self.fixedstardata.items()
        cnt = 0
        for key, data in items:
            cnt += 1
            index = self.InsertStringItem(sys.maxint, data[0])
            self.SetStringItem(index, FixedStarListCtrl.NUM, str(cnt) + '.')
            self.SetStringItem(index, FixedStarListCtrl.NAME, data[0])
            self.SetStringItem(index, FixedStarListCtrl.NOMNAME, data[1])
            self.SetItemData(index, key)

        self.SetColumnWidth(FixedStarListCtrl.NUM, 50)
        self.SetColumnWidth(FixedStarListCtrl.NAME, 120)
        self.SetColumnWidth(FixedStarListCtrl.NOMNAME, 80)

    def OnItemActivated(self, evt):
        self.ToggleItem(evt.m_itemIndex)

    def OnDeselectAll(self):
        items = self.fixedstardata.iteritems()
        for k, v in items:
            if self.IsChecked(k - 1):
                self.CheckItem(k - 1, False)

    def OnSelectAll(self):
        items = self.fixedstardata.iteritems()
        for k, v in items:
            if not self.IsChecked(k - 1):
                self.CheckItem(k - 1, True)

    def load(self, names):
        fs = FixedStars(self.ephepath)
        if fs.read(names):
            idx = 1
            for f in fs.data:
                self.fixedstardata[idx] = (
                 f.name, f.nomname)
                idx += 1

        else:
            txt = mtexts.txtsfiles['FileError'] + '(' + fs.fname + ')'
            dlgm = wx.MessageDialog(self, txt, mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlgm.ShowModal()
            dlgm.Destroy()


class FixedStarsPDDlg(wx.Dialog):

    def __init__(self, parent, options, pdfixedstarssel, ephepath):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, -1, mtexts.txtsfixedstarspddlg['FixedStars'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.PostCreate(pre)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        self.sstars = wx.StaticBox(self, label='')
        starssizer = wx.StaticBoxSizer(self.sstars, wx.VERTICAL)
        ID_FixedStars = wx.NewId()
        self.li = FixedStarListCtrl(self, ephepath, ID_FixedStars, size=(275, 280))
        starssizer.Add(self.li, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.li.fill(options.fixedstars, pdfixedstarssel)
        hbtnsizer = wx.BoxSizer(wx.HORIZONTAL)
        ID_SelectAll = wx.NewId()
        btnSelectAll = wx.Button(self, ID_SelectAll, mtexts.txtsfixedstarspddlg['SelectAll'])
        hbtnsizer.Add(btnSelectAll, 0)
        ID_DeselectAll = wx.NewId()
        btnDeselectAll = wx.Button(self, ID_DeselectAll, mtexts.txtsfixedstarspddlg['Reset'])
        hbtnsizer.Add(btnDeselectAll, 0)
        starssizer.Add(hbtnsizer, 0)
        mvsizer.Add(starssizer, 0, wx.LEFT | wx.RIGHT, 5)
        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=ID_SelectAll)
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=ID_DeselectAll)
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

    def OnDeselectAll(self, event):
        self.li.OnDeselectAll()

    def OnSelectAll(self, event):
        self.li.OnSelectAll()

    def getSelections(self):
        sels = []
        keys = self.li.fixedstardata.iterkeys()
        for k in keys:
            sels.append(self.li.IsChecked(k - 1))

        return sels[:]
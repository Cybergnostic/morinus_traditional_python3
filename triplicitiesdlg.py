# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import copy
import wx
import chart
import mtexts

class TriplicitiesDlg(wx.Dialog):

    def __init__(self, parent, opts):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtstriplicitiesdlg['Triplicities'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.trips = [
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None]]
        self.tripsval = copy.deepcopy(opts.trips)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        triplicityList = (
         mtexts.txtstriplicitiesdlg['Dorothean'], mtexts.txtstriplicitiesdlg['Ptolemaic'], mtexts.txtstriplicitiesdlg['Morinus'])
        self.triplicityListlen = len(triplicityList)
        self.cb = wx.ComboBox(self, -1, triplicityList[opts.seltrip], size=(150, -1), choices=triplicityList, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.cb.SetSelection(opts.seltrip)
        mvsizer.Add(self.cb, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 5)
        strips = wx.StaticBox(self, label='')
        tripssizer = wx.StaticBoxSizer(strips, wx.VERTICAL)
        num = len(self.trips)
        subnum = len(self.trips[0])
        gsizer = wx.FlexGridSizer(0, 2, 0, 0)
        label = wx.StaticText(self, -1, '')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        hsizercap = wx.BoxSizer(wx.HORIZONTAL)
        triplicities = (mtexts.txtstriplicitiesdlg['Fire'], mtexts.txtstriplicitiesdlg['Air'], mtexts.txtstriplicitiesdlg['Water'], mtexts.txtstriplicitiesdlg['Earth'])
        triptypes = (mtexts.txtstriplicitiesdlg['Primary'], mtexts.txtstriplicitiesdlg['Secondary'], mtexts.txtstriplicitiesdlg['Participating'])
        for i in range(subnum):
            label = wx.StaticText(self, -1, triptypes[i])
            hsizercap.Add(label, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        gsizer.Add(hsizercap, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        pls = (
         mtexts.txtscommon['Saturn'], mtexts.txtscommon['Jupiter'], mtexts.txtscommon['Mars'], mtexts.txtscommon['Sun'], mtexts.txtscommon['Venus'], mtexts.txtscommon['Mercury'], mtexts.txtscommon['Moon'])
        pls2 = (mtexts.txtscommon['Saturn'], mtexts.txtscommon['Jupiter'], mtexts.txtscommon['Mars'], mtexts.txtscommon['Sun'], mtexts.txtscommon['Venus'], mtexts.txtscommon['Mercury'], mtexts.txtscommon['Moon'], mtexts.txtscommon['None'])
        for i in range(num):
            label = wx.StaticText(self, -1, triplicities[i] + ':')
            gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            for j in range(subnum):
                chstxt = pls
                if j == 2:
                    chstxt = pls2
                self.trips[i][j] = wx.ComboBox(self, -1, chstxt[self.tripsval[opts.seltrip][i][j]], size=(90,
                                                                                                          -1), choices=chstxt, style=wx.CB_DROPDOWN | wx.CB_READONLY)
                self.trips[i][j].SetSelection(self.tripsval[opts.seltrip][i][j])
                hsizer.Add(self.trips[i][j], 0, wx.ALIGN_LEFT | wx.ALL, 5)

            gsizer.Add(hsizer, 0, wx.ALIGN_LEFT | wx.TOP, 2)

        tripssizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        mvsizer.Add(tripssizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, 5)
        self.oldidx = opts.seltrip
        btnsizer = wx.StdDialogButtonSizer()
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Ok'])
        btnsizer.AddButton(btnOk)
        btnOk.SetHelpText(mtexts.txtscommon['HelpOk'])
        btnOk.SetDefault()
        btn = wx.Button(self, wx.ID_CANCEL, mtexts.txtscommon['Cancel'])
        btnsizer.AddButton(btn)
        btn.SetHelpText(mtexts.txtscommon['HelpCancel'])
        btnsizer.Realize()
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        self.Bind(wx.EVT_COMBOBOX, self.onSelect, id=self.cb.GetId())
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        btnOk.SetFocus()
        return

    def onSelect(self, event):
        idx = event.GetSelection()
        num = len(self.trips)
        subnum = len(self.trips[0])
        for i in range(num):
            for j in range(subnum):
                self.tripsval[self.oldidx][i][j] = self.trips[i][j].GetCurrentSelection()
                self.trips[i][j].SetSelection(self.tripsval[idx][i][j])

        self.oldidx = idx

    def onOK(self, event):
        num = len(self.trips)
        subnum = len(self.trips[0])
        curridx = self.cb.GetCurrentSelection()
        for i in range(num):
            for j in range(subnum):
                self.tripsval[curridx][i][j] = self.trips[i][j].GetCurrentSelection()

        self.Close()
        self.SetReturnCode(wx.ID_OK)

    def check(self, opts):
        changed = False
        if opts.seltrip != self.cb.GetCurrentSelection():
            opts.seltrip = self.cb.GetCurrentSelection()
            changed = True
        num = len(self.trips)
        subnum = len(self.trips[0])
        for typ in range(self.triplicityListlen):
            for i in range(num):
                for j in range(subnum):
                    if self.tripsval[typ][i][j] != opts.trips[typ][i][j]:
                        opts.trips[typ][i][j] = self.tripsval[typ][i][j]
                        changed = True

        return changed
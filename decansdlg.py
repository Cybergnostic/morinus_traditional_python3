# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import copy, wx, mtexts

class DecansDlg(wx.Dialog):

    def __init__(self, parent, opts):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtsdecansdlg['Decans'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.decans = [
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None],
         [
          None, None, None]]
        self.decansval = copy.deepcopy(opts.decans)
        DIFF = 5
        if opts.netbook:
            DIFF = 2
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        decanList = (
         mtexts.txtsdecansdlg['Chaldean'], mtexts.txtsdecansdlg['Triplicity'])
        self.decanListLen = len(decanList)
        self.cb = wx.ComboBox(self, -1, decanList[opts.seldecan], size=(150, -1), choices=decanList, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.cb.SetSelection(opts.seldecan)
        mvsizer.Add(self.cb, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 5)
        sdecans = wx.StaticBox(self, label='')
        decanssizer = wx.StaticBoxSizer(sdecans, wx.VERTICAL)
        num = len(self.decans)
        subnum = len(self.decans[0])
        gsizer = wx.FlexGridSizer(num, 2, 0, 0)
        signs = (mtexts.txtscommon['Aries'], mtexts.txtscommon['Taurus'], mtexts.txtscommon['Gemini'], mtexts.txtscommon['Cancer'], mtexts.txtscommon['Leo'], mtexts.txtscommon['Virgo'], mtexts.txtscommon['Libra'], mtexts.txtscommon['Scorpio'], mtexts.txtscommon['Sagittarius'], mtexts.txtscommon['Capricorn'], mtexts.txtscommon['Aquarius'], mtexts.txtscommon['Pisces'])
        pls = (mtexts.txtscommon['Saturn'], mtexts.txtscommon['Jupiter'], mtexts.txtscommon['Mars'], mtexts.txtscommon['Sun'], mtexts.txtscommon['Venus'], mtexts.txtscommon['Mercury'], mtexts.txtscommon['Moon'])
        for i in range(num):
            label = wx.StaticText(self, -1, signs[i] + ':')
            gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, DIFF)
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            for j in range(subnum):
                self.decans[i][j] = wx.ComboBox(self, -1, pls[self.decansval[opts.seldecan][i][j]], size=(90,
                                                                                                          -1), choices=pls, style=wx.CB_DROPDOWN | wx.CB_READONLY)
                self.decans[i][j].SetSelection(self.decansval[opts.seldecan][i][j])
                hsizer.Add(self.decans[i][j], 0, wx.ALIGN_LEFT | wx.ALL, DIFF)

            gsizer.Add(hsizer, 0, wx.ALIGN_LEFT | wx.TOP, 2)

        decanssizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        mvsizer.Add(decanssizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, 5)
        btnsizer = wx.StdDialogButtonSizer()
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Ok'])
        btnsizer.AddButton(btnOk)
        btnOk.SetHelpText(mtexts.txtscommon['HelpOk'])
        btnOk.SetDefault()
        btn = wx.Button(self, wx.ID_CANCEL, mtexts.txtscommon['Cancel'])
        btnsizer.AddButton(btn)
        btn.SetHelpText(mtexts.txtscommon['HelpCancel'])
        btnsizer.Realize()
        DIFF = 10
        if opts.netbook:
            DIFF = 2
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, DIFF)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        self.Bind(wx.EVT_COMBOBOX, self.onSelect, id=self.cb.GetId())
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        btnOk.SetFocus()
        return

    def onSelect(self, event):
        idx = event.GetSelection()
        oldidx = 0
        if idx == 0:
            oldidx = 1
        num = len(self.decans)
        subnum = len(self.decans[0])
        for i in range(num):
            for j in range(subnum):
                self.decansval[oldidx][i][j] = self.decans[i][j].GetCurrentSelection()
                self.decans[i][j].SetSelection(self.decansval[idx][i][j])

    def onOK(self, event):
        num = len(self.decans)
        subnum = len(self.decans[0])
        curridx = self.cb.GetCurrentSelection()
        for i in range(num):
            for j in range(subnum):
                self.decansval[curridx][i][j] = self.decans[i][j].GetCurrentSelection()

        self.Close()
        self.SetReturnCode(wx.ID_OK)

    def check(self, opts):
        changed = False
        if opts.seldecan != self.cb.GetCurrentSelection():
            opts.seldecan = self.cb.GetCurrentSelection()
            changed = True
        num = len(self.decans)
        subnum = len(self.decans[0])
        for typ in range(self.decanListLen):
            for i in range(num):
                for j in range(subnum):
                    if self.decansval[typ][i][j] != opts.decans[typ][i][j]:
                        opts.decans[typ][i][j] = self.decansval[typ][i][j]
                        changed = True

        return changed
# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import chart
import mtexts
import util

class ProfTableMonDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self)
        self.Create(parent, -1, mtexts.txtsproftablemondlg['MonthlyProfections'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        sselection = wx.StaticBox(self, label='')
        selectionsizer = wx.StaticBoxSizer(sselection, wx.VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.steps12rb = wx.RadioButton(self, -1, mtexts.txtsproftablemondlg['Steps12'], style=wx.RB_GROUP)
        vsizer.Add(self.steps12rb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        self.steps13rb = wx.RadioButton(self, -1, mtexts.txtsproftablemondlg['Steps13'])
        vsizer.Add(self.steps13rb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        selectionsizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        mvsizer.Add(selectionsizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, 5)
        btnsizer = wx.StdDialogButtonSizer()
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

    def initialize(self):
        self.steps12rb.SetValue(True)
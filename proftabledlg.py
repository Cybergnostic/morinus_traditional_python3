# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import chart
import intvalidator
import rangechecker
import mtexts
import util

class ProfTableDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self)
        self.Create(parent, -1, mtexts.txtsproftabledlg['Profections'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        sselection = wx.StaticBox(self, label='')
        selectionsizer = wx.StaticBoxSizer(sselection, wx.VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.mainrb = wx.RadioButton(self, -1, mtexts.txtsproftabledlg['ProfsMainSignificatorsOnly'], style=wx.RB_GROUP)
        vsizer.Add(self.mainrb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        self.allrb = wx.RadioButton(self, -1, mtexts.txtsproftabledlg['ProfsAll'])
        vsizer.Add(self.allrb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
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
        self.mainrb.SetValue(True)
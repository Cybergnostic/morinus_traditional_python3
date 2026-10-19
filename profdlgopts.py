# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import chart
import intvalidator
import rangechecker
import mtexts
import util

class ProfDlgOpts(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self)
        self.Create(parent, -1, mtexts.txtsprofdlgopts['Profections'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        sselection = wx.StaticBox(self, label='')
        selectionsizer = wx.StaticBoxSizer(sselection, wx.VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.zodiacalrb = wx.RadioButton(self, -1, mtexts.txtsprofdlgopts['ZodiacalAnnualProfection'], style=wx.RB_GROUP)
        vsizer.Add(self.zodiacalrb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        self.mundanerb = wx.RadioButton(self, -1, mtexts.txtsprofdlgopts['PlacidianAnnualProfection'])
        vsizer.Add(self.mundanerb, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        self.usezodprojsckb = wx.CheckBox(self, -1, mtexts.txtsprofdlgopts['UseZodProjs'])
        self.usezodprojsckb.Enable(False)
        vsubsizer.Add(self.usezodprojsckb, 0, wx.ALL, 2)
        vsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.LEFT, 12)
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
        self.Bind(wx.EVT_RADIOBUTTON, self.onMundane, id=self.mundanerb.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.onZodiacal, id=self.zodiacalrb.GetId())

    def onMundane(self, event):
        self.usezodprojsckb.Enable(True)

    def onZodiacal(self, event):
        self.usezodprojsckb.Enable(False)
        self.usezodprojsckb.SetValue(False)

    def fill(self, opts):
        if opts.zodprof:
            self.zodiacalrb.SetValue(True)
        else:
            self.mundanerb.SetValue(True)
            self.usezodprojsckb.Enable(True)
        self.usezodprojsckb.SetValue(opts.usezodprojsprof)

    def check(self, opts):
        changed = False
        if opts.zodprof != self.zodiacalrb.GetValue():
            opts.zodprof = self.zodiacalrb.GetValue()
            changed = True
        if opts.usezodprojsprof != self.usezodprojsckb.GetValue():
            opts.usezodprojsprof = self.usezodprojsckb.GetValue()
            changed = True
        return changed
# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import syzygy
import mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class SyzygyDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtssyzygydlg['Syzygy'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        ssyzygy = wx.StaticBox(self, label='')
        syzygysizer = wx.StaticBoxSizer(ssyzygy, wx.VERTICAL)
        self.syzmoonrb = wx.RadioButton(self, -1, mtexts.txtssyzygydlg['SyzMoon'], style=wx.RB_GROUP)
        syzygysizer.Add(self.syzmoonrb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        self.syzaboverb = wx.RadioButton(self, -1, mtexts.txtssyzygydlg['SyzAbove'])
        syzygysizer.Add(self.syzaboverb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        self.syzabovenatalrb = wx.RadioButton(self, -1, mtexts.txtssyzygydlg['SyzAboveNatal'])
        syzygysizer.Add(self.syzabovenatalrb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        mvsizer.Add(syzygysizer, 0, wx.GROW | wx.ALL, 5)
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

    def fill(self, opts):
        if opts.syzmoon == syzygy.Syzygy.MOON:
            self.syzmoonrb.SetValue(True)
        elif opts.syzmoon == syzygy.Syzygy.ABOVEHOR:
            self.syzaboverb.SetValue(True)
        else:
            self.syzabovenatalrb.SetValue(True)

    def check(self, opts):
        changed = False
        if opts.syzmoon != syzygy.Syzygy.MOON and self.syzmoonrb.GetValue():
            opts.syzmoon = syzygy.Syzygy.MOON
            changed = True
        elif opts.syzmoon != syzygy.Syzygy.ABOVEHOR and self.syzaboverb.GetValue():
            opts.syzmoon = syzygy.Syzygy.ABOVEHOR
            changed = True
        elif opts.syzmoon != syzygy.Syzygy.ABOVEHORNATAL and self.syzabovenatalrb.GetValue():
            opts.syzmoon = syzygy.Syzygy.ABOVEHORNATAL
            changed = True
        return changed
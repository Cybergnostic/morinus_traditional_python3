# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, mtexts
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class FirdariaDlg(wx.Dialog):

    def __init__(self, parent):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, -1, mtexts.txtsfirdariadlg['Firdaria'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.PostCreate(pre)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        sfirdaria = wx.StaticBox(self, label=mtexts.txtsfirdariadlg['Nocturnal'])
        firdariasizer = wx.StaticBoxSizer(sfirdaria, wx.VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.bonrb = wx.RadioButton(self, -1, mtexts.txtsfirdariadlg['Bonatus'], style=wx.RB_GROUP)
        vsizer.Add(self.bonrb, 0, wx.ALIGN_CENTER, 5)
        self.birrb = wx.RadioButton(self, -1, mtexts.txtsfirdariadlg['AlBiruni'])
        vsizer.Add(self.birrb, 0, wx.ALIGN_CENTER, 5)
        firdariasizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        mvsizer.Add(firdariasizer, 0, wx.GROW | wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != '__WXMSW__':
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
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
        btnOk.SetFocus()

    def fill(self, opts):
        if opts.isfirbonatti:
            self.bonrb.SetValue(True)
        else:
            self.birrb.SetValue(True)

    def check(self, opts):
        changed = self.bonrb.GetValue() != opts.isfirbonatti
        if changed:
            opts.isfirbonatti = self.bonrb.GetValue()
        return changed
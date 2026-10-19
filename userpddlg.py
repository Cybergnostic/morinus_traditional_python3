# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, chart, intvalidator, mtexts, util
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class UserPDDlg(wx.Dialog):

    def __init__(self, parent, titletxt):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, -1, titletxt, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.PostCreate(pre)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        fgsizer = wx.FlexGridSizer(2, 4)
        self.suser = wx.StaticBox(self, label='')
        usersizer = wx.StaticBoxSizer(self.suser, wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsuserpddlg['Long'] + ':')
        fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsuserpddlg['Deg'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.londeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,
                                                                                                   -1))
        self.londeg.SetHelpText(mtexts.txtsuserpddlg['HelpPDDeg'])
        self.londeg.SetMaxLength(3)
        vvsizer.Add(self.londeg, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsuserpddlg['Min'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.lonmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.lonmin.SetHelpText(mtexts.txtsuserpddlg['HelpMin'])
        self.lonmin.SetMaxLength(2)
        vvsizer.Add(self.lonmin, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsuserpddlg['Sec'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.lonsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.lonsec.SetHelpText(mtexts.txtsuserpddlg['HelpMin'])
        self.lonsec.SetMaxLength(2)
        vvsizer.Add(self.lonsec, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        label = wx.StaticText(self, -1, mtexts.txtsuserpddlg['Lat'] + ':')
        fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsuserpddlg['Deg'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.latdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 90), size=(40,
                                                                                                  -1))
        self.latdeg.SetHelpText(mtexts.txtsuserpddlg['HelpLatDeg'])
        self.latdeg.SetMaxLength(2)
        vvsizer.Add(self.latdeg, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsuserpddlg['Min'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.latmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.latmin.SetHelpText(mtexts.txtsuserpddlg['HelpMin'])
        self.latmin.SetMaxLength(2)
        vvsizer.Add(self.latmin, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsuserpddlg['Sec'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.latsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.latsec.SetHelpText(mtexts.txtsuserpddlg['HelpMin'])
        self.latsec.SetMaxLength(2)
        vvsizer.Add(self.latsec, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvvsizer = wx.BoxSizer(wx.VERTICAL)
        vvvsizer.Add(fgsizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.southernckb = wx.CheckBox(self, -1, mtexts.txtsuserpddlg['SouthernLatitude'])
        vvvsizer.Add(self.southernckb, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        usersizer.Add(vvvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        mvsizer.Add(usersizer, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT, 5)
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
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.londeg.SetFocus()

    def onOK(self, event):
        if self.Validate() and self.suser.Validate():
            self.Close()
            self.SetReturnCode(wx.ID_OK)

    def initialize(self, londata, latdata, southern):
        londeg, lonmin, lonsec = str(londata[0]), str(londata[1]), str(londata[2])
        latdeg, latmin, latsec = str(latdata[0]), str(latdata[1]), str(latdata[2])
        self.londeg.SetValue(str(londeg))
        self.lonmin.SetValue(str(lonmin))
        self.lonsec.SetValue(str(lonsec))
        self.latdeg.SetValue(str(latdeg))
        self.latmin.SetValue(str(latmin))
        self.latsec.SetValue(str(latsec))
        self.southernckb.SetValue(southern)

    def check(self, londata, latdata, southern):
        changed = False
        if londata[0] != int(self.londeg.GetValue()):
            changed = True
        elif londata[1] != int(self.lonmin.GetValue()):
            changed = True
        elif londata[2] != int(self.lonsec.GetValue()):
            changed = True
        elif latdata[0] != int(self.latdeg.GetValue()):
            changed = True
        elif latdata[1] != int(self.latmin.GetValue()):
            changed = True
        elif latdata[2] != int(self.latsec.GetValue()):
            changed = True
        elif southern != self.southernckb.GetValue():
            changed = True
        return changed
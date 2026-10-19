# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import copy
import string
import wx
import chart
import util
import mtexts

class IntValidator(wx.Validator):

    def __init__(self, minim=None, maxim=None):
        wx.Validator.__init__(self)
        self.minim = minim
        self.maxim = maxim
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return IntValidator(self.minim, self.maxim)

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        if val == '':
            dlgm = wx.MessageDialog(None, mtexts.txtstermsdlg['NumFieldsCannotBeEmpty'], mtexts.txtstermsdlg['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return False
        else:
            if self.minim != None and int(val) < self.minim or self.maxim != None and int(val) >= self.maxim:
                s = mtexts.txtstermsdlg['RangeError2']
                if self.maxim != None:
                    s = mtexts.txtstermsdlg['RangeError3'] + '%2d' % self.maxim
                dlgm = wx.MessageDialog(None, s, mtexts.txtstermsdlg['Error'], wx.OK | wx.ICON_EXCLAMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
                return False
            return True

    def OnChar(self, event):
        key = event.KeyCode
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if chr(key) in string.digits:
            event.Skip()
            return
        if not wx.Validator.IsSilent():
            wx.Bell()


class TermsDlg(wx.Dialog):

    def __init__(self, parent, opts):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtstermsdlg['Terms'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.terms = [
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]],
         [
          [
           None, None], [None, None], [None, None], [None, None], [None, None]]]
        self.termsval = copy.deepcopy(opts.terms)
        DIFF = 5
        if opts.netbook:
            DIFF = 2
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        self.termList = (
         mtexts.txtstermsdlg['Egyptian'], mtexts.txtstermsdlg['Ptolemaic'])
        self.termListlen = len(self.termList)
        self.cb = wx.ComboBox(self, -1, self.termList[opts.selterm], size=(150, -1), choices=self.termList, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.cb.SetSelection(opts.selterm)
        mvsizer.Add(self.cb, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 5)
        sterms = wx.StaticBox(self, label='')
        termssizer = wx.StaticBoxSizer(sterms, wx.VERTICAL)
        num = len(self.terms)
        subnum = len(self.terms[0])
        gsizer = wx.FlexGridSizer(0, 2, 0, 0)
        self.signs = (mtexts.txtscommon['Aries'], mtexts.txtscommon['Taurus'], mtexts.txtscommon['Gemini'], mtexts.txtscommon['Cancer'], mtexts.txtscommon['Leo'], mtexts.txtscommon['Virgo'], mtexts.txtscommon['Libra'], mtexts.txtscommon['Scorpio'], mtexts.txtscommon['Sagittarius'], mtexts.txtscommon['Capricorn'], mtexts.txtscommon['Aquarius'], mtexts.txtscommon['Pisces'])
        pls = (mtexts.txtscommon['Saturn'], mtexts.txtscommon['Jupiter'], mtexts.txtscommon['Mars'], mtexts.txtscommon['Sun'], mtexts.txtscommon['Venus'], mtexts.txtscommon['Mercury'], mtexts.txtscommon['Moon'])
        for i in range(num):
            label = wx.StaticText(self, -1, self.signs[i] + ':')
            gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, DIFF)
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            for j in range(subnum):
                hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
                self.terms[i][j][0] = wx.ComboBox(self, -1, pls[self.termsval[opts.selterm][i][j][0]], size=(90,
                                                                                                             -1), choices=pls, style=wx.CB_DROPDOWN | wx.CB_READONLY)
                self.terms[i][j][0].SetSelection(self.termsval[opts.selterm][i][j][0])
                hsubsizer.Add(self.terms[i][j][0], 0, wx.ALIGN_LEFT)
                self.terms[i][j][1] = wx.TextCtrl(self, -1, str(self.termsval[opts.selterm][i][j][1]), validator=IntValidator(0, 20), size=(30,
                                                                                                                                            -1))
                self.terms[i][j][1].SetMaxLength(2)
                hsubsizer.Add(self.terms[i][j][1], 0, wx.ALIGN_LEFT)
                hsizer.Add(hsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, DIFF)

            gsizer.Add(hsizer, 0, wx.ALIGN_LEFT | wx.TOP, 2)

        termssizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        mvsizer.Add(termssizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, 5)
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
        if self.Validate():
            num = len(self.terms)
            subnum = len(self.terms[0])
            for i in range(num):
                for j in range(subnum):
                    self.termsval[oldidx][i][j][0] = self.terms[i][j][0].GetCurrentSelection()
                    self.termsval[oldidx][i][j][1] = int(self.terms[i][j][1].GetValue())
                    self.terms[i][j][0].SetSelection(self.termsval[idx][i][j][0])
                    self.terms[i][j][1].SetValue(str(self.termsval[idx][i][j][1]))

        else:
            self.cb.SetSelection(oldidx)

    def onOK(self, event):
        if self.Validate():
            num = len(self.terms)
            subnum = len(self.terms[0])
            curridx = self.cb.GetCurrentSelection()
            for i in range(num):
                for j in range(subnum):
                    self.termsval[curridx][i][j][0] = self.terms[i][j][0].GetCurrentSelection()
                    self.termsval[curridx][i][j][1] = int(self.terms[i][j][1].GetValue())

            OK = 0
            MULTIPLANETS = 1
            NOT30 = 2
            errcode = OK
            for typ in range(self.termListlen):
                for i in range(num):
                    summa = 0
                    pls = [False, False, False, False, False, False, False]
                    for j in range(subnum):
                        if not pls[self.termsval[typ][i][j][0]]:
                            pls[self.termsval[typ][i][j][0]] = True
                        else:
                            errcode = 1
                            summa = chart.Chart.SIGN_DEG
                            break
                        summa += self.termsval[typ][i][j][1]

                    if summa != chart.Chart.SIGN_DEG:
                        errcode = 2
                    if errcode != 0:
                        break

                if errcode != 0:
                    break

            if errcode == OK:
                self.Close()
                self.SetReturnCode(wx.ID_OK)
            else:
                txt = mtexts.txtstermsdlg['MultiPlanets'] + '(' + self.termList[typ] + ',' + self.signs[i] + ')'
                if errcode == NOT30:
                    txt = mtexts.txtstermsdlg['NOT30'] + '(' + self.termList[typ] + ',' + self.signs[i] + ')'
                dlgm = wx.MessageDialog(None, txt, mtexts.txtstermsdlg['Error'], wx.OK | wx.ICON_EXCLAMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
        return

    def check(self, opts):
        changed = False
        if opts.selterm != self.cb.GetCurrentSelection():
            opts.selterm = self.cb.GetCurrentSelection()
            changed = True
        num = len(self.terms)
        subnum = len(self.terms[0])
        for typ in range(self.termListlen):
            for i in range(num):
                for j in range(subnum):
                    if self.termsval[typ][i][j][0] != opts.terms[typ][i][j][0] or self.termsval[typ][i][j][1] != opts.terms[typ][i][j][1]:
                        opts.terms[typ][i][j][0] = self.termsval[typ][i][j][0]
                        opts.terms[typ][i][j][1] = self.termsval[typ][i][j][1]
                        changed = True

        return changed
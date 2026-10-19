# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, string, mtexts

class FloatValidator(wx.PyValidator):

    def __init__(self, minim=None, maxim=None):
        wx.PyValidator.__init__(self)
        self.minim = minim
        self.maxim = maxim
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return FloatValidator(self.minim, self.maxim)

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        if val == '':
            dlgm = wx.MessageDialog(None, mtexts.txtsvalidators['FieldsCannotBeEmpty'], mtexts.txtsvalidators['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return False
        else:
            if self.minim != None and float(val) < self.minim or self.maxim != None and float(val) >= self.maxim:
                s = mtexts.txtsvalidators['RangeError2']
                if self.maxim != None:
                    s = mtexts.txtsvalidators['RangeError3'] + '%2.1f' % self.maxim
                dlgm = wx.MessageDialog(None, s, mtexts.txtsvalidators['Error'], wx.OK | wx.ICON_EXCLAMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
                return False
            return True

    def OnChar(self, event):
        key = event.KeyCode
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        tc = self.GetWindow()
        val = tc.GetValue()
        dot = False
        for x in val:
            if x == '.':
                dot = True

        if chr(key) in string.digits or not dot and chr(key) == '.':
            event.Skip()
            return
        if not wx.Validator_IsSilent():
            wx.Bell()
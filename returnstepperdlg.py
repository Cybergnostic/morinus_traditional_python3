"""Stepper for a solar or lunar return window: previous / next return
(a year for solar returns, a lunar month for lunar returns)."""

import i18n
import wx
import chart
import returnslist
import util


class ReturnStepperDlg(wx.Dialog):
    def __init__(self, parent, radix):
        self.solar = parent.chart.htype == chart.Chart.SOLAR
        wx.Dialog.__init__(self, parent, -1, i18n.tr('Solar returns' if self.solar else 'Lunar returns'), style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        self.radix = radix
        self.label = wx.StaticText(self, -1, '', style=wx.ALIGN_CENTRE_HORIZONTAL)
        prev = wx.Button(self, -1, '<  ' + i18n.tr('Previous year' if self.solar else 'Previous return'), size=(170, 36))
        nxt = wx.Button(self, -1, i18n.tr('Next year' if self.solar else 'Next return') + '  >', size=(170, 36))
        close = wx.Button(self, wx.ID_CLOSE)
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(prev, 0, wx.ALL, 5)
        buttons.Add(nxt, 0, wx.ALL, 5)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(buttons, 0, wx.ALL, 5)
        sizer.Add(close, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.SetSizerAndFit(sizer)
        prev.Bind(wx.EVT_BUTTON, lambda e: self.step(False))
        nxt.Bind(wx.EVT_BUTTON, lambda e: self.step(True))
        # modeless: Close() would only emulate a button, so the dialog is destroyed
        close.Bind(wx.EVT_BUTTON, lambda e: self.Destroy())
        self.Bind(wx.EVT_CLOSE, lambda e: self.Destroy())
        self.updateLabel()

    def updateLabel(self):
        t = self.parent.chart.time
        h, m, s = util.decToDeg(t.time)
        self.label.SetLabel('%s  %04d-%02d-%02d  %02d:%02d:%02d UT' % (i18n.tr('Solar return' if self.solar else 'Lunar return'), t.year, t.month, t.day, h, m, s))
        self.Layout()

    def step(self, forward):
        wait = wx.BusyCursor()
        chrt = returnslist.step_return(self.radix, self.parent.chart, forward)
        if chrt is None:
            wx.MessageBox(i18n.tr('The next return could not be computed.' if forward else 'The previous return could not be computed.'), '', wx.OK | wx.ICON_INFORMATION, self)
            return
        self.parent.change(chrt)
        self.updateLabel()

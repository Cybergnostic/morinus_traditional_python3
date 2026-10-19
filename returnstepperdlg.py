"""Stepper for a solar or lunar return window: previous / next return
(a year for solar returns, a lunar month for lunar returns)."""

import wx
import chart
import returnslist
import util


class ReturnStepperDlg(wx.Dialog):
    def __init__(self, parent, radix):
        self.solar = parent.chart.htype == chart.Chart.SOLAR
        wx.Dialog.__init__(self, parent, -1, 'Solar returns' if self.solar else 'Lunar returns', style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        self.radix = radix
        unit = 'year' if self.solar else 'return'
        self.label = wx.StaticText(self, -1, '', style=wx.ALIGN_CENTRE_HORIZONTAL)
        prev = wx.Button(self, -1, '<  Previous '+unit, size=(170, 36))
        nxt = wx.Button(self, -1, 'Next '+unit+'  >', size=(170, 36))
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
        close.Bind(wx.EVT_BUTTON, lambda e: self.Close())
        self.updateLabel()

    def updateLabel(self):
        t = self.parent.chart.time
        h, m, s = util.decToDeg(t.time)
        self.label.SetLabel('%s return  %04d-%02d-%02d  %02d:%02d:%02d UT' % ('Solar' if self.solar else 'Lunar', t.year, t.month, t.day, h, m, s))
        self.Layout()

    def step(self, forward):
        wait = wx.BusyCursor()
        chrt = returnslist.step_return(self.radix, self.parent.chart, forward)
        if chrt is None:
            wx.MessageBox('The %s return could not be computed.' % ('next' if forward else 'previous'), '', wx.OK | wx.ICON_INFORMATION, self)
            return
        self.parent.change(chrt)
        self.updateLabel()

"""Side-by-side single-chart wheels, without changing GraphChart."""
import os
import wx
import graphchart


def caption(chrt):
    t = chrt.time
    year = '%d BC' % t.origyear if t.bc else str(t.origyear)
    return '%s - %s-%02d-%02d %02d:%02d' % (
        chrt.name, year, t.origmonth, t.origday, t.hour, t.minute)


class ChartPicker(wx.Panel):
    """Choose radix, an open transit/return/lunation, or a saved .hor chart."""

    def __init__(self, parent, mainfr, on_change):
        wx.Panel.__init__(self, parent)
        self.mainfr = mainfr
        self.on_change = on_change
        self.loaded = []
        self.sources = []
        line = wx.BoxSizer(wx.HORIZONTAL)
        self.choice = wx.Choice(self)
        self.openbutton = wx.Button(self, label='Open chart file...')
        self.refreshbutton = wx.Button(self, label='Refresh')
        line.Add(self.choice, 1, wx.EXPAND | wx.RIGHT, 5)
        line.Add(self.openbutton, 0, wx.RIGHT, 5)
        line.Add(self.refreshbutton, 0)
        self.SetSizer(line)
        self.Bind(wx.EVT_CHOICE, self.changed, self.choice)
        self.Bind(wx.EVT_BUTTON, self.open_file, self.openbutton)
        self.Bind(wx.EVT_BUTTON, self.refresh, self.refreshbutton)
        self.refresh()

    def refresh(self, event=None):
        previous = self.selected()
        sources = [('Radix: ' + caption(self.mainfr.horoscope),
                    self.mainfr.horoscope)]
        # TransitFrame also hosts return charts and the lunation event charts.
        import transitframe
        for w in wx.GetTopLevelWindows():
            if isinstance(w, transitframe.TransitFrame) and not w.IsBeingDeleted():
                chrt = w.chart
                sources.append(('Open: ' + caption(chrt), chrt))
        for fpath, chrt in self.loaded:
            sources.append(('File: ' + caption(chrt), chrt))
        self.sources = sources
        self.choice.Clear()
        for title, _ in sources:
            self.choice.Append(title)
        selected = next((i for i, (_, chrt) in enumerate(sources)
                         if chrt is previous), 0)
        self.choice.SetSelection(selected)
        if event is not None:
            self.on_change()

    def selected(self):
        i = self.choice.GetSelection()
        return self.sources[i][1] if 0 <= i < len(self.sources) else self.mainfr.horoscope

    def changed(self, event):
        self.on_change()

    def open_file(self, event):
        dlg = wx.FileDialog(self, 'Open chart', self.mainfr.fpathhors, '',
                            'Morinus charts (*.hor)|*.hor',
                            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        try:
            if dlg.ShowModal() != wx.ID_OK:
                return
            path = dlg.GetPath()
        finally:
            dlg.Destroy()
        chrt = self.mainfr.subLoad(path, os.path.dirname(path), dontclose=True)
        if chrt is not None:
            self.loaded.append((path, chrt))
            self.refresh()
            self.choice.SetSelection(len(self.sources) - 1)
            self.on_change()


class WheelCell(wx.Panel):
    def __init__(self, parent, mainfr):
        wx.Panel.__init__(self, parent)
        self.mainfr = mainfr
        self.buffer = None
        self.pending = None
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.heading = wx.StaticText(self, label='')
        self.picker = ChartPicker(self, mainfr, self.queue_draw)
        self.canvas = wx.Panel(self)
        self.canvas.SetMinSize((200, 200))
        self.canvas.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.canvas.Bind(wx.EVT_PAINT, self.paint)
        self.canvas.Bind(wx.EVT_SIZE, self.resize)
        sizer.Add(self.heading, 0, wx.BOTTOM, 4)
        sizer.Add(self.picker, 0, wx.EXPAND | wx.BOTTOM, 5)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(sizer)
        wx.CallAfter(self.queue_draw)

    def resize(self, event):
        self.queue_draw()
        event.Skip()

    def queue_draw(self):
        if self.pending is None:
            self.pending = wx.CallLater(90, self.redraw)

    def redraw(self):
        self.pending = None
        if self.IsBeingDeleted() or not self.IsShown():
            return
        w, h = self.canvas.GetClientSize()
        if w < 100 or h < 100:
            return
        chrt = self.picker.selected()
        self.heading.SetLabel(caption(chrt))
        self.buffer = graphchart.GraphChart(
            chrt, (w, h), self.mainfr.options, self.mainfr.options.bw).drawChart()
        self.canvas.Refresh(False)

    def paint(self, event):
        if self.buffer is None:
            wx.PaintDC(self.canvas)
        else:
            wx.BufferedPaintDC(self.canvas, self.buffer)


class CompareGridFrame(wx.Frame):
    def __init__(self, mainfr):
        wx.Frame.__init__(self, mainfr, title='Compare charts', size=(1100, 650))
        self.SetMinSize((700, 500))
        outer = wx.BoxSizer(wx.VERTICAL)
        bar = wx.BoxSizer(wx.HORIZONTAL)
        bar.Add(wx.StaticText(self, label='Layout:'), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.layout_choice = wx.Choice(self, choices=['1 x 2', '2 x 2'])
        self.layout_choice.SetSelection(0)
        bar.Add(self.layout_choice)
        outer.Add(bar, 0, wx.ALL, 10)
        self.grid = wx.GridSizer(rows=1, cols=2, vgap=8, hgap=8)
        self.cells = [WheelCell(self, mainfr) for _ in range(4)]
        for cell in self.cells[:2]:
            self.grid.Add(cell, 1, wx.EXPAND)
        for cell in self.cells[2:]:
            cell.Hide()
        outer.Add(self.grid, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.SetSizer(outer)
        self.Bind(wx.EVT_CHOICE, self.change_layout, self.layout_choice)
        self.CentreOnParent()
        wx.CallAfter(self.refresh_wheels)

    def change_layout(self, event=None):
        quad = self.layout_choice.GetSelection() == 1
        self.grid.Clear(delete_windows=False)
        self.grid.SetRows(2 if quad else 1)
        self.grid.SetCols(2)
        for i, cell in enumerate(self.cells):
            cell.Show(i < (4 if quad else 2))
            if cell.IsShown():
                self.grid.Add(cell, 1, wx.EXPAND)
        self.Layout()
        self.refresh_wheels()

    def refresh_wheels(self):
        for cell in self.cells:
            if cell.IsShown():
                cell.queue_draw()


def show(mainfr):
    frame = CompareGridFrame(mainfr)
    frame.Show(True)
    return frame

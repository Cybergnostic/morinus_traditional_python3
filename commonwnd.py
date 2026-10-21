# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import os
import csv
import tradoptions
import wx
import menubars
import mtexts
from PIL import ImageDraw

# Morinus.ttf letters as Unicode, for copying tables as text
SYMBOLS = dict(zip('ABCDEFGHI', '\u2644\u2643\u2642\u2609\u2640\u263f\u263d\u260a\u260b'))
SYMBOLS.update(zip('abcdefghijkl', '\u2648\u2649\u264a\u264b\u264c\u264d\u264e\u264f\u2650\u2651\u2652\u2653'))
SYMBOLS.update(zip('LMNOP', '\u260c\u26b9\u25a1\u25b3\u260d'))
SYMBOLS.update({'R': '\u2225', 'S': '-\u2225', 'J': '\u2297', 'T': '\u211e', '0': 'Asc', '1': 'MC'})

class CommonWnd(wx.ScrolledWindow):
    SCROLL_RATE = 20
    BORDER = 20

    def __init__(self, parent, chrt, options, id=-1, size=wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)
        self.parent = parent
        self.chart = chrt
        self.options = options
        self.bw = self.options.bw
        self.SetBackgroundColour(self.options.clrbackground)
        self.SetScrollRate(CommonWnd.SCROLL_RATE, CommonWnd.SCROLL_RATE)
        self.pmenu = wx.Menu()
        menubars.later(self, 'Table')
        self.ID_SaveAsBitmap = wx.NewId()
        self.ID_BlackAndWhite = wx.NewId()
        self.pmenu.Append(self.ID_SaveAsBitmap, mtexts.txtspopupmenu['SaveAsBmp'], mtexts.txtspopupmenu['SaveTable'])
        mbw = self.pmenu.Append(self.ID_BlackAndWhite, mtexts.txtspopupmenu['BlackAndWhite'], mtexts.txtspopupmenu['TableBW'], wx.ITEM_CHECK)
        self.ID_CopyAsText = wx.NewIdRef()
        self.pmenu.Append(self.ID_CopyAsText, 'Copy as text', 'Copy the table to the clipboard as text (tab-separated)')
        self.Bind(wx.EVT_MENU, self.onCopyAsText, id=self.ID_CopyAsText)
        # copying as an image, CSV, and zoom (scaling the drawn table; the zoom is kept for all tables)
        for label, help, handler in (('Copy as image', 'Copy the table to the clipboard as a picture', self.onCopyAsImage),
                                     ('Export as CSV...', 'Save the table as a CSV file for spreadsheets', self.onExportCSV), (None, None, None),
                                     ('Zoom in\tCtrl++', 'Larger table', lambda e: self.setZoom(self.zoom * 1.25)),
                                     ('Zoom out\tCtrl+-', 'Smaller table', lambda e: self.setZoom(self.zoom / 1.25)),
                                     ('Actual size\tCtrl+0', 'The table at its drawn size', lambda e: self.setZoom(1.0))):
            if label is None:
                self.pmenu.AppendSeparator()
                continue
            item = self.pmenu.Append(wx.NewIdRef(), label, help)
            self.Bind(wx.EVT_MENU, handler, id=item.GetId())
        self.zoom = 1.0
        self.zoomed = None
        self.Bind(wx.EVT_MOUSEWHEEL, self.onWheel)
        wx.CallAfter(self.initZoom)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
        self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)
        if self.bw:
            mbw.Check()

    def onPopupMenu(self, event):
        self.PopupMenu(self.pmenu, event.GetPosition())

    def onSaveAsBitmap(self, event):
        name = self.chart.name + self.getExt()
        dlg = wx.FileDialog(self, mtexts.txtsfiles['SaveAsBmp'], '', name, mtexts.txtsfiles['BMPFiles'], wx.FD_SAVE)
        if os.path.isdir(self.mainfr.fpathimgs):
            dlg.SetDirectory(self.mainfr.fpathimgs)
        else:
            dlg.SetDirectory('.')
        if dlg.ShowModal() == wx.ID_OK:
            dpath = dlg.GetDirectory()
            fpath = dlg.GetPath()
            if not fpath.endswith('.png'):
                fpath += '.png'
            if os.path.isfile(fpath):
                dlgm = wx.MessageDialog(self, mtexts.txtsfiles['FileExists'], mtexts.txtsfiles['Message'], wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                if dlgm.ShowModal() == wx.ID_NO:
                    dlgm.Destroy()
                    dlg.Destroy()
                    return
                dlgm.Destroy()
            self.mainfr.fpathimgs = dpath
            self.buffer.SaveFile(fpath, wx.BITMAP_TYPE_PNG)
        dlg.Destroy()

    def onBlackAndWhite(self, event):
        if self.bw != event.IsChecked():
            self.bw = event.IsChecked()
            self.drawBkg()
            self.zoomed = None
            self.Refresh()

    def OnPaint(self, event):
        if self.zoom == 1.0:
            dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
            return
        if self.zoomed is None or self.zoomed[0] is not self.buffer:
            self.zoomed = (self.buffer, self.scaled())
        dc = wx.PaintDC(self)
        self.DoPrepareDC(dc)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.DrawBitmap(self.zoomed[1], 0, 0)

    def scaled(self):
        img = self.buffer.ConvertToImage()
        w, h = max(1, int(img.GetWidth() * self.zoom)), max(1, int(img.GetHeight() * self.zoom))
        return img.Scale(w, h, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()

    def initZoom(self):
        if self and getattr(self, 'buffer', None) is not None:
            self.setZoom(tradoptions.get('table_zoom'), False)

    def setZoom(self, zoom, keep=True):
        """Shows the table scaled by zoom (0.5-3); keep: for the next tables too."""
        self.zoom = round(min(3.0, max(0.5, zoom)), 3)
        if abs(self.zoom - 1.0) < 0.01:
            self.zoom = 1.0
        self.zoomed = None
        self.SetVirtualSize((int(self.buffer.GetWidth() * self.zoom), int(self.buffer.GetHeight() * self.zoom)))
        if keep:
            tradoptions.set({'table_zoom': self.zoom})
            if self.options.autosave:
                tradoptions.save()
        self.Refresh()

    def unzoom(self, x, y):
        """A position in the window as one in the drawn table (before scrolling)."""
        return x / self.zoom, y / self.zoom

    def onWheel(self, event):
        if event.ControlDown():
            self.setZoom(self.zoom * (1.1 if event.GetWheelRotation() > 0 else 1 / 1.1))
        else:
            event.Skip()

    def onCopyAsImage(self, event):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.BitmapDataObject(self.buffer))
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()

    def onExportCSV(self, event):
        name = self.chart.name + self.getExt() + '.csv'
        dlg = wx.FileDialog(self, 'Export as CSV', '', name, 'CSV files (*.csv)|*.csv', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if os.path.isdir(self.mainfr.fpathimgs):
            dlg.SetDirectory(self.mainfr.fpathimgs)
        if dlg.ShowModal() == wx.ID_OK:
            fpath = dlg.GetPath()
            if not fpath.lower().endswith('.csv'):
                fpath += '.csv'
            with open(fpath, 'w', newline='', encoding='utf-8-sig') as f:
                csv.writer(f).writerows(line.split('\t') for line in self.tableText().splitlines())
        dlg.Destroy()

    def tableText(self):
        """The table as tab-separated text, rebuilt from what drawBkg draws:
        texts on one line form a row, gaps wider than a space separate cells."""
        calls = []
        text = ImageDraw.ImageDraw.text

        def record(draw, xy, txt, *args, **kwargs):
            font = kwargs.get('font', args[1] if len(args) > 1 else None)
            calls.append((xy[0], xy[1], txt, font))
            return text(draw, xy, txt, *args, **kwargs)
        ImageDraw.ImageDraw.text = record
        try:
            self.drawBkg()
        finally:
            ImageDraw.ImageDraw.text = text
        items = []
        for x, y, txt, font in calls:
            if not txt.strip() or font is None:
                continue
            size = getattr(font, 'size', 10)
            width = font.getlength(txt)
            if getattr(font, 'path', '').endswith('Morinus.ttf'):
                txt = ''.join(SYMBOLS.get(c, c) for c in txt)
            items.append((y + size / 2.0, x, x + width, txt, size))
        rows = []
        for cy, x0, x1, txt, size in sorted(items):
            if rows and abs(cy - rows[-1][0]) < size * 0.6:
                rows[-1][1].append((x0, x1, txt, size))
            else:
                rows.append((cy, [(x0, x1, txt, size)]))
        lines = []
        for cy, cells in rows:
            line = ''
            end = None
            for x0, x1, txt, size in sorted(cells):
                if end is not None:
                    line += ' ' if x0 - end < size * 0.8 else '\t'
                line += txt.strip()
                end = x1
            lines.append(line)
        return '\n'.join(lines) + '\n'

    def onCopyAsText(self, event):
        txt = self.tableText()
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(txt))
            wx.TheClipboard.Flush()	# keep it after Morinus closes
            wx.TheClipboard.Close()

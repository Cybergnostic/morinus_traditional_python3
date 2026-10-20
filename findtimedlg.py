# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import sys
import wx
import rangechecker
import intvalidator
import findtime
import mtexts
import util
import _thread
import wx.lib.newevent
FTReadyEvent, EVT_FTREADY = wx.lib.newevent.NewEvent()
FTDataReadyEvent, EVT_FTDATAREADY = wx.lib.newevent.NewEvent()
FTYearEvent, EVT_FTYEAR = wx.lib.newevent.NewEvent()
ftlock = _thread.allocate_lock()

class AbortFindTime:

    def __init__(self):
        self.abort = False

    def aborting(self):
        self.abort = True


class ResListCtrl(wx.ListCtrl):
    NUM = 0
    DATE = 1
    TIME = 2
    COLNUM = TIME + 1

    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        self.reslistdata = {}
        self.Populate()
        self.Id = ID

    def Populate(self):
        self.InsertColumn(ResListCtrl.NUM, '')
        self.InsertColumn(ResListCtrl.DATE, mtexts.txtsfindtimedlg['Date'])
        self.InsertColumn(ResListCtrl.TIME, mtexts.txtsfindtimedlg['Time'])
        self.SetColumnWidth(ResListCtrl.NUM, 50)
        self.SetColumnWidth(ResListCtrl.DATE, 150)
        self.SetColumnWidth(ResListCtrl.TIME, 150)
        self.currentItem = -1
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

    def GetListCtrl(self):
        return self

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemSelected(self, event):
        self.currentItem = event.GetIndex()
        event.Skip()

    def OnColClick(self, event):
        event.Skip()

    def OnAdd(self, item):
        num = self.GetItemCount() + 1
        numtxt = str(num) + '.'
        self.InsertItem(num - 1, numtxt)
        self.SetItem(num - 1, 1, item[0])
        self.SetItem(num - 1, 2, item[1])
        self.currentItem = 0
        self.EnsureVisible(self.currentItem)
        self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def OnStart(self):
        if self.currentItem != -1:
            dlg = wx.MessageDialog(self, mtexts.txtscommon['AreYouSure'], mtexts.txtscommon['Confirm'], wx.YES_NO | wx.ICON_QUESTION)
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                self.DeleteAllItems()
                self.currentItem = -1
                dlg.Destroy()
                return True
            dlg.Destroy()
            return False
        return True


provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class FindTimeDlg(wx.Dialog):
    LON = 0
    RETR = 1
    MIN = 0
    SEC = 1
    RET = 2
    USEAPPROX = 0
    APPROXDEG = 1
    APPROXMIN = 2
    APPROXSEC = 3

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, mtexts.txtsfindtimedlg['FindTime'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        sbc = wx.StaticBox(self, label='')
        sbcsizer = wx.StaticBoxSizer(sbc, wx.VERTICAL)
        self.bcckb = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['BC'])
        sbcsizer.Add(self.bcckb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vsizer.Add(sbcsizer, 0, wx.GROW)
        splanets = wx.StaticBox(self, label='')
        splanetssizer = wx.StaticBoxSizer(splanets, wx.VERTICAL)
        gsizer = wx.GridSizer(0, 5, 0, 0)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Saturn'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.saturndeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,
                                                                                                      -1))
        self.saturndeg.SetHelpText(mtexts.txtsfindtimedlg['HelpDeg'])
        self.saturndeg.SetMaxLength(3)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.saturndeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['D'])
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.saturnmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                     -1))
        self.saturnmin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.saturnmin.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.saturnmin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.saturnmintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['M'])
        hsizer.Add(self.saturnmintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.saturnsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                     -1))
        self.saturnsec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.saturnsec.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.saturnsec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.saturnsectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['S'])
        hsizer.Add(self.saturnsectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.saturnretr = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['R'])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.saturnretr, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Jupiter'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.jupiterdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,
                                                                                                       -1))
        self.jupiterdeg.SetHelpText(mtexts.txtsfindtimedlg['HelpDeg'])
        self.jupiterdeg.SetMaxLength(3)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.jupiterdeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['D'])
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.jupitermin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                      -1))
        self.jupitermin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.jupitermin.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.jupitermin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.jupitermintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['M'])
        hsizer.Add(self.jupitermintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.jupitersec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                      -1))
        self.jupitersec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.jupitersec.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.jupitersec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.jupitersectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['S'])
        hsizer.Add(self.jupitersectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.jupiterretr = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['R'])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.jupiterretr, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Mars'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.marsdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,
                                                                                                    -1))
        self.marsdeg.SetHelpText(mtexts.txtsfindtimedlg['HelpDeg'])
        self.marsdeg.SetMaxLength(3)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.marsdeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['D'])
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.marsmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                   -1))
        self.marsmin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.marsmin.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.marsmin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.marsmintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['M'])
        hsizer.Add(self.marsmintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.marssec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                   -1))
        self.marssec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.marssec.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.marssec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.marssectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['S'])
        hsizer.Add(self.marssectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.marsretr = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['R'])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.marsretr, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Sun'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.sundeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,
                                                                                                   -1))
        self.sundeg.SetHelpText(mtexts.txtsfindtimedlg['HelpDeg'])
        self.sundeg.SetMaxLength(3)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.sundeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['D'])
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.sunmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.sunmin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.sunmin.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.sunmin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.sunmintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['M'])
        hsizer.Add(self.sunmintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.sunsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.sunsec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.sunsec.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.sunsec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.sunsectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['S'])
        hsizer.Add(self.sunsectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.sunretr = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['R'])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.sunretr, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.sunretr.Enable(False)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Venus'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.venusdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,
                                                                                                     -1))
        self.venusdeg.SetHelpText(mtexts.txtsfindtimedlg['HelpDeg'])
        self.venusdeg.SetMaxLength(3)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.venusdeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['D'])
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.venusmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                    -1))
        self.venusmin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.venusmin.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.venusmin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.venusmintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['M'])
        hsizer.Add(self.venusmintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.venussec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                    -1))
        self.venussec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.venussec.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.venussec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.venussectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['S'])
        hsizer.Add(self.venussectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.venusretr = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['R'])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.venusretr, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Mercury'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mercurydeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,
                                                                                                       -1))
        self.mercurydeg.SetHelpText(mtexts.txtsfindtimedlg['HelpDeg'])
        self.mercurydeg.SetMaxLength(3)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.mercurydeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['D'])
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mercurymin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                      -1))
        self.mercurymin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.mercurymin.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.mercurymin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mercurymintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['M'])
        hsizer.Add(self.mercurymintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mercurysec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                      -1))
        self.mercurysec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.mercurysec.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.mercurysec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mercurysectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['S'])
        hsizer.Add(self.mercurysectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mercuryretr = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['R'])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.mercuryretr, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtscommon['Moon'] + ':')
        gsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.moondeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,
                                                                                                    -1))
        self.moondeg.SetHelpText(mtexts.txtsfindtimedlg['HelpDeg'])
        self.moondeg.SetMaxLength(3)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.moondeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        label = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['D'])
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.moonmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                   -1))
        self.moonmin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.moonmin.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.moonmin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.moonmintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['M'])
        hsizer.Add(self.moonmintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.moonsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                   -1))
        self.moonsec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.moonsec.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.moonsec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.moonsectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['S'])
        hsizer.Add(self.moonsectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.moonretr = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['R'])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.moonretr, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.moonretr.Enable(False)
        splanetssizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vsizer.Add(splanetssizer, 0)
        suse = wx.StaticBox(self, label=mtexts.txtsfindtimedlg['Use'])
        susesizer = wx.StaticBoxSizer(suse, wx.VERTICAL)
        self.useminckb = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['Minute'])
        susesizer.Add(self.useminckb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        self.usesecckb = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['Second'])
        susesizer.Add(self.usesecckb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        self.useretrckb = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['Retrograde'])
        susesizer.Add(self.useretrckb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vsizer.Add(susesizer, 1, wx.GROW)
        mhsizer.Add(vsizer, 0, wx.GROW, 0)
        vvvsizer = wx.BoxSizer(wx.VERTICAL)
        sangles = wx.StaticBox(self, label='')
        sanglessizer = wx.StaticBoxSizer(sangles, wx.VERTICAL)
        gsizer = wx.GridSizer(0, 4, 0, 0)
        self.asctxt = wx.StaticText(self, -1, mtexts.txtscommon['Asc'] + ':')
        gsizer.Add(self.asctxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.ascdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,
                                                                                                   -1))
        self.ascdeg.SetHelpText(mtexts.txtsfindtimedlg['HelpDeg'])
        self.ascdeg.SetMaxLength(3)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.ascdeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.ascdegtxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['D'])
        hsizer.Add(self.ascdegtxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.ascmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.ascmin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.ascmin.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.ascmin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.ascmintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['M'])
        hsizer.Add(self.ascmintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.ascsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.ascsec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.ascsec.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.ascsec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.ascsectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['S'])
        hsizer.Add(self.ascsectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mctxt = wx.StaticText(self, -1, mtexts.txtscommon['MC'] + ':')
        gsizer.Add(self.mctxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mcdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 359), size=(40,
                                                                                                  -1))
        self.mcdeg.SetHelpText(mtexts.txtsfindtimedlg['HelpDeg'])
        self.mcdeg.SetMaxLength(3)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.mcdeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mcdegtxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['D'])
        hsizer.Add(self.mcdegtxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mcmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                 -1))
        self.mcmin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.mcmin.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.mcmin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mcmintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['M'])
        hsizer.Add(self.mcmintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mcsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                 -1))
        self.mcsec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.mcsec.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.mcsec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.mcsectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['S'])
        hsizer.Add(self.mcsectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        sanglessizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        self.useascmcckb = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['Use'])
        sanglessizer.Add(self.useascmcckb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vvvsizer.Add(sanglessizer, 0, wx.GROW | wx.LEFT, 5)
        rnge = 3000
        checker = rangechecker.RangeChecker()
        if checker.isExtended():
            rnge = 5000
        sforce = wx.StaticBox(self, label='')
        sforcesizer = wx.StaticBoxSizer(sforce, wx.VERTICAL)
        gsizer = wx.GridSizer(0, 3, 0, 0)
        self.fyear = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, rnge), size=(50,
                                                                                                   -1))
        if checker.isExtended():
            self.fyear.SetHelpText(mtexts.txtsfindtimedlg['HelpYear'])
        else:
            self.fyear.SetHelpText(mtexts.txtsfindtimedlg['HelpYear2'])
        self.fyear.SetMaxLength(4)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.fyear, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fyeartxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['YE'])
        hsizer.Add(self.fyeartxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fmonth = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,
                                                                                                  -1))
        self.fmonth.SetHelpText(mtexts.txtsfindtimedlg['HelpMonth'])
        self.fmonth.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.fmonth, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fmonthtxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['MO'])
        hsizer.Add(self.fmonthtxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fday = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 31), size=(50,
                                                                                                -1))
        self.fday.SetHelpText(mtexts.txtsfindtimedlg['HelpDay'])
        self.fday.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.fday, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fdaytxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['DA'])
        hsizer.Add(self.fdaytxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fhour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 23), size=(50,
                                                                                                 -1))
        self.fhour.SetHelpText(mtexts.txtsfindtimedlg['HelpHour'])
        self.fhour.SetMaxLength(3)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.fhour, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fhourtxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['HO'])
        hsizer.Add(self.fhourtxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,
                                                                                                -1))
        self.fmin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.fmin.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.fmin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fmintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['MI'])
        hsizer.Add(self.fmintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,
                                                                                                -1))
        self.fsec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.fsec.SetMaxLength(2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.fsec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.fsectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['SE'])
        hsizer.Add(self.fsectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        gsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        sforcesizer.Add(gsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        self.forceckb = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['ForceTheDate'])
        sforcesizer.Add(self.forceckb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vvvsizer.Add(sforcesizer, 0, wx.GROW | wx.LEFT, 5)
        sapprox = wx.StaticBox(self, label=mtexts.txtsfindtimedlg['ApproxPlanets'])
        sapproxsizer = wx.StaticBoxSizer(sapprox, wx.VERTICAL)
        self.useapproxckb = wx.CheckBox(self, -1, mtexts.txtsfindtimedlg['Use'])
        self.approxdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 4), size=(30,
                                                                                                    -1))
        self.approxdeg.SetHelpText(mtexts.txtsfindtimedlg['HelpApproxDeg'])
        self.approxdeg.SetMaxLength(1)
        self.approxmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                     -1))
        self.approxmin.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.approxmin.SetMaxLength(2)
        self.approxsec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                     -1))
        self.approxsec.SetHelpText(mtexts.txtsfindtimedlg['HelpMin'])
        self.approxsec.SetMaxLength(2)
        hsizerDeg = wx.BoxSizer(wx.HORIZONTAL)
        hsizerDeg.Add(self.approxdeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.approxdegtxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['D'])
        hsizerDeg.Add(self.approxdegtxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        hsizerMin = wx.BoxSizer(wx.HORIZONTAL)
        hsizerMin.Add(self.approxmin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.approxmintxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['M'])
        hsizerMin.Add(self.approxmintxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        hsizerSec = wx.BoxSizer(wx.HORIZONTAL)
        hsizerSec.Add(self.approxsec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.approxsectxt = wx.StaticText(self, -1, mtexts.txtsfindtimedlg['S'])
        hsizerSec.Add(self.approxsectxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        hsizerLon = wx.BoxSizer(wx.HORIZONTAL)
        hsizerLon.Add(hsizerDeg, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        hsizerLon.Add(hsizerMin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        hsizerLon.Add(hsizerSec, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        hsizerAppr = wx.BoxSizer(wx.HORIZONTAL)
        hsizerAppr.Add(self.useapproxckb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        hsizerAppr.Add(hsizerLon, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        sapproxsizer.Add(hsizerAppr, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
        vvvsizer.Add(sapproxsizer, 0, wx.GROW | wx.LEFT, 5)
        sreslist = wx.StaticBox(self, label='')
        reslistsizer = wx.StaticBoxSizer(sreslist, wx.VERTICAL)
        ID_ResList = wx.NewId()
        self.li = ResListCtrl(self, ID_ResList, size=(360, 100), style=wx.LC_VRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL)
        reslistsizer.Add(self.li, 1, wx.GROW | wx.ALL, 5)
        vvvsizer.Add(reslistsizer, 0, wx.GROW | wx.LEFT, 5)
        List_Start_ID = wx.NewId()
        self.btnStart = wx.Button(self, List_Start_ID, mtexts.txtsfindtimedlg['Start'])
        List_Show_ID = wx.NewId()
        self.btnShow = wx.Button(self, List_Show_ID, mtexts.txtsfindtimedlg['Show'])
        self.btnShow.Enable(False)
        hbtnsizer = wx.BoxSizer(wx.HORIZONTAL)
        hbtnsizer.Add(self.btnStart, 1, wx.GROW, 5)
        hbtnsizer.Add(self.btnShow, 1, wx.GROW, 5)
        vvvsizer.Add(hbtnsizer, 0, wx.GROW, 5)
        mhsizer.Add(vvvsizer, 0, wx.GROW, 0)
        mvsizer.Add(mhsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != '__WXMSW__':
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txtscommon['Close'])
        btnOk.SetDefault()
        btnsizer.AddButton(btnOk)
        btnsizer.Realize()
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        self.Bind(wx.EVT_CHECKBOX, self.onUseMin, id=self.useminckb.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.onUseSec, id=self.usesecckb.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.onUseRetr, id=self.useretrckb.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.onUseAscMC, id=self.useascmcckb.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.onUseForce, id=self.forceckb.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.onUseApprox, id=self.useapproxckb.GetId())
        self.useminckb.SetValue(True)
        self.usesecckb.SetValue(True)
        self.useretrckb.SetValue(True)
        self.useascmcckb.SetValue(False)
        self.enableAscMC(self.useascmcckb.GetValue())
        self.enableForce(self.useascmcckb.GetValue())
        self.useapproxckb.SetValue(False)
        self.approxdeg.Enable(False)
        self.approxdegtxt.Enable(False)
        self.approxmin.Enable(False)
        self.approxmintxt.Enable(False)
        self.approxsec.Enable(False)
        self.approxsectxt.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.OnStart, id=self.btnStart.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnShow, id=self.btnShow.GetId())
        self.Bind(wx.EVT_BUTTON, self.onOK, id=btnOk.GetId())
        self.Bind(wx.EVT_CLOSE, self.onOK)
        self.Bind(EVT_FTREADY, self.OnFTReady)
        self.Bind(EVT_FTDATAREADY, self.OnFTDataReady)
        self.Bind(EVT_FTYEAR, self.OnFTYear)
        btnOk.SetFocus()
        self.progtxt = mtexts.txtsfindtimedlg['BusyInfo']
        self.suffix = ''
        self.found = False
        self.ar = None
        return

    def onUseMin(self, event):
        val = self.useminckb.GetValue()
        self.enableMins(val)
        if not val:
            self.usesecckb.SetValue(False)
            self.usesecckb.Enable(False)
            self.enableSecs(False)
            self.useapproxckb.SetValue(False)
            self.approxdeg.Enable(False)
            self.approxdegtxt.Enable(False)
            self.approxmin.Enable(False)
            self.approxmintxt.Enable(False)
            self.approxsec.Enable(False)
            self.approxsectxt.Enable(False)
        else:
            self.usesecckb.Enable(True)

    def enableMins(self, val):
        ar = (
         self.saturnmin, self.saturnmintxt, self.jupitermin, self.jupitermintxt, self.marsmin, self.marsmintxt, self.sunmin, self.sunmintxt, self.venusmin, self.venusmintxt, self.mercurymin, self.mercurymintxt, self.moonmin, self.moonmintxt)
        arlen = len(ar)
        for i in range(arlen):
            ar[i].Enable(val)

    def onUseSec(self, event):
        self.enableSecs(self.usesecckb.GetValue())
        val = self.usesecckb.GetValue()
        if not val:
            self.useapproxckb.SetValue(False)
            self.approxdeg.Enable(False)
            self.approxdegtxt.Enable(False)
            self.approxmin.Enable(False)
            self.approxmintxt.Enable(False)
            self.approxsec.Enable(False)
            self.approxsectxt.Enable(False)

    def enableSecs(self, val):
        ar = (
         self.saturnsec, self.saturnsectxt, self.jupitersec, self.jupitersectxt, self.marssec, self.marssectxt, self.sunsec, self.sunsectxt, self.venussec, self.venussectxt, self.mercurysec, self.mercurysectxt, self.moonsec, self.moonsectxt)
        arlen = len(ar)
        for i in range(arlen):
            ar[i].Enable(val)

    def onUseRetr(self, event):
        self.enableRetrs(self.useretrckb.GetValue())

    def onUseAscMC(self, event):
        self.enableAscMC(self.useascmcckb.GetValue())
        self.enableForce(self.useascmcckb.GetValue())
        if self.forceckb.GetValue():
            self.btnStart.Enable(not self.useascmcckb.GetValue())
            self.btnShow.Enable(self.useascmcckb.GetValue())

    def onUseForce(self, event):
        self.btnStart.Enable(not self.forceckb.GetValue())
        self.btnShow.Enable(self.forceckb.GetValue())

    def onUseApprox(self, event):
        self.enableApprox(self.useapproxckb.GetValue())

    def enableRetrs(self, val):
        ar = (
         self.saturnretr, self.jupiterretr, self.marsretr, self.venusretr, self.mercuryretr)
        arlen = len(ar)
        for i in range(arlen):
            ar[i].Enable(val)

    def enableAscMC(self, val):
        ar = (
         self.asctxt, self.ascdeg, self.ascdegtxt, self.ascmin, self.ascmintxt, self.ascsec, self.ascsectxt, self.mctxt, self.mcdeg, self.mcdegtxt, self.mcmin, self.mcmintxt, self.mcsec, self.mcsectxt)
        arlen = len(ar)
        for i in range(arlen):
            ar[i].Enable(val)

    def enableForce(self, val):
        ar = (
         self.fyear, self.fyeartxt, self.fmonth, self.fmonthtxt, self.fday, self.fdaytxt, self.fhour, self.fhourtxt, self.fmin, self.fmintxt, self.fsec, self.fsectxt)
        arlen = len(ar)
        for i in range(arlen):
            ar[i].Enable(val)

        self.forceckb.Enable(val)

    def enableApprox(self, val):
        self.approxdeg.Enable(val)
        self.approxdegtxt.Enable(val)
        self.approxmin.Enable(val)
        self.approxmintxt.Enable(val)
        self.approxsec.Enable(val)
        self.approxsectxt.Enable(val)
        self.enableMins(True)
        self.enableSecs(True)
        self.useminckb.SetValue(True)
        self.usesecckb.Enable(True)
        self.usesecckb.SetValue(True)

    def OnStart(self, event):
        if not self.Validate():
            return
        else:
            res = self.li.OnStart()
            if not res:
                return
            if not self.checkAsc():
                return
            self.bc = self.bcckb.GetValue()
            saturnlon = float(self.saturndeg.GetValue())
            if self.useminckb.GetValue():
                saturnlon += float(self.saturnmin.GetValue()) / 60.0
            if self.usesecckb.GetValue():
                saturnlon += float(self.saturnsec.GetValue()) / 3600.0
            saturnretr = self.saturnretr.GetValue()
            jupiterlon = float(self.jupiterdeg.GetValue())
            if self.useminckb.GetValue():
                jupiterlon += float(self.jupitermin.GetValue()) / 60.0
                if self.usesecckb.GetValue():
                    jupiterlon += float(self.jupitersec.GetValue()) / 3600.0
            jupiterretr = self.jupiterretr.GetValue()
            marslon = float(self.marsdeg.GetValue())
            if self.useminckb.GetValue():
                marslon += float(self.marsmin.GetValue()) / 60.0
                if self.usesecckb.GetValue():
                    marslon += float(self.marssec.GetValue()) / 3600.0
            marsretr = self.marsretr.GetValue()
            sunlon = float(self.sundeg.GetValue())
            if self.useminckb.GetValue():
                sunlon += float(self.sunmin.GetValue()) / 60.0
                if self.usesecckb.GetValue():
                    sunlon += float(self.sunsec.GetValue()) / 3600.0
            sunretr = False
            venuslon = float(self.venusdeg.GetValue())
            if self.useminckb.GetValue():
                venuslon += float(self.venusmin.GetValue()) / 60.0
                if self.usesecckb.GetValue():
                    venuslon += float(self.venussec.GetValue()) / 3600.0
            venusretr = self.venusretr.GetValue()
            mercurylon = float(self.mercurydeg.GetValue())
            if self.useminckb.GetValue():
                mercurylon += float(self.mercurymin.GetValue()) / 60.0
                if self.usesecckb.GetValue():
                    mercurylon += float(self.mercurysec.GetValue()) / 3600.0
            mercuryretr = self.mercuryretr.GetValue()
            moonlon = float(self.moondeg.GetValue())
            if self.useminckb.GetValue():
                moonlon += float(self.moonmin.GetValue()) / 60.0
                if self.usesecckb.GetValue():
                    moonlon += float(self.moonsec.GetValue()) / 3600.0
            moonretr = False
            useascmc = self.useascmcckb.GetValue()
            asclon = float(self.ascdeg.GetValue()) + float(self.ascmin.GetValue()) / 60.0 + float(self.ascsec.GetValue()) / 3600.0
            mclon = float(self.mcdeg.GetValue()) + float(self.mcmin.GetValue()) / 60.0 + float(self.mcsec.GetValue()) / 3600.0
            useapprox = self.useapproxckb.GetValue()
            approxdeg = float(self.approxdeg.GetValue())
            approxmin = float(self.approxmin.GetValue())
            approxsec = float(self.approxsec.GetValue())
            ftdata = (
             (
              saturnlon, saturnretr), (jupiterlon, jupiterretr), (marslon, marsretr), (sunlon, sunretr), (venuslon, venusretr), (mercurylon, mercuryretr), (moonlon, moonretr))
            usemin = self.useminckb.GetValue()
            usesec = self.usesecckb.GetValue()
            useretr = self.useretrckb.GetValue()
            ftdatause = (usemin, usesec, useretr)
            ftdataascmc = (
             useascmc, asclon, mclon)
            ftdataapprox = (
             useapprox, approxdeg, approxmin, approxsec)
            self.suffix = ''
            self.progtxt = mtexts.txtsfindtimedlg['BusyInfo']
            self.progbar = wx.ProgressDialog(mtexts.txtsfindtimedlg['Calculating'], self.progtxt + '\n', parent=self, style=wx.PD_CAN_ABORT | wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME)
            self.progbar.Fit()
            self.btnShow.Enable(False)
            self.found = False
            if self.ar != None:
                del self.ar
                self.ar = None
            self.ftready = False
            self.abort = AbortFindTime()
            thId = _thread.start_new_thread(self.calcCharts, (self.bc, ftdata, ftdatause, ftdataascmc, ftdataapprox, self))
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.OnTimer)
            self.timer.Start(500)
            return

    def calcCharts(self, bc, ftdata, ftdatause, ftdataascmc, ftdataapprox, win):
        ft = findtime.FindTime(bc, ftdata, ftdatause, ftdataascmc, ftdataapprox, self.abort, win)
        ft.find()
        ftlock.acquire()
        self.ftready = True
        ftlock.release()
        evt = FTReadyEvent()
        wx.PostEvent(win, evt)

    def OnTimer(self, event):
        ftlock.acquire()
        if not self.ftready:
            self.progtxt = mtexts.txtsfindtimedlg['BusyInfo'] + '\n' + mtexts.txtsfindtimedlg['Year'] + ': ' + self.suffix
            keepGoing, skip = self.progbar.Pulse(self.progtxt)
            if not keepGoing:
                self.abort.aborting()
        ftlock.release()

    def OnFTReady(self, event):
        self.timer.Stop()
        del self.timer
        self.progbar.Destroy()
        del self.progbar
        if self.abort.abort:
            self.Refresh()
        elif not self.found:
            dlgm = wx.MessageDialog(self, mtexts.txtsfindtimedlg['NoChartWithSettings'], mtexts.txtsfindtimedlg['Information'], wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
        del self.abort
        if self.found:
            self.btnShow.Enable(True)

    def OnFTDataReady(self, event):
        self.OnAdd(event.attr1)
        if self.ar == None:
            self.ar = []
        self.ar.append(event.attr1)
        self.found = True
        return

    def OnFTYear(self, event):
        signtxt = ''
        if self.bcckb.GetValue():
            signtxt = '-'
        self.suffix = signtxt + str(event.attr1)

    def OnAdd(self, fnd):
        datstr = str(fnd[0]) + '.' + str(fnd[1]) + '.' + str(fnd[2])
        h, m, s = util.decToDeg(fnd[3])
        timstr = str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
        item = [datstr, timstr]
        self.li.OnAdd(item)

    def OnShow(self, event):
        if self.useascmcckb.GetValue() and self.forceckb.GetValue():
            if not self.Validate():
                return
        if not self.checkAsc():
            return
        arplac = [0.0, 0.0, False]
        if self.useascmcckb.GetValue():
            arplac[0] = float(self.mcdeg.GetValue()) + float(self.mcmin.GetValue()) / 60.0 + float(self.mcsec.GetValue()) / 3600.0
            arplac[1] = float(self.ascdeg.GetValue()) + float(self.ascmin.GetValue()) / 60.0 + float(self.ascsec.GetValue()) / 3600.0
            arplac[2] = True
        if self.forceckb.GetValue():
            t = float(self.fhour.GetValue()) + float(self.fmin.GetValue()) / 60.0 + float(self.fsec.GetValue()) / 3600.0
            it = (int(self.fyear.GetValue()), int(self.fmonth.GetValue()), int(self.fday.GetValue()), t)
        else:
            it = self.ar[self.li.currentItem]
        self.parent.showFindTime(self.bcckb.GetValue(), it, arplac)

    def checkAsc(self):
        res = True
        if self.useascmcckb.GetValue():
            if int(self.ascdeg.GetValue()) == 0 and int(self.ascmin.GetValue()) == 0 and int(self.ascsec.GetValue()) == 0 or int(self.ascdeg.GetValue()) == 180 and int(self.ascmin.GetValue()) == 0 and int(self.ascsec.GetValue()) == 0:
                dlg = wx.MessageDialog(self, mtexts.txtsfindtimedlg['InvalidAsc'], mtexts.txtsfindtimedlg['Information'], wx.OK | wx.ICON_INFORMATION)
                val = dlg.ShowModal()
                dlg.Destroy()
                res = False
        return res

    def onOK(self, event):
        # the dialog is modeless: Close() here would only click this button
        # again (wxPython 4), so the dialog is destroyed instead
        self.Destroy()

    def fill(self):
        self.saturndeg.SetValue(str(0))
        self.saturnmin.SetValue(str(0))
        self.saturnsec.SetValue(str(0))
        self.jupiterdeg.SetValue(str(0))
        self.jupitermin.SetValue(str(0))
        self.jupitersec.SetValue(str(0))
        self.marsdeg.SetValue(str(0))
        self.marsmin.SetValue(str(0))
        self.marssec.SetValue(str(0))
        self.sundeg.SetValue(str(0))
        self.sunmin.SetValue(str(0))
        self.sunsec.SetValue(str(0))
        self.venusdeg.SetValue(str(0))
        self.venusmin.SetValue(str(0))
        self.venussec.SetValue(str(0))
        self.mercurydeg.SetValue(str(0))
        self.mercurymin.SetValue(str(0))
        self.mercurysec.SetValue(str(0))
        self.moondeg.SetValue(str(0))
        self.moonmin.SetValue(str(0))
        self.moonsec.SetValue(str(0))
        self.ascdeg.SetValue(str(0))
        self.ascmin.SetValue(str(0))
        self.ascsec.SetValue(str(0))
        self.mcdeg.SetValue(str(0))
        self.mcmin.SetValue(str(0))
        self.mcsec.SetValue(str(0))
        self.fyear.SetValue(str(1))
        self.fmonth.SetValue(str(1))
        self.fday.SetValue(str(1))
        self.fhour.SetValue(str(0))
        self.fmin.SetValue(str(0))
        self.fsec.SetValue(str(0))
        self.approxdeg.SetValue(str(0))
        self.approxmin.SetValue(str(0))
        self.approxsec.SetValue(str(0))
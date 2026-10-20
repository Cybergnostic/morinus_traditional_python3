# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import sys
import wx
import limchecklistctrlmixin
import intvalidator
import chart
import planets
import lots
import options
import mtexts
import copy
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class LotsListCtrl(limchecklistctrlmixin.LimCheckListCtrlMixin, wx.ListCtrl):
    NUM = 0
    NAME = 1
    FORMULA = 2
    DIURNAL = 3
    SHOWN = 4
    LORDTXT = '!'
    DIURNALTXT = '*'
    # no practical limit on the number of lots (was 40)
    MAX_LOTS_NUM = 100000

    def __init__(self, parent, ID, lots, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        limchecklistctrlmixin.LimCheckListCtrlMixin.__init__(self, LotsListCtrl.MAX_LOTS_NUM)
        self.parent = parent
        self.lotsdata = {}
        self.night = False
        self.load(lots)
        self.Populate()
        self.Id = ID
        self.changed = False
        self.removed = False

    def Populate(self):
        self.InsertColumn(LotsListCtrl.NUM, '')
        self.InsertColumn(LotsListCtrl.NAME, mtexts.txtslotsdlg['Name'])
        self.InsertColumn(LotsListCtrl.FORMULA, mtexts.txtslotsdlg['Formula'], format=wx.LIST_FORMAT_CENTER)
        self.InsertColumn(LotsListCtrl.DIURNAL, mtexts.txtslotsdlg['Diurnal'], format=wx.LIST_FORMAT_CENTER)
        self.InsertColumn(LotsListCtrl.SHOWN, mtexts.txtslotsdlg['Formula'], format=wx.LIST_FORMAT_CENTER)
        items = list(self.lotsdata.items())
        cnt = 0
        for key, data in items:
            cnt += 1
            index = self.InsertStringItem(self.GetItemCount(), data[0])
            self.SetItem(index, LotsListCtrl.NUM, str(cnt) + '.')
            self.SetItem(index, LotsListCtrl.NAME, data[0])
            self.SetItem(index, LotsListCtrl.FORMULA, data[1])
            self.SetItem(index, LotsListCtrl.DIURNAL, data[2])
            self.SetItemData(index, key)

        self.SetColumnWidth(LotsListCtrl.NUM, 60)
        self.SetColumnWidth(LotsListCtrl.NAME, 160)
        self.SetColumnWidth(LotsListCtrl.FORMULA, 0)
        self.SetColumnWidth(LotsListCtrl.DIURNAL, 65)
        self.SetColumnWidth(LotsListCtrl.SHOWN, 160)
        self.currentItem = 0
        self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

    def SetItem(self, *args, **kw):
        # keeps the shown formula in step with the stored formula and the night-reversal flag
        res = wx.ListCtrl.SetItem(self, *args, **kw)
        if len(args) >= 3 and args[1] in (LotsListCtrl.FORMULA, LotsListCtrl.DIURNAL):
            self.updateShown(args[0])
        return res

    def shownFormula(self, form, diurnal):
        """The formula as it applies to a night chart when night is selected (reversing lots swap the 2nd and 3rd terms)"""
        if not (self.night and diurnal) or '+' not in form or '-' not in form:
            return form
        return '%s + %s - %s' % (self.getFormula(form, 1), self.getFormula(form, 3), self.getFormula(form, 2))

    def updateShown(self, index):
        form = self.getColumnText(index, LotsListCtrl.FORMULA)
        diurnal = self.getColumnText(index, LotsListCtrl.DIURNAL) != ''
        wx.ListCtrl.SetItem(self, index, LotsListCtrl.SHOWN, self.shownFormula(form, diurnal))

    def setNight(self, night):
        self.night = night
        for i in range(self.GetItemCount()):
            self.updateShown(i)

    def setVisibility(self, opts):
        for i in range(self.GetItemCount()):
            if opts.lotsvisible[i]:
                self.CheckItem(i)

    def GetListCtrl(self):
        return self

    def getCurrItem(self):
        return self.currentItem

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def initFill(self):
        item = []
        name = self.getColumnText(self.currentItem, LotsListCtrl.NAME)
        form = self.getColumnText(self.currentItem, LotsListCtrl.FORMULA)
        f1 = self.getFormula(form, 1)
        f2 = self.getFormula(form, 2)
        f3 = self.getFormula(form, 3)
        fs = [f1, f2, f3]
        refordegs = [0, 0, 0]
        for j in range(len(fs)):
            if fs[j][0].isdigit():
                lord = fs[j][(-1)] == LotsListCtrl.LORDTXT
                txt = ''
                if lord:
                    txt = fs[j][:-1]
                else:
                    txt = fs[j][:]
                signtxt = txt[-3:]
                sign = self.getSignFromText(signtxt)
                if sign == -1:
                    continue
                deg = int(txt[:-3])
                refordegs[j] = sign * chart.Chart.SIGN_DEG + deg
                fs[j] = mtexts.lotstxts[lots.Lots.DEG]
                if lord:
                    fs[j] = mtexts.lotstxts[lots.Lots.DEGLORD]
            elif fs[j][0] == mtexts.txtslotsdlg['R']:
                lord = fs[j][(-1)] == LotsListCtrl.LORDTXT
                if lord:
                    refordegs[j] = int(fs[j][1:-1])
                else:
                    refordegs[j] = int(fs[j][1:])
                fs[j] = mtexts.lotstxts[lots.Lots.REF]
                if lord:
                    fs[j] = mtexts.lotstxts[lots.Lots.REFLORD]

        diurnal = self.getColumnText(self.currentItem, LotsListCtrl.DIURNAL)
        diur = True
        if diurnal == '':
            diur = False
        item = (name, (mtexts.conv[fs[0]], mtexts.conv[fs[1]], mtexts.conv[fs[2]]), (refordegs[0], refordegs[1], refordegs[2]), diur)
        self.parent.fillEditor(item)

    def OnItemSelected(self, event):
        self.currentItem = event.GetIndex()
        item = []
        name = self.getColumnText(self.currentItem, LotsListCtrl.NAME)
        form = self.getColumnText(self.currentItem, LotsListCtrl.FORMULA)
        f1 = self.getFormula(form, 1)
        f2 = self.getFormula(form, 2)
        f3 = self.getFormula(form, 3)
        fs = [f1, f2, f3]
        refordegs = [0, 0, 0]
        for j in range(len(fs)):
            if fs[j][0].isdigit():
                lord = fs[j][(-1)] == LotsListCtrl.LORDTXT
                txt = ''
                if lord:
                    txt = fs[j][:-1]
                else:
                    txt = fs[j][:]
                signtxt = txt[-3:]
                sign = self.getSignFromText(signtxt)
                if sign == -1:
                    continue
                deg = int(txt[:-3])
                refordegs[j] = sign * chart.Chart.SIGN_DEG + deg
                fs[j] = mtexts.lotstxts[lots.Lots.DEG]
                if lord:
                    fs[j] = mtexts.lotstxts[lots.Lots.DEGLORD]
            elif fs[j][0] == mtexts.txtslotsdlg['R']:
                lord = fs[j][(-1)] == LotsListCtrl.LORDTXT
                if lord:
                    refordegs[j] = int(fs[j][1:-1])
                else:
                    refordegs[j] = int(fs[j][1:])
                fs[j] = mtexts.lotstxts[lots.Lots.REF]
                if lord:
                    fs[j] = mtexts.lotstxts[lots.Lots.REFLORD]

        diurnal = self.getColumnText(self.currentItem, LotsListCtrl.DIURNAL)
        diur = True
        if diurnal == '':
            diur = False
        item = (name, (mtexts.conv[fs[0]], mtexts.conv[fs[1]], mtexts.conv[fs[2]]), (refordegs[0], refordegs[1], refordegs[2]), diur)
        self.parent.fillEditor(item)
        event.Skip()

    def OnColClick(self, event):
        event.Skip()

    def OnCheckItem(self, index, flag):
        pass

    def isReferred(self, num, lines=None):
        for i in range(num, self.GetItemCount()):
            form = self.getColumnText(i, LotsListCtrl.FORMULA)
            f1 = self.getFormula(form, 1)
            f2 = self.getFormula(form, 2)
            f3 = self.getFormula(form, 3)
            fs = [f1, f2, f3]
            ref = 0
            for j in range(len(fs)):
                if fs[j][0] == mtexts.txtslotsdlg['R']:
                    lord = fs[j][(-1)] == LotsListCtrl.LORDTXT
                    if lord:
                        ref = int(fs[j][1:-1])
                    else:
                        ref = int(fs[j][1:])
                    if ref == num:
                        if lines == None:
                            return True
                        lines.append(i)
                        break

        if lines == None:
            return False
        else:
            return lines

    def isReferring(self, idx):
        form = self.getColumnText(idx - 1, LotsListCtrl.FORMULA)
        f1 = self.getFormula(form, 1)
        f2 = self.getFormula(form, 2)
        f3 = self.getFormula(form, 3)
        fs = [
         f1, f2, f3]
        for i in range(len(fs)):
            if fs[i][0] == mtexts.txtslotsdlg['R']:
                return True

        return False

    def checkName(self, name, idx=None):
        for i in range(self.GetItemCount()):
            if name == self.getColumnText(i, LotsListCtrl.NAME):
                if idx == None or idx != i:
                    return True

        return False

    def OnAdd(self, item):
        num = self.GetItemCount()
        it = (num, item[0], item[1], item[2])
        if self.checkName(it[LotsListCtrl.NAME]):
            dlgm = wx.MessageDialog(self, mtexts.txtslotsdlg['LotAlreadyExists'], '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return False
        self.InsertStringItem(num, str(num + 1))
        for i in range(1, len(it)):
            self.SetItem(num, i, it[i])

        self.currentItem = num
        self.EnsureVisible(self.currentItem)
        self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self.changed = True
        return True

    def OnModify(self, item):
        it = (
         self.currentItem + 1, item[0], item[1], item[2])
        if self.currentItem == 0:
            nametxt = self.getColumnText(0, LotsListCtrl.NAME)
            if nametxt != item[0]:
                self.SetItem(0, LotsListCtrl.NAME, item[0])
                self.changed = True
            diurnaltxt = self.getColumnText(0, LotsListCtrl.DIURNAL)
            if diurnaltxt != item[2]:
                self.SetItem(0, LotsListCtrl.DIURNAL, item[2])
                self.changed = True
        else:
            if self.checkName(it[LotsListCtrl.NAME], self.currentItem):
                dlgm = wx.MessageDialog(self, mtexts.txtslotsdlg['LotAlreadyExists'], '', wx.OK | wx.ICON_INFORMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
                return
            for i in range(1, len(it)):
                self.SetItem(self.currentItem, i, it[i])

            self.changed = True
        self.EnsureVisible(self.currentItem)
        self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def OnRemove(self):
        if self.currentItem != 0:
            dlg = wx.MessageDialog(self, mtexts.txtscommon['AreYouSure'], mtexts.txtscommon['Confirm'], wx.YES_NO | wx.ICON_QUESTION)
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                num = self.currentItem + 1
                linestodelete = [num - 1]
                linestodelete = self.isReferred(num, linestodelete)
                for i in range(num, self.GetItemCount()):
                    form = self.getColumnText(i, LotsListCtrl.FORMULA)
                    f1 = self.getFormula(form, 1)
                    f2 = self.getFormula(form, 2)
                    f3 = self.getFormula(form, 3)
                    fs = [f1, f2, f3]
                    ref = 0
                    for j in range(len(fs)):
                        if fs[j][0] == mtexts.txtslotsdlg['R']:
                            lord = fs[j][(-1)] == LotsListCtrl.LORDTXT
                            if lord:
                                ref = int(fs[j][1:-1])
                            else:
                                ref = int(fs[j][1:])
                            for k in range(len(linestodelete)):
                                if ref > linestodelete[k]:
                                    ref -= 1
                                    fs[j] = mtexts.txtslotsdlg['R'] + str(ref)
                                    if lord:
                                        fs[j] += LotsListCtrl.LORDTXT

                        formula = fs[0] + ' + ' + fs[1] + ' - ' + fs[2]
                        self.SetItem(i, LotsListCtrl.FORMULA, formula)

                for l in range(len(linestodelete)):
                    self.DeleteItem(linestodelete[l] - l)

                self.parent.removeRefs(len(linestodelete))
                for i in range(1, self.GetItemCount() + 1):
                    self.SetItem(i - 1, LotsListCtrl.NUM, str(i) + '.')

                if self.currentItem >= self.GetItemCount():
                    self.currentItem = self.GetItemCount() - 1
                    self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                else:
                    self.SetItemState(self.currentItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                self.changed = True
                self.removed = True
            dlg.Destroy()
        else:
            dlg = wx.MessageDialog(self, mtexts.txtslotsdlg['LoFCannotBeRemoved'], mtexts.txtscommon['Information'], wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()

    def OnRemoveAll(self):
        if self.GetItemCount() > 1:
            dlg = wx.MessageDialog(self, mtexts.txtscommon['AreYouSure'], mtexts.txtscommon['Confirm'], wx.YES_NO | wx.ICON_QUESTION)
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                num = self.GetItemCount()
                for i in range(1, num):
                    self.DeleteItem(1)

                self.currentItem = 0
                self.changed = True
                self.removed = True
            dlg.Destroy()
        else:
            dlg = wx.MessageDialog(self, mtexts.txtslotsdlg['LoFCannotBeRemoved'], mtexts.txtscommon['Information'], wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()

    def load(self, lotsobj):
        if lotsobj != None:
            idx = 1
            num = len(lotsobj)
            for i in range(num):
                fs = (lotsobj[i][lots.Lots.FORMULA][0], lotsobj[i][lots.Lots.FORMULA][1], lotsobj[i][lots.Lots.FORMULA][2])
                refordegs = (lotsobj[i][lots.Lots.REFORDEG][0], lotsobj[i][lots.Lots.REFORDEG][1], lotsobj[i][lots.Lots.REFORDEG][2])
                formula = ''
                for j in range(len(fs)):
                    if fs[j] == lots.Lots.DEG or fs[j] == lots.Lots.DEGLORD:
                        sign = refordegs[j] // chart.Chart.SIGN_DEG
                        deg = refordegs[j] % chart.Chart.SIGN_DEG
                        formula += str(deg) + self.parent.signsabbr[sign]
                        if fs[j] == lots.Lots.DEGLORD:
                            formula += LotsListCtrl.LORDTXT
                    elif fs[j] == lots.Lots.REF or fs[j] == lots.Lots.REFLORD:
                        formula += mtexts.txtslotsdlg['R'] + str(refordegs[j])
                        if fs[j] == lots.Lots.REFLORD:
                            formula += LotsListCtrl.LORDTXT
                    else:
                        formula += mtexts.lotstxts[fs[j]]
                    if j == 0:
                        formula += ' + '
                    if j == 1:
                        formula += ' - '

                diurnal = ''
                if lotsobj[i][3]:
                    diurnal = LotsListCtrl.DIURNALTXT
                self.lotsdata[idx] = (
                 lotsobj[i][0], formula, diurnal)
                idx += 1

        return

    def save(self, opts):
        if self.changed:
            opts.deleteLots()
            lotsobj = []
            for i in range(self.GetItemCount()):
                numtxt = self.getColumnText(i, LotsListCtrl.NUM)
                if numtxt[(-1)] == '.':
                    numtxt = numtxt[:-1]
                num = int(numtxt)
                name = self.getColumnText(i, LotsListCtrl.NAME)
                form = self.getColumnText(i, LotsListCtrl.FORMULA)
                f1 = self.getFormula(form, 1)
                f2 = self.getFormula(form, 2)
                f3 = self.getFormula(form, 3)
                fs = [f1, f2, f3]
                refordegs = [0, 0, 0]
                for j in range(len(fs)):
                    if fs[j][0].isdigit():
                        lord = fs[j][(-1)] == LotsListCtrl.LORDTXT
                        txt = ''
                        if lord:
                            txt = fs[j][:-1]
                        else:
                            txt = fs[j][:]
                        signtxt = txt[-3:]
                        sign = self.getSignFromText(signtxt)
                        if sign == -1:
                            continue
                        deg = int(txt[:-3])
                        refordegs[j] = sign * chart.Chart.SIGN_DEG + deg
                        fs[j] = mtexts.lotstxts[lots.Lots.DEG]
                        if lord:
                            fs[j] = mtexts.lotstxts[lots.Lots.DEGLORD]
                    elif fs[j][0] == mtexts.txtslotsdlg['R']:
                        lord = fs[j][(-1)] == LotsListCtrl.LORDTXT
                        if lord:
                            refordegs[j] = int(fs[j][1:-1])
                        else:
                            refordegs[j] = int(fs[j][1:])
                        fs[j] = mtexts.lotstxts[lots.Lots.REF]
                        if lord:
                            fs[j] = mtexts.lotstxts[lots.Lots.REFLORD]

                diurnal = self.getColumnText(i, LotsListCtrl.DIURNAL)
                diur = True
                if diurnal == '':
                    diur = False
                lotsobj.append((name, (mtexts.conv[fs[0]], mtexts.conv[fs[1]], mtexts.conv[fs[2]]), (refordegs[0], refordegs[1], refordegs[2]), diur))

            opts.lots = copy.deepcopy(lotsobj)
        return (
         self.changed, self.removed)

    def getSignFromText(self, s):
        for i in range(len(self.parent.signsabbr)):
            if self.parent.signsabbr[i] == s:
                return i

        return -1

    def getFormula(self, txt, num):
        if num == 1:
            idx = txt.find('+')
            f = txt[0:idx]
        elif num == 2:
            idx = txt.find('+')
            idx2 = txt.find('-')
            f = txt[idx + 1:idx2]
        else:
            idx = txt.find('-')
            f = txt[idx + 1:]
        f = f.strip()
        return f


class LotsDlg(wx.Dialog):

    def __init__(self, parent, opts):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, mtexts.txtslotsdlg['Lots'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.options = opts
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        COMBOSIZE = 70
        DIFF = 5
        if self.options.netbook:
            DIFF = 2
        self.sascref = wx.StaticBox(self, label='')
        refsizer = wx.StaticBoxSizer(self.sascref, wx.HORIZONTAL)
        label = wx.StaticText(self, -1, mtexts.txtslotsdlg['Ascendant'] + ':')
        refsizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, DIFF)
        self.refcb = wx.ComboBox(self, -1, mtexts.lotsreftxts[0], size=(COMBOSIZE, -1), choices=mtexts.lotsreftxts, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.refcb.SetStringSelection(mtexts.lotsreftxts[0])
        refsizer.Add(self.refcb, 0, wx.ALL, DIFF)
        # which sect's formulas the list shows; calculation always follows the chart
        label = wx.StaticText(self, -1, 'Formulas:')
        refsizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, DIFF)
        self.sectcb = wx.ComboBox(self, -1, 'Day', size=(COMBOSIZE+30, -1), choices=['Day', 'Night'], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.sectcb.SetSelection(1 if LotsDlg.isNightChart(parent) else 0)
        refsizer.Add(self.sectcb, 0, wx.ALL, DIFF)
        self.Bind(wx.EVT_COMBOBOX, self.onSect, id=self.sectcb.GetId())
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        vsubsizer.Add(refsizer, 1, wx.GROW | wx.ALIGN_LEFT | wx.RIGHT, 5)
        self.seditor = wx.StaticBox(self, label='')
        editorsizer = wx.StaticBoxSizer(self.seditor, wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtslotsdlg['Name'] + ':')
        editorsizer.Add(label, 0, wx.LEFT, DIFF)
        self.name = wx.TextCtrl(self, -1, '', size=(200, -1))
        self.name.SetMaxLength(40)
        editorsizer.Add(self.name, 0, wx.ALL, DIFF)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.acb = wx.ComboBox(self, -1, mtexts.lotstxts[0], size=(COMBOSIZE, -1), choices=mtexts.lotstxts, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.acb.SetStringSelection(mtexts.lotstxts[0])
        hsizer.Add(self.acb, 0, wx.ALL, DIFF)
        label = wx.StaticText(self, -1, '+(')
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.bcb = wx.ComboBox(self, -1, mtexts.lotstxts[0], size=(COMBOSIZE, -1), choices=mtexts.lotstxts, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.bcb.SetStringSelection(mtexts.lotstxts[0])
        hsizer.Add(self.bcb, 0, wx.ALL, DIFF)
        label = wx.StaticText(self, -1, '-')
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.ccb = wx.ComboBox(self, -1, mtexts.lotstxts[0], size=(COMBOSIZE, -1), choices=mtexts.lotstxts, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.ccb.SetStringSelection(mtexts.lotstxts[0])
        hsizer.Add(self.ccb, 0, wx.ALL, DIFF)
        label = wx.StaticText(self, -1, ')')
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        editorsizer.Add(hsizer, 0, wx.ALL, DIFF)
        self.diurnalckb = wx.CheckBox(self, -1, mtexts.txtslotsdlg['Diurnal'])
        editorsizer.Add(self.diurnalckb, 0, wx.ALL, DIFF)
        self.arrefnum = []
        for i in range(len(self.options.lots)):
            self.arrefnum.append(str(i + 1))

        self.sref = wx.StaticBox(self, label=mtexts.txtslotsdlg['Reference'])
        refsizer = wx.StaticBoxSizer(self.sref, wx.VERTICAL)
        hrefsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rcba = wx.ComboBox(self, -1, self.arrefnum[0], size=(COMBOSIZE, -1), choices=self.arrefnum, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.rcba.SetStringSelection(self.arrefnum[0])
        self.rcba.Enable(False)
        hrefsizer.Add(self.rcba, 0, wx.ALL, 5)
        label = wx.StaticText(self, -1, '  ')
        hrefsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.rcbb = wx.ComboBox(self, -1, self.arrefnum[0], size=(COMBOSIZE, -1), choices=self.arrefnum, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.rcbb.SetStringSelection(self.arrefnum[0])
        self.rcbb.Enable(False)
        hrefsizer.Add(self.rcbb, 0, wx.ALL, 5)
        label = wx.StaticText(self, -1, ' ')
        hrefsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.rcbc = wx.ComboBox(self, -1, self.arrefnum[0], size=(COMBOSIZE, -1), choices=self.arrefnum, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.rcbc.SetStringSelection(self.arrefnum[0])
        self.rcbc.Enable(False)
        hrefsizer.Add(self.rcbc, 0, wx.ALL, 5)
        refsizer.Add(hrefsizer, 0, wx.ALL, 0)
        editorsizer.Add(refsizer, 0, wx.ALL | wx.GROW, 5)
        self.signs = (
         mtexts.txtscommon['Aries'], mtexts.txtscommon['Taurus'], mtexts.txtscommon['Gemini'], mtexts.txtscommon['Cancer'], mtexts.txtscommon['Leo'], mtexts.txtscommon['Virgo'], mtexts.txtscommon['Libra'], mtexts.txtscommon['Scorpio'], mtexts.txtscommon['Sagittarius'], mtexts.txtscommon['Capricorn'], mtexts.txtscommon['Aquarius'], mtexts.txtscommon['Pisces'])
        self.signsabbr = (
         mtexts.txtscommon['Ari'], mtexts.txtscommon['Tau'], mtexts.txtscommon['Gem'], mtexts.txtscommon['Can'], mtexts.txtscommon['Leo'], mtexts.txtscommon['Vir'], mtexts.txtscommon['Lib'], mtexts.txtscommon['Sco'], mtexts.txtscommon['Sag'], mtexts.txtscommon['Cap'], mtexts.txtscommon['Aqu'], mtexts.txtscommon['Pis'])
        self.sdeg = wx.StaticBox(self, label=mtexts.txtslotsdlg['Degrees'])
        degsizer = wx.StaticBoxSizer(self.sdeg, wx.VERTICAL)
        hdegsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dcba = wx.ComboBox(self, -1, self.signs[0], size=(COMBOSIZE, -1), choices=self.signs, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.dcba.SetStringSelection(self.signs[0])
        self.dcba.Enable(False)
        hdegsizer.Add(self.dcba, 0, wx.ALL, DIFF)
        label = wx.StaticText(self, -1, '  ')
        hdegsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.dcbb = wx.ComboBox(self, -1, self.signs[0], size=(COMBOSIZE, -1), choices=self.signs, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.dcbb.SetStringSelection(self.signs[0])
        self.dcbb.Enable(False)
        hdegsizer.Add(self.dcbb, 0, wx.ALL, DIFF)
        label = wx.StaticText(self, -1, ' ')
        hdegsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.dcbc = wx.ComboBox(self, -1, self.signs[0], size=(COMBOSIZE, -1), choices=self.signs, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.dcbc.SetStringSelection(self.signs[0])
        self.dcbc.Enable(False)
        hdegsizer.Add(self.dcbc, 0, wx.ALL, DIFF)
        degsizer.Add(hdegsizer, 0, wx.ALL, 0)
        hdegsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.dega = wx.TextCtrl(self, -1, '0', validator=intvalidator.IntValidator(0, 29), size=(COMBOSIZE, -1))
        self.dega.Enable(False)
        hdegsizer2.Add(self.dega, 0, wx.ALL, DIFF)
        label = wx.StaticText(self, -1, '  ')
        hdegsizer2.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.degb = wx.TextCtrl(self, -1, '0', validator=intvalidator.IntValidator(0, 29), size=(COMBOSIZE, -1))
        self.degb.Enable(False)
        hdegsizer2.Add(self.degb, 0, wx.ALL, DIFF)
        label = wx.StaticText(self, -1, ' ')
        hdegsizer2.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.degc = wx.TextCtrl(self, -1, '0', validator=intvalidator.IntValidator(0, 29), size=(COMBOSIZE, -1))
        self.degc.Enable(False)
        hdegsizer2.Add(self.degc, 0, wx.ALL, DIFF)
        degsizer.Add(hdegsizer2, 0, wx.ALL, 0)
        editorsizer.Add(degsizer, 0, wx.ALL | wx.GROW, DIFF)
        vsubsizer.Add(editorsizer, 0, wx.ALIGN_LEFT | wx.RIGHT, DIFF)
        susehouses = wx.StaticBox(self, label='')
        usehousessizer = wx.StaticBoxSizer(susehouses, wx.VERTICAL)
        self.usehousesckb = wx.CheckBox(self, -1, mtexts.txtslotsdlg['UseHousesNotDegrees'])
        usehousessizer.Add(self.usehousesckb, 0, wx.ALL, DIFF)
        vsubsizer.Add(usehousessizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.RIGHT, 5)
        sbtns = wx.StaticBox(self, label='')
        btnssizer = wx.StaticBoxSizer(sbtns, wx.VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        ID_Add = wx.NewId()
        btnAdd = wx.Button(self, ID_Add, mtexts.txtslotsdlg['Add'])
        vsizer.Add(btnAdd, 0, wx.GROW | wx.ALL, DIFF)
        ID_Modify = wx.NewId()
        btnModify = wx.Button(self, ID_Modify, mtexts.txtslotsdlg['Modify'])
        vsizer.Add(btnModify, 0, wx.GROW | wx.ALL, DIFF)
        if not self.options.netbook:
            ID_Remove = wx.NewId()
            btnRemove = wx.Button(self, ID_Remove, mtexts.txtslotsdlg['Remove'])
            vsizer.Add(btnRemove, 0, wx.GROW | wx.ALL, 5)
            ID_RemoveAll = wx.NewId()
            btnRemoveAll = wx.Button(self, ID_RemoveAll, mtexts.txtslotsdlg['RemoveAll'])
            vsizer.Add(btnRemoveAll, 0, wx.GROW | wx.ALL, 5)
        btnssizer.Add(vsizer, 0, wx.GROW | wx.ALL, DIFF)
        vsubsizer.Add(btnssizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.RIGHT, 5)
        mhsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        slots = wx.StaticBox(self, label='')
        lotssizer = wx.StaticBoxSizer(slots, wx.VERTICAL)
        ID_Lots = wx.NewId()
        self.li = LotsListCtrl(self, ID_Lots, self.options.lots, size=(430, -1), style=wx.LC_VRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.li.setNight(self.sectcb.GetSelection() == 1)
        lotssizer.Add(self.li, 1, wx.GROW | wx.ALL, 5)
        self.li.setVisibility(opts)
        mhsizer.Add(lotssizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 0)
        mvsizer.Add(mhsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.OnAdd, id=ID_Add)
        self.Bind(wx.EVT_BUTTON, self.OnModify, id=ID_Modify)
        if not self.options.netbook:
            self.Bind(wx.EVT_BUTTON, self.OnRemove, id=ID_Remove)
            self.Bind(wx.EVT_BUTTON, self.OnRemoveAll, id=ID_RemoveAll)
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
        DIFF = 10
        if self.options.netbook:
            DIFF = 2
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, DIFF)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        self.Bind(wx.EVT_COMBOBOX, self.onFormulaA, id=self.acb.GetId())
        self.Bind(wx.EVT_COMBOBOX, self.onFormulaB, id=self.bcb.GetId())
        self.Bind(wx.EVT_COMBOBOX, self.onFormulaC, id=self.ccb.GetId())
        self.li.initFill()
        btnOk.SetFocus()

    @staticmethod
    def isNightChart(parent):
        """True if the chart open in the main window is a night chart, by the same test the lots use"""
        chrt = getattr(parent, 'horoscope', None)
        if chrt is None or getattr(parent, 'splash', True):
            return False
        if chrt.options.usedaynightorb:
            return not chrt.abovehorizonwithorb
        return not chrt.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].abovehorizon

    def onSect(self, event):
        self.li.setNight(self.sectcb.GetSelection() == 1)

    def onFormulaA(self, event):
        valref = self.acb.GetCurrentSelection() == lots.Lots.REF or self.acb.GetCurrentSelection() == lots.Lots.REFLORD
        valdeg = self.acb.GetCurrentSelection() == lots.Lots.DEG or self.acb.GetCurrentSelection() == lots.Lots.DEGLORD
        if not valref:
            self.rcba.SetStringSelection('1')
        if not valdeg:
            self.dcba.SetStringSelection(mtexts.txtscommon['Aries'])
            self.dega.SetValue('0')
        self.rcba.Enable(valref)
        self.dcba.Enable(valdeg)
        self.dega.Enable(valdeg)

    def onFormulaB(self, event):
        valref = self.bcb.GetCurrentSelection() == lots.Lots.REF or self.bcb.GetCurrentSelection() == lots.Lots.REFLORD
        valdeg = self.bcb.GetCurrentSelection() == lots.Lots.DEG or self.bcb.GetCurrentSelection() == lots.Lots.DEGLORD
        if not valref:
            self.rcbb.SetStringSelection('1')
        if not valdeg:
            self.dcbb.SetStringSelection(mtexts.txtscommon['Aries'])
            self.degb.SetValue('0')
        self.rcbb.Enable(valref)
        self.dcbb.Enable(valdeg)
        self.degb.Enable(valdeg)

    def onFormulaC(self, event):
        valref = self.ccb.GetCurrentSelection() == lots.Lots.REF or self.ccb.GetCurrentSelection() == lots.Lots.REFLORD
        valdeg = self.ccb.GetCurrentSelection() == lots.Lots.DEG or self.ccb.GetCurrentSelection() == lots.Lots.DEGLORD
        if not valref:
            self.rcbc.SetStringSelection('1')
        if not valdeg:
            self.dcbc.SetStringSelection(mtexts.txtscommon['Aries'])
            self.degc.SetValue('0')
        self.rcbc.Enable(valref)
        self.dcbc.Enable(valdeg)
        self.degc.Enable(valdeg)

    def OnAdd(self, event):
        name = self.name.GetValue()
        if name == '':
            dlgm = wx.MessageDialog(self, mtexts.txtslotsdlg['LotNameEmpty'], '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        f1 = mtexts.lotstxts[self.acb.GetCurrentSelection()]
        f2 = mtexts.lotstxts[self.bcb.GetCurrentSelection()]
        f3 = mtexts.lotstxts[self.ccb.GetCurrentSelection()]
        arformcbs = (
         self.acb, self.bcb, self.ccb)
        arrefcbs = (self.rcba, self.rcbb, self.rcbc)
        ardegcbs = (self.dcba, self.dcbb, self.dcbc)
        ardegdegs = (self.dega, self.degb, self.degc)
        fs = [f1, f2, f3]
        for i in range(len(fs)):
            if arformcbs[i].GetCurrentSelection() == lots.Lots.DEG or arformcbs[i].GetCurrentSelection() == lots.Lots.DEGLORD:
                if int(ardegdegs[i].GetValue()) > chart.Chart.SIGN_DEG:
                    dlg = wx.MessageDialog(self, mtexts.txtslotsdlg['DegreeProblem'] + ' ' + str(chart.Chart.SIGN_DEG), '', wx.OK | wx.ICON_INFORMATION)
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
                sign = ardegcbs[i].GetCurrentSelection()
                fs[i] = ardegdegs[i].GetValue() + self.signsabbr[sign]
                if arformcbs[i].GetCurrentSelection() == lots.Lots.DEGLORD:
                    fs[i] += LotsListCtrl.LORDTXT

        for i in range(len(fs)):
            if arformcbs[i].GetCurrentSelection() == lots.Lots.REF or arformcbs[i].GetCurrentSelection() == lots.Lots.REFLORD:
                lotidx = arrefcbs[i].GetCurrentSelection() + 1
                if self.li.isReferring(lotidx):
                    dlg = wx.MessageDialog(self, mtexts.txtslotsdlg['AlreadyReferring'], '', wx.OK | wx.ICON_INFORMATION)
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
                fs[i] = mtexts.txtslotsdlg['R'] + str(lotidx)
                if arformcbs[i].GetCurrentSelection() == lots.Lots.REFLORD:
                    fs[i] += LotsListCtrl.LORDTXT

        formula = fs[0] + ' + ' + fs[1] + ' - ' + fs[2]
        diurnal = ''
        if self.diurnalckb.GetValue():
            diurnal = LotsListCtrl.DIURNALTXT
        item = []
        item.append(name)
        item.append(formula)
        item.append(diurnal)
        res = self.li.OnAdd(item)
        if res:
            arrefcbs = (
             self.rcba, self.rcbb, self.rcbc)
            for i in range(len(arrefcbs)):
                arrefcbs[i].Append(str(self.li.GetItemCount()))

    def OnModify(self, event):
        name = self.name.GetValue()
        if name == '':
            dlgm = wx.MessageDialog(self, mtexts.txtslotsdlg['LotNameEmpty'], '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        diurnal = ''
        if self.diurnalckb.GetValue():
            diurnal = LotsListCtrl.DIURNALTXT
        if self.li.getCurrItem() == 0:
            dlgm = wx.MessageDialog(self, mtexts.txtslotsdlg['FormulaWontBeCopied'], '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            item = (
             name, '', diurnal)
        else:
            f1 = mtexts.lotstxts[self.acb.GetCurrentSelection()]
            f2 = mtexts.lotstxts[self.bcb.GetCurrentSelection()]
            f3 = mtexts.lotstxts[self.ccb.GetCurrentSelection()]
            arformcbs = (
             self.acb, self.bcb, self.ccb)
            arrefcbs = (self.rcba, self.rcbb, self.rcbc)
            ardegcbs = (self.dcba, self.dcbb, self.dcbc)
            ardegdegs = (self.dega, self.degb, self.degc)
            fs = [f1, f2, f3]
            for i in range(len(fs)):
                if arformcbs[i].GetCurrentSelection() == lots.Lots.DEG or arformcbs[i].GetCurrentSelection() == lots.Lots.DEGLORD:
                    if int(ardegdegs[i].GetValue()) > chart.Chart.SIGN_DEG:
                        dlg = wx.MessageDialog(self, mtexts.txtslotsdlg['DegreeProblem'] + ' ' + str(chart.Chart.SIGN_DEG), '', wx.OK | wx.ICON_INFORMATION)
                        dlg.ShowModal()
                        dlg.Destroy()
                        return
                    sign = ardegcbs[i].GetCurrentSelection()
                    fs[i] = ardegdegs[i].GetValue() + self.signsabbr[sign]
                    if arformcbs[i].GetCurrentSelection() == lots.Lots.DEGLORD:
                        fs[i] += LotsListCtrl.LORDTXT

            for i in range(len(fs)):
                if arformcbs[i].GetCurrentSelection() == lots.Lots.REF or arformcbs[i].GetCurrentSelection() == lots.Lots.REFLORD:
                    lotidx = self.li.getCurrItem() + 1
                    if self.li.isReferred(lotidx):
                        dlg = wx.MessageDialog(self, mtexts.txtslotsdlg['AlreadyReferred'], '', wx.OK | wx.ICON_INFORMATION)
                        dlg.ShowModal()
                        dlg.Destroy()
                        return
                    lotidx = arrefcbs[i].GetCurrentSelection() + 1
                    if self.li.isReferring(lotidx):
                        dlg = wx.MessageDialog(self, mtexts.txtslotsdlg['AlreadyReferring'], '', wx.OK | wx.ICON_INFORMATION)
                        dlg.ShowModal()
                        dlg.Destroy()
                        return
                    fs[i] = mtexts.txtslotsdlg['R'] + str(lotidx)
                    if arformcbs[i].GetCurrentSelection() == lots.Lots.REFLORD:
                        fs[i] += LotsListCtrl.LORDTXT

            formula = fs[0] + ' + ' + fs[1] + ' - ' + fs[2]
            item = []
            item.append(name)
            item.append(formula)
            item.append(diurnal)
        self.li.OnModify(item)

    def OnRemove(self, event):
        self.li.OnRemove()

    def OnRemoveAll(self, event):
        self.li.OnRemoveAll()

    def removeRefs(self, num):
        arrefcbs = (
         self.rcba, self.rcbb, self.rcbc)
        for i in range(len(arrefcbs)):
            ar = arrefcbs[i].Items[:]
            del ar[-num:]
            arrefcbs[i].Items = ar[:]

    def fillEditor(self, item):
        self.name.SetValue(item[lots.Lots.NAME])
        arformcbs = (
         self.acb, self.bcb, self.ccb)
        arrefcbs = (self.rcba, self.rcbb, self.rcbc)
        ardegcbs = (self.dcba, self.dcbb, self.dcbc)
        ardegdegs = (self.dega, self.degb, self.degc)
        for i in range(len(arformcbs)):
            arformcbs[i].SetStringSelection(mtexts.lotstxts[item[lots.Lots.FORMULA][i]])
            valref = item[lots.Lots.FORMULA][i] == lots.Lots.REF or item[lots.Lots.FORMULA][i] == lots.Lots.REFLORD
            valdeg = item[lots.Lots.FORMULA][i] == lots.Lots.DEG or item[lots.Lots.FORMULA][i] == lots.Lots.DEGLORD
            if valref:
                arrefcbs[i].SetStringSelection(str(item[lots.Lots.REFORDEG][i]))
            else:
                arrefcbs[i].SetStringSelection('1')
            if valdeg:
                degsign = item[lots.Lots.REFORDEG][i] // chart.Chart.SIGN_DEG
                degval = item[lots.Lots.REFORDEG][i] % chart.Chart.SIGN_DEG
                ardegcbs[i].SetStringSelection(self.signs[degsign])
                ardegdegs[i].SetValue(str(degval))
            else:
                ardegcbs[i].SetStringSelection(mtexts.txtscommon['Aries'])
                ardegdegs[i].SetValue('0')
            arrefcbs[i].Enable(valref)
            ardegcbs[i].Enable(valdeg)
            ardegdegs[i].Enable(valdeg)

        self.diurnalckb.SetValue(item[lots.Lots.DIURNAL])

    def fill(self, opts):
        self.refcb.SetStringSelection(mtexts.lotsreftxts[opts.lotsref])
        self.usehousesckb.SetValue(opts.lotsusehouses)

    def check(self, opts):
        changed = False
        removed = False
        if self.refcb.GetCurrentSelection() != opts.lotsref:
            opts.lotsref = self.refcb.GetCurrentSelection()
            changed = True
        ch, rem = self.li.save(opts)
        if ch:
            changed = True
            if rem:
                removed = True
        checkedlots = []
        for k in range(self.li.GetItemCount()):
            checkedlots.append(self.li.IsChecked(k))

        if opts.lotsvisible == None:
            opts.lotsvisible = checkedlots[:]
            changed = True
        elif len(opts.lotsvisible) != len(checkedlots):
            del opts.lotsvisible
            opts.lotsvisible = checkedlots[:]
            changed = True
        else:
            for i in range(len(checkedlots)):
                if opts.lotsvisible[i] != checkedlots[i]:
                    opts.lotsvisible[i] = checkedlots[i]
                    changed = True

        if opts.lotsusehouses != self.usehousesckb.GetValue():
            opts.lotsusehouses = self.usehousesckb.GetValue()
            changed = True
        return (changed, removed)
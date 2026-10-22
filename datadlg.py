# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
import wx
import chart
import intvalidator
import rangechecker
import placesdlg
import mtexts
import util
from auto_timezone import resolve_timezone, TimezoneLookupError
import tradoptions
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(i18n.tr(provider))

class DataDlg(wx.Dialog):
    PLUSCHOICES = (
     '+', '-')

    def __init__(self, parent, langid, netbook):
        self.langid = langid
        self.netbook = netbook
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, -1, i18n.tr(mtexts.txtsdatadlg['Data']), pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mhsizer = wx.BoxSizer(wx.HORIZONTAL)
        sname = wx.StaticBox(self, label='')
        namesizer = wx.StaticBoxSizer(sname, wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Name'] + ':')
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.name = wx.TextCtrl(self, -1, '', size=(220, -1))
        self.name.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpName']))
        self.name.SetMaxLength(20)
        hsizer.Add(self.name, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Gender'] + ':')
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        self.genderrbM = wx.RadioButton(self, -1, i18n.tr(mtexts.txtsdatadlg['Male']), style=wx.RB_GROUP)
        vsubsizer.Add(self.genderrbM, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        self.genderrbF = wx.RadioButton(self, -1, i18n.tr(mtexts.txtsdatadlg['Female']))
        vsubsizer.Add(self.genderrbF, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        hsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Type'] + ':')
        hsubsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.typecb = wx.ComboBox(self, -1, mtexts.typeList[0], size=(140, -1), choices=i18n.tr(mtexts.typeList), style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.typecb.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpType']))
        hsubsizer.Add(self.typecb, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hsizer.Add(hsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        vsizer.Add(hsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, 5)
        namesizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        vsubsizer = wx.BoxSizer(wx.VERTICAL)
        hsubsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsubsizer.Add(namesizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.LEFT, 0)
        rnge = 3000
        checker = rangechecker.RangeChecker()
        if checker.isExtended():
            rnge = 5000
        self.stime = wx.StaticBox(self, label='')
        timesizer = wx.StaticBoxSizer(self.stime, wx.VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.timeckb = wx.CheckBox(self, -1, i18n.tr(mtexts.txtsdatadlg['BC']))
        vsizer.Add(self.timeckb, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        fgsizer = wx.FlexGridSizer(0, 3, 0, 0)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Year'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,
                                                                                                  -1))
        vvsizer.Add(self.year, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        if checker.isExtended():
            self.year.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpYear']))
        else:
            self.year.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpYear2']))
        self.year.SetMaxLength(4)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Month'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.month = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,
                                                                                                 -1))
        self.month.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpMonth']))
        self.month.SetMaxLength(2)
        vvsizer.Add(self.month, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Day'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.day = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 31), size=(50,
                                                                                               -1))
        self.day.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpDay']))
        self.day.SetMaxLength(2)
        vvsizer.Add(self.day, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Hour'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.hour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 23), size=(50,
                                                                                                -1))
        self.hour.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpHour']))
        self.hour.SetMaxLength(2)
        vvsizer.Add(self.hour, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Min'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.minute = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,
                                                                                                  -1))
        self.minute.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpMin']))
        self.minute.SetMaxLength(2)
        vvsizer.Add(self.minute, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Sec'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        self.sec = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(50,
                                                                                               -1))
        self.sec.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpMin']))
        self.sec.SetMaxLength(2)
        vvsizer.Add(self.sec, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 0)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsizer.Add(fgsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        timesizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        vvsubsizer = wx.BoxSizer(wx.VERTICAL)
        vvsubsizer.Add(timesizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.RIGHT, 5)
        fgsizer = wx.FlexGridSizer(0, 4, 0, 0)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.splace = wx.StaticBox(self, label='')
        placesizer = wx.StaticBoxSizer(self.splace, wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Long'] + ':')
        fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Deg'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.londeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 180), size=(40,
                                                                                                   -1))
        self.londeg.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpLonDeg']))
        self.londeg.SetMaxLength(3)
        vvsizer.Add(self.londeg, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Min'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.lonmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.lonmin.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpMin']))
        self.lonmin.SetMaxLength(2)
        vvsizer.Add(self.lonmin, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        self.placerbE = wx.RadioButton(self, -1, i18n.tr(mtexts.txtsdatadlg['E']), style=wx.RB_GROUP)
        vvsizer.Add(self.placerbE, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        self.placerbW = wx.RadioButton(self, -1, i18n.tr(mtexts.txtsdatadlg['W']))
        vvsizer.Add(self.placerbW, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Lat'] + ':')
        fgsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Deg'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.latdeg = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 90), size=(40,
                                                                                                  -1))
        self.latdeg.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpLatDeg']))
        self.latdeg.SetMaxLength(2)
        vvsizer.Add(self.latdeg, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Min'] + ':')
        vvsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.latmin = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                  -1))
        self.latmin.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpMin']))
        self.latmin.SetMaxLength(2)
        vvsizer.Add(self.latmin, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        self.placerbN = wx.RadioButton(self, -1, i18n.tr(mtexts.txtsdatadlg['N']), style=wx.RB_GROUP)
        vvsizer.Add(self.placerbN, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        self.placerbS = wx.RadioButton(self, -1, i18n.tr(mtexts.txtsdatadlg['S']))
        vvsizer.Add(self.placerbS, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.LEFT, 2)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vsizer.Add(fgsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        ID_PlaceButton = wx.NewId()
        placebtn = wx.Button(self, ID_PlaceButton, mtexts.txtsdatadlg['Place'] + ':', size=(100,
                                                                                            -1))
        vsizer.Add(placebtn, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.birthplace = wx.TextCtrl(self, -1, '', size=(170, -1))
        self.birthplace.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpPlace']))
        self.birthplace.SetMaxLength(20)
        vsizer.Add(self.birthplace, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        placesizer.Add(vsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        vvsubsizer.Add(placesizer, 0, wx.ALIGN_LEFT | wx.RIGHT, 5)
        hsubsizer.Add(vvsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        self.szone = wx.StaticBox(self, label='')
        zonesizer = wx.StaticBoxSizer(self.szone, wx.VERTICAL)
        self.calcb = wx.ComboBox(self, -1, mtexts.calList[0], size=(80, -1), choices=i18n.tr(mtexts.calList), style=wx.CB_DROPDOWN | wx.CB_READONLY)
        zonesizer.Add(self.calcb, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 5)
        self.zonecb = wx.ComboBox(self, -1, mtexts.zoneList[0], size=(80, -1), choices=i18n.tr(mtexts.zoneList), style=wx.CB_DROPDOWN | wx.CB_READONLY)
        zonesizer.Add(self.zonecb, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 5)
        hhsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.gmtlabel = wx.StaticText(self, -1, i18n.tr(mtexts.txtsdatadlg['GMT']))
        hhsizer.Add(self.gmtlabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.pluscb = wx.ComboBox(self, -1, DataDlg.PLUSCHOICES[0], size=(50, -1), choices=i18n.tr(DataDlg.PLUSCHOICES), style=wx.CB_DROPDOWN | wx.CB_READONLY)
        hhsizer.Add(self.pluscb, 0, wx.LEFT, 5)
        zonesizer.Add(hhsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        fgsizer = wx.FlexGridSizer(0, 2, 0, 0)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        self.zhourlabel = wx.StaticText(self, -1, mtexts.txtsdatadlg['Hour'] + ':')
        vvsizer.Add(self.zhourlabel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.zhour = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 12), size=(40,
                                                                                                 -1))
        self.zhour.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpZoneHour']))
        self.zhour.SetMaxLength(2)
        vvsizer.Add(self.zhour, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vvsizer = wx.BoxSizer(wx.VERTICAL)
        self.zminutelabel = wx.StaticText(self, -1, mtexts.txtsdatadlg['Min'] + ':')
        vvsizer.Add(self.zminutelabel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        self.zminute = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 59), size=(40,
                                                                                                   -1))
        self.zminute.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpMin']))
        self.zminute.SetMaxLength(2)
        vvsizer.Add(self.zminute, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 5)
        fgsizer.Add(vvsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        zonesizer.Add(fgsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.daylightckb = wx.CheckBox(self, -1, i18n.tr(mtexts.txtsdatadlg['Daylight']))
        zonesizer.Add(self.daylightckb, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        auto_zone_btn = wx.Button(self, -1, i18n.tr('Auto time zone (date + location)'))
        zonesizer.Add(auto_zone_btn, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.onAutoTimezone, auto_zone_btn)
        self.daylightckb.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpDaylight']))
        vvsubsizer = wx.BoxSizer(wx.VERTICAL)
        vvsubsizer.Add(zonesizer, 2, wx.ALIGN_LEFT | wx.ALL, 0)
        self.sphs = wx.StaticBox(self, label=i18n.tr(mtexts.txtsdatadlg['PlanetaryHour']))
        hourssizer = wx.StaticBoxSizer(self.sphs, wx.VERTICAL)
        label = wx.StaticText(self, -1, mtexts.txtsdatadlg['Altitude'] + ':')
        hourssizer.Add(label, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.alt = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, 10000), size=(60,
                                                                                                  -1))
        self.alt.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpAltitude']))
        self.alt.SetMaxLength(5)
        hhsubsizer = wx.BoxSizer(wx.HORIZONTAL)
        hhsubsizer.Add(self.alt, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        label = wx.StaticText(self, -1, 'm')
        hhsubsizer.Add(label, 0, wx.ALIGN_CENTER | wx.LEFT, 2)
        hourssizer.Add(hhsubsizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vvsubsizer.Add(hourssizer, 1, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 0)
        hsubsizer.Add(vvsubsizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 0)
        vsubsizer.Add(hsubsizer, 0, wx.ALIGN_LEFT | wx.ALL, 0)
        mhsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, 5)
        self.snotes = wx.StaticBox(self, label=i18n.tr(mtexts.txtsdatadlg['Notes']))
        notessizer = wx.StaticBoxSizer(self.snotes, wx.VERTICAL)
        self.notes = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE, size=(250, -1))
        self.notes.SetHelpText(i18n.tr(mtexts.txtsdatadlg['HelpNotes']))
        # GTK cannot limit the length of multiline text
        if wx.Platform == '__WXMSW__':
            self.notes.SetMaxLength(500)
        notessizer.Add(self.notes, 1, wx.ALIGN_LEFT | wx.ALL, 0)
        mhsizer.Add(notessizer, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 0)
        mvsizer.Add(mhsizer, 0, wx.ALIGN_LEFT | wx.TOP | wx.RIGHT, 5)
        btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != '__WXMSW__':
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        btnOk = wx.Button(self, wx.ID_OK, i18n.tr(mtexts.txtscommon['Ok']))
        btnOk.SetHelpText(i18n.tr(mtexts.txtscommon['HelpOk']))
        btnOk.SetDefault()
        btnsizer.AddButton(btnOk)
        btn = wx.Button(self, wx.ID_CANCEL, i18n.tr(mtexts.txtscommon['Cancel']))
        btn.SetHelpText(i18n.tr(mtexts.txtscommon['HelpCancel']))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        DIFF = 10
        if self.netbook:
            DIFF = 2
        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, DIFF)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.onPlaceButton, id=ID_PlaceButton)
        self.Bind(wx.EVT_COMBOBOX, self.onZone, id=self.zonecb.GetId())
        self.name.SetFocus()

    def onOK(self, event):
        if self.Validate() and self.stime.Validate() and self.splace.Validate() and self.szone.Validate() and self.sphs:
            if util.checkDate(int(self.year.GetValue()), int(self.month.GetValue()), int(self.day.GetValue())):
                self.Close()
                self.SetReturnCode(wx.ID_OK)
            else:
                dlgm = wx.MessageDialog(None, mtexts.txtsdatadlg['InvalidDate'] + ' (' + self.year.GetValue() + '.' + self.month.GetValue() + '.' + self.day.GetValue() + '.)', i18n.tr(mtexts.txtsdatadlg['Error']), wx.OK | wx.ICON_EXCLAMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
        return

    def onAutoTimezone(self, event, quiet=False):
        """Explicit lookup; existing charts/manual edits are never changed silently.
        quiet (after choosing a place): no messages when no zone can be given."""
        if self.timeckb.GetValue():
            if quiet:
                return
            wx.MessageBox(i18n.tr('Automatic time zones require an AD/CE date. Use manual settings for BC dates.'),
                          i18n.tr('Automatic time zone'), wx.OK | wx.ICON_WARNING, self)
            return
        if self.calcb.GetCurrentSelection() != chart.Time.GREGORIAN:
            if quiet:
                return
            wx.MessageBox(i18n.tr('Automatic time zones require a Gregorian calendar date. Use manual settings for Julian dates.'),
                          i18n.tr('Automatic time zone'), wx.OK | wx.ICON_WARNING, self)
            return
        try:
            lat = int(self.latdeg.GetValue()) + int(self.latmin.GetValue()) / 60.0
            lon = int(self.londeg.GetValue()) + int(self.lonmin.GetValue()) / 60.0
            if self.placerbS.GetValue():
                lat = -lat
            if self.placerbW.GetValue():
                lon = -lon
            name, offset_minutes, dst, warning = resolve_timezone(
                int(self.year.GetValue()), int(self.month.GetValue()),
                int(self.day.GetValue()), int(self.hour.GetValue()),
                int(self.minute.GetValue()), int(self.sec.GetValue()), lat, lon)
        except (TimezoneLookupError, ValueError) as exc:
            if quiet:
                return
            wx.MessageBox(str(exc), i18n.tr('Automatic time zone'),
                          wx.OK | wx.ICON_WARNING, self)
            return
        sign = '+' if offset_minutes >= 0 else '-'
        hours, minutes = divmod(abs(offset_minutes), 60)
        confirmation = ('IANA zone: %s\nStandard GMT offset: %s%02d:%02d\n'
                        'Daylight saving: %s\n\n%s\n\nApply to chart?'
                        % (name, sign, hours, minutes, 'Yes' if dst else 'No',
                           warning or 'Please confirm the offset is correct.'))
        if wx.MessageBox(i18n.tr(confirmation), i18n.tr('Automatic time zone'),
                         wx.YES_NO | wx.ICON_QUESTION, self) != wx.YES:
            return
        self.zonecb.SetSelection(chart.Time.ZONE)
        self.enableGMT(True)
        self.pluscb.SetStringSelection(sign)
        self.zhour.SetValue(str(hours))
        self.zminute.SetValue(str(minutes))
        self.daylightckb.SetValue(dst)

    def onZone(self, event):
        self.enableGMT(self.zonecb.GetCurrentSelection() == 0)

    def enableGMT(self, enable):
        self.gmtlabel.Enable(enable)
        self.pluscb.Enable(enable)
        self.zhourlabel.Enable(enable)
        self.zhour.Enable(enable)
        self.zminute.Enable(enable)
        self.zminutelabel.Enable(enable)

    def onPlaceButton(self, event):
        pdlg = placesdlg.PlacesDlg(self, self.langid, self.netbook)
        val = pdlg.ShowModal()
        if val == wx.ID_OK:
            if pdlg.li.currentItem != -1:
                place = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.PLACE)
                lon = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.LON)
                lat = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.LAT)
                zone = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.ZONE)
                alt = pdlg.li.getColumnText(pdlg.li.currentItem, placesdlg.PlaceListCtrl.ALT)
                self.birthplace.SetValue(place.strip())
                idx = lon.find('E')
                if idx == -1:
                    idx = lon.find('W')
                    self.placerbW.SetValue(True)
                else:
                    self.placerbE.SetValue(True)
                fr = 0
                if lon[0] == '0':
                    fr = 1
                self.londeg.SetValue(lon[fr:idx])
                idx += 1
                if lon[idx] == '0':
                    idx += 1
                self.lonmin.SetValue(lon[idx:])
                idx = lat.find('N')
                if idx == -1:
                    idx = lat.find('S')
                    self.placerbS.SetValue(True)
                else:
                    self.placerbN.SetValue(True)
                fr = 0
                if lat[0] == '0':
                    fr = 1
                self.latdeg.SetValue(lat[fr:idx])
                idx += 1
                if lat[idx] == '0':
                    idx += 1
                self.latmin.SetValue(lat[idx:])
                self.pluscb.SetStringSelection(zone[0])
                zone = zone[1:]
                idx = zone.find(':')
                self.zhour.SetValue(zone[0:idx])
                idx += 1
                if zone[idx] == '0':
                    idx += 1
                self.zminute.SetValue(zone[idx:])
                self.alt.SetValue(alt)
                # the place's zone is today's; offer the one in force on the birth date
                if tradoptions.get('place_timezone'):
                    self.onAutoTimezone(None, quiet=True)
        pdlg.Destroy()

    def initialize(self):
        self.timeckb.SetValue(False)
        self.name.SetValue('')
        self.genderrbM.SetValue(True)
        self.year.SetValue(str(1950))
        self.month.SetValue(str(1))
        self.day.SetValue(str(1))
        self.hour.SetValue(str(0))
        self.minute.SetValue(str(0))
        self.sec.SetValue(str(0))
        self.birthplace.SetValue('')
        self.londeg.SetValue(str(0))
        self.lonmin.SetValue(str(0))
        self.latdeg.SetValue(str(0))
        self.latmin.SetValue(str(0))
        self.placerbE.SetValue(True)
        self.placerbN.SetValue(True)
        self.typecb.SetStringSelection(mtexts.typeList[chart.Chart.RADIX])
        self.calcb.SetStringSelection(mtexts.calList[chart.Time.GREGORIAN])
        self.zonecb.SetStringSelection(mtexts.zoneList[chart.Time.ZONE])
        self.enableGMT(True)
        self.pluscb.SetStringSelection(DataDlg.PLUSCHOICES[0])
        self.zhour.SetValue(str(1))
        self.zminute.SetValue(str(0))
        self.daylightckb.SetValue(False)
        self.alt.SetValue(str(100))
        self.notes.Clear()

    def fill(self, chrt):
        self.name.SetValue(chrt.name)
        if chrt.male:
            self.genderrbM.SetValue(True)
        else:
            self.genderrbF.SetValue(True)
        self.typecb.SetStringSelection(mtexts.typeList[chrt.htype])
        self.year.SetValue(str(chrt.time.origyear))
        self.month.SetValue(str(chrt.time.origmonth))
        self.day.SetValue(str(chrt.time.origday))
        self.hour.SetValue(str(chrt.time.hour))
        self.minute.SetValue(str(chrt.time.minute))
        self.sec.SetValue(str(chrt.time.second))
        self.timeckb.SetValue(chrt.time.bc)
        self.calcb.SetStringSelection(mtexts.calList[chrt.time.cal])
        self.zonecb.SetStringSelection(mtexts.zoneList[chrt.time.zt])
        self.enableGMT(chrt.time.zt == chart.Time.ZONE)
        idx = 0
        if not chrt.time.plus:
            idx = 1
        self.pluscb.SetStringSelection(DataDlg.PLUSCHOICES[idx])
        self.zhour.SetValue(str(chrt.time.zh))
        self.zminute.SetValue(str(chrt.time.zm))
        self.daylightckb.SetValue(chrt.time.daylightsaving)
        self.birthplace.SetValue(chrt.place.placename)
        self.londeg.SetValue(str(chrt.place.deglon))
        self.lonmin.SetValue(str(chrt.place.minlon))
        if chrt.place.east:
            self.placerbE.SetValue(True)
        else:
            self.placerbW.SetValue(True)
        self.latdeg.SetValue(str(chrt.place.deglat))
        self.latmin.SetValue(str(chrt.place.minlat))
        if chrt.place.north:
            self.placerbN.SetValue(True)
        else:
            self.placerbS.SetValue(True)
        self.alt.SetValue(str(chrt.place.altitude))
        self.notes.SetValue(chrt.notes)

    def check(self, chrt):
        changed = False
        if self.name.GetValue() != chrt.name:
            changed = True
        elif self.genderrbM.GetValue() != chrt.male:
            changed = True
        elif self.typecb.GetCurrentSelection() != chrt.htype:
            changed = True
        elif self.notes.GetValue() != chrt.notes:
            changed = True
        elif int(self.year.GetValue()) != chrt.time.origyear:
            changed = True
        elif int(self.month.GetValue()) != chrt.time.origmonth:
            changed = True
        elif int(self.day.GetValue()) != chrt.time.origday:
            changed = True
        elif int(self.hour.GetValue()) != chrt.time.hour:
            changed = True
        elif int(self.minute.GetValue()) != chrt.time.minute:
            changed = True
        elif int(self.sec.GetValue()) != chrt.time.second:
            changed = True
        elif self.timeckb.GetValue() != chrt.time.bc:
            changed = True
        elif self.calcb.GetCurrentSelection() != chrt.time.cal:
            changed = True
        elif self.zonecb.GetCurrentSelection() != chrt.time.zt:
            changed = True
        idx = 0
        if not chrt.time.plus:
            idx = 1
        elif self.pluscb.GetCurrentSelection() != idx:
            changed = True
        elif int(self.zhour.GetValue()) != chrt.time.zh:
            changed = True
        elif int(self.zminute.GetValue()) != chrt.time.zm:
            changed = True
        elif int(self.daylightckb.GetValue()) != chrt.time.daylightsaving:
            changed = True
        elif self.birthplace.GetValue() != chrt.place.placename:
            changed = True
        elif int(self.londeg.GetValue()) != chrt.place.deglon:
            changed = True
        elif int(self.lonmin.GetValue()) != chrt.place.minlon:
            changed = True
        elif self.placerbE.GetValue() != chrt.place.east:
            changed = True
        elif int(self.latdeg.GetValue()) != chrt.place.deglat:
            changed = True
        elif int(self.latmin.GetValue()) != chrt.place.minlat:
            changed = True
        elif self.placerbN.GetValue() != chrt.place.north:
            changed = True
        elif self.alt.GetValue() != chrt.place.altitude:
            changed = True
        return changed
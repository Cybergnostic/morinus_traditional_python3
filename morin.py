# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
import wx
import wx.adv
import conditionswnd
import temperamentwnd
import zodiacalreleasing
import zodiacalreleasingwnd
import decennialswnd
import circumambulationwnd
import heliacalwnd
import fixedstaranglewnd
import fixedstarsworkspace
import hoursrisesetworkspace
import dodecacalcdlg
import starnames
import tradoptions
import tradoptsdlg
import chartlookdlg
import settingswnd
import commandsearch
import sidebar
import time as _time
import defaultsbtn
import returnslistframe
import os
import pickle
import datetime
from PIL import Image
import astrology
import houses
import planets
import chart
import common
import datadlg
import findtimedlg
import graphephemdlg
import graphephemframe
import ephemcalc
import ephemerisworkspace
import userpd
import primdirs
import mtexts
import util
import placidiansapd
import placidianutppd
import regiomontanpd
import campanianpd
import positionsframe
import positionsworkspace
import positionscatalog
import almutenchartframe
import almutentopicalsframe
import almutenzodsframe
import miscframe
import munposframe
import antisciaframe
import aspectsframe
import midpointsframe
import risesetframe
import speedsframe
import zodparsframe
import fixedstarsframe
import fixedstarsaspectsframe
import lotsframe
import stripframe
import hoursframe
import transitmframe
import profstableframe
import userframe
import firdariaframe
import primdirslistframe
import primdirsrangedlg
import graphchart
import comparegrid
import multiwheel
import squarechartframe
import transits
import revolutions
import revolutionsdlg
import transitframe
import suntransits
import suntransitsdlg
import timespacedlg
import secdir
import secdirframe
import secdirdlg
import stepperdlg
import electionstepperdlg
import electionsframe
import profdlg
import profections
import munprofections
import profectionsframe
import profectionstepperdlg
import profectiontablestepperdlg
import proftabledlg
import heliochartframe
import appearance1dlg
import appearance2dlg
import dignitiesdlg
import triplicitiesdlg
import termsdlg
import decansdlg
import almutenchartdlg
import almutentopicalsdlg
import colorsdlg
import primarydirsdlg
import primarydirsdlgsmall
import primarykeysdlg
import pdsinchartdlgopts
import syzygydlg
import lunationnavigator
import transitsearch
import lotsdlg
import fixedstarsdlg
import profdlgopts
import firdariadlg
import defaultlocdlg
import ayanamshadlg
import transitmdlg
import orbsdlg
import menuseldlg
import menuseldlg2
import langsdlg
import htmlhelpframe
import math
import _thread
import wx.lib.newevent
PDReadyEvent, EVT_PDREADY = wx.lib.newevent.NewEvent()
pdlock = _thread.allocate_lock()

class MFrame(wx.Frame):
    XSIZE = 960
    YSIZE = 720
    MHOROSCOPE, MTABLES, MCHARTS, MOPTIONS, MHELP = list(range(0, 5))

    def __init__(self, parent, id, title, opts):
        wx.Frame.__init__(self, parent, id, i18n.tr(title), wx.DefaultPosition, wx.Size(MFrame.XSIZE, MFrame.YSIZE))
        self.fpath = ''
        self.fpathhors = 'Hors'
        self.fpathimgs = 'Images'
        self.title = title
        self.origtitle = title
        self.hortitle = title
        self.options = opts
        common.common = common.Common()
        self.CenterOnScreen()
        self.SetMinSize((200, 200))
        self.SetBackgroundColour(self.options.clrbackground)
        self.dirty = False
        self.buildMenus()
        self.statusbar = self.CreateStatusBar(4, name='status_line')
        self.statusbar.SetStatusWidths([-5, -2, -3, -4])
        self.buildToolBar()
        self.sidebar_width = tradoptions.get('sidebar_width')
        self._sidebar_last_draw = 0.0
        self.sidebar = sidebar.Sidebar(self, self.onSidebarResize)
        self.sidebar.Hide()
        if os.name == 'mac' or os.name == 'posix':
            self.Bind(wx.EVT_PAINT, self.onPaint)
        else:
            self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_CLOSE, self.onExit)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.splash = True
        self.enableMenus(False)
        self.moptions.Enable(self.ID_SaveOpts, False)
        if self.options.checkOptsFiles():
            self.moptions.Enable(self.ID_Reload, True)
        else:
            self.moptions.Enable(self.ID_Reload, False)
        self.trdatedlg = None
        self.trmondlg = None
        self.suntrdlg = None
        self.revdlg = None
        self.secdirdlg = None
        self.pdrangedlg = None
        os.environ['SE_EPHE_PATH'] = ''
        astrology.swe_set_ephe_path(common.common.ephepath)
        # returns stepped or listed outside Charts > Revolutions use the same sidereal correction
        returnslistframe.returnslist.sidereal_solar_correction = self.calcPrecNutCorrectedSolar
        self.drawSplash()
        self.clickedPlId = None
        self.Bind(EVT_PDREADY, self.OnPDReady)
        return

    def buildMenus(self):
        """File, View, Tables, Charts, Tools, Options, Help. The items of
        Morinus 6 keep their ids and are shown as chosen in Options > Menu
        selection (menusels, indexed by their original menus)."""
        sels = self.options.menusels
        menubar = wx.MenuBar()
        self.ID_New, self.ID_Data, self.ID_HereAndNow, self.ID_Load, self.ID_Save, self.ID_SaveAsBitmap, self.ID_Synastry, self.ID_FindTime, self.ID_Ephemeris, self.ID_Close, self.ID_Exit = list(range(100, 111))
        self.horbase = 100
        self.ID_Positions, self.ID_TAlmutens, self.ID_AlmutenZodiacal, self.ID_AlmutenChart, self.ID_AlmutenTopical, self.ID_Misc, self.ID_MunPos, self.ID_Antiscia, self.ID_Aspects, self.ID_Midpoints, self.ID_RiseSet, self.ID_Speeds, self.ID_ZodPars, self.ID_FixedStars, self.ID_FixedStarsAsps, self.ID_Lots, self.ID_Strip, self.ID_PlanetaryHours, self.ID_ExactTransits, self.ID_Profections, self.ID_UserSpeculum, self.ID_Firdaria, self.ID_PrimaryDirs = list(range(120, 143))
        self.tabbase = 120
        self.ID_Transits, self.ID_Revolutions, self.ID_SunTransits, self.ID_SecondaryDirs, self.ID_Elections, self.ID_SquareChart, self.ID_SyzygyChart, self.ID_SyzygyChart2, self.ID_ProfectionsChart, self.ID_HelioChart = list(range(150, 160))
        self.chartsbase = 150
        self.ID_Appearance1, self.ID_Appearance2, self.ID_Dignities, self.ID_MinorDignities, self.ID_Triplicities, self.ID_Terms, self.ID_Decans, self.ID_Almutens, self.ID_ChartAlmuten, self.ID_Topical, self.ID_Ayanamsha, self.ID_Colors, self.ID_HouseSystem, self.ID_Nodes, self.ID_Orbs, self.ID_PrimaryDirsOpt, self.ID_PrimaryKeys, self.ID_PDsInChartOpt, self.ID_LotsOpt, self.ID_Syzygy, self.ID_FixedStarsOpt, self.ID_ProfectionsOpt, self.ID_FirdariaOpt, self.ID_DefLocationOpt, self.ID_MenuSel, self.ID_MenuSelFirst, self.ID_MenuSelSecond, self.ID_Languages, self.ID_AutoSaveOpts, self.ID_SaveOpts, self.ID_Reload = list(range(170, 201))
        self.optsbase = 170
        self.ID_Help = 300
        self.ID_About = 301
        self.helpbase = 300

        def shown(iid):
            # the submenu items (almutens, minor dignities, menu selection) have no slot of their own
            if iid < 120:
                return sels[MFrame.MHOROSCOPE][iid - self.horbase]
            if iid < 150:
                return sels[MFrame.MTABLES][iid - self.tabbase - (0 if iid == self.ID_Positions else 1)]
            if iid < 170:
                return sels[MFrame.MCHARTS][iid - self.chartsbase]
            if iid < 300:
                skip = 0 if iid <= self.ID_Dignities else 1 if iid <= self.ID_Decans else 2 if iid <= self.ID_DefLocationOpt else 3
                return sels[MFrame.MOPTIONS][iid - self.optsbase - skip]
            return sels[MFrame.MHELP][iid - self.helpbase]

        def add(menu, iid, key, handler, doc=None):
            # an item of Morinus 6
            if shown(iid):
                menu.Append(iid, i18n.tr(mtexts.menutxts[key]), i18n.tr(mtexts.menutxts[doc or key + 'Doc']))
                self.Bind(wx.EVT_MENU, handler, id=iid)

        def new(menu, label, doc, handler, iid=None):
            # an added item, always shown
            item = menu.Append(iid if iid is not None else wx.NewIdRef(), i18n.tr(label), i18n.tr(doc))
            self.Bind(wx.EVT_MENU, handler, id=item.GetId())
            return item

        def sep(menu):
            n = menu.GetMenuItemCount()
            if n and not menu.FindItemByPosition(n - 1).IsSeparator():
                menu.AppendSeparator()

        def finish(menu, label):
            n = menu.GetMenuItemCount()
            if n and menu.FindItemByPosition(n - 1).IsSeparator():
                menu.Delete(menu.FindItemByPosition(n - 1))
            if menu.GetMenuItemCount():
                menubar.Append(menu, i18n.tr(label))

        # File
        self.mhoros = wx.Menu()
        add(self.mhoros, self.ID_New, 'HMNew', self.onNew)
        add(self.mhoros, self.ID_HereAndNow, 'HMHereAndNow', self.onHereAndNow)
        add(self.mhoros, self.ID_Load, 'HMLoad', self.onLoad)
        if shown(self.ID_Load):
            self.mrecent = wx.Menu()
            self.mhoros.AppendSubMenu(self.mrecent, i18n.tr('Recent charts'))
            self.filehistory = wx.FileHistory()
            self.filehistory.UseMenu(self.mrecent)
            self.Bind(wx.EVT_MENU_RANGE, self.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9)
        sep(self.mhoros)
        add(self.mhoros, self.ID_Save, 'HMSave', self.onSave)
        add(self.mhoros, self.ID_SaveAsBitmap, 'HMSaveAsBmp', self.onSaveAsBitmap)
        add(self.mhoros, self.ID_Data, 'HMData', self.onData)
        sep(self.mhoros)
        add(self.mhoros, self.ID_Close, 'HMClose', self.onClose)
        sep(self.mhoros)
        add(self.mhoros, self.ID_Exit, 'HMExit', self.onExit)
        finish(self.mhoros, 'File' if mtexts.menutxts['MHoroscope'].replace('&', '') == 'Horoscope' else mtexts.menutxts['MHoroscope'])

        # View: the switches of Options > Appearance I, the house system and the nodes
        self.mview = wx.Menu()
        self.viewchecks = {}
        for attr, label, doc in (('houses', 'House cusps', 'Draw the house cusps on the chart'), ('showterms', 'Terms', 'Show the ring of the terms'),
                                 ('showdecans', 'Decans', 'Show the ring of the decans'), ('showdata', 'Chart data', 'Write the data of the chart in its centre'),
                                 ('enableclick', 'Click a planet for its aspects', 'Clicking a planet draws only its aspects')):
            item = self.mview.AppendCheckItem(wx.NewIdRef(), i18n.tr(label), i18n.tr(doc))
            self.Bind(wx.EVT_MENU, lambda e, a=attr: self.onViewOption(a, e.IsChecked()), id=item.GetId())
            self.viewchecks[attr] = item
        self.mring = wx.Menu()
        self.ringitems = {}
        for value, label in ((chart.Chart.SHOWNONE, 'None'), (chart.Chart.SHOWFIXEDSTARS, 'Fixed stars'), (chart.Chart.SHOWANTIS, 'Antiscia'),
                             (chart.Chart.SHOWLOTS, 'Lots'), (chart.Chart.SHOWDODECATEMORIA, 'Dodecatemoria')):
            item = self.mring.AppendRadioItem(wx.NewIdRef(), i18n.tr(label), i18n.tr('Show this in the outer ring of the chart'))
            self.Bind(wx.EVT_MENU, lambda e, v=value: self.onViewOption('showobject', v), id=item.GetId())
            self.ringitems[value] = item
        self.mview.AppendSubMenu(self.mring, i18n.tr('Outer ring'))
        self.viewbw = self.mview.AppendCheckItem(wx.NewIdRef(), i18n.tr('Black and white'), i18n.tr('Draw the chart and the tables in black and white'))
        self.Bind(wx.EVT_MENU, lambda e: self.onViewOption('bw', e.IsChecked()), id=self.viewbw.GetId())
        self.viewsidebar = self.mview.AppendCheckItem(wx.NewIdRef(), i18n.tr('Planet sidebar'), i18n.tr('Show the planet, chart and time lords beside the chart'))
        self.viewsidebar.Check(tradoptions.get('show_sidebar'))
        self.Bind(wx.EVT_MENU, self.onViewSidebar, id=self.viewsidebar.GetId())
        self.viewtoolbar = self.mview.AppendCheckItem(wx.NewIdRef(), i18n.tr('Toolbar'), i18n.tr('Show the toolbar with the command search'))
        self.viewtoolbar.Check(tradoptions.get('show_toolbar'))
        self.Bind(wx.EVT_MENU, self.onViewToolBar, id=self.viewtoolbar.GetId())
        sep(self.mview)
        self.ID_Housesystem1, self.ID_Housesystem2, self.ID_Housesystem3, self.ID_Housesystem4, self.ID_Housesystem5, self.ID_Housesystem6, self.ID_Housesystem7, self.ID_Housesystem8, self.ID_Housesystem9, self.ID_Housesystem10, self.ID_Housesystem11, self.ID_Housesystem12 = list(range(1050, 1062))
        self.ID_NodeMean = 1070
        self.ID_NodeTrue = 1071
        self.hsbase = self.ID_Housesystem1
        self.nodebase = self.ID_NodeMean
        self.mhousesystem = wx.Menu()
        self.itplac = self.mhousesystem.Append(self.ID_Housesystem1, i18n.tr(mtexts.menutxts['OMHSPlacidus']), '', wx.ITEM_RADIO)
        self.itkoch = self.mhousesystem.Append(self.ID_Housesystem2, i18n.tr(mtexts.menutxts['OMHSKoch']), '', wx.ITEM_RADIO)
        self.itregio = self.mhousesystem.Append(self.ID_Housesystem3, i18n.tr(mtexts.menutxts['OMHSRegiomontanus']), '', wx.ITEM_RADIO)
        self.itcampa = self.mhousesystem.Append(self.ID_Housesystem4, i18n.tr(mtexts.menutxts['OMHSCampanus']), '', wx.ITEM_RADIO)
        self.itequal = self.mhousesystem.Append(self.ID_Housesystem5, i18n.tr(mtexts.menutxts['OMHSEqual']), '', wx.ITEM_RADIO)
        self.itwhole = self.mhousesystem.Append(self.ID_Housesystem6, i18n.tr(mtexts.menutxts['OMHSWholeSign']), '', wx.ITEM_RADIO)
        self.itaxial = self.mhousesystem.Append(self.ID_Housesystem7, i18n.tr(mtexts.menutxts['OMHSAxial']), '', wx.ITEM_RADIO)
        self.itmorin = self.mhousesystem.Append(self.ID_Housesystem8, i18n.tr(mtexts.menutxts['OMHSMorinus']), '', wx.ITEM_RADIO)
        self.ithoriz = self.mhousesystem.Append(self.ID_Housesystem9, i18n.tr(mtexts.menutxts['OMHSHorizontal']), '', wx.ITEM_RADIO)
        self.itpage = self.mhousesystem.Append(self.ID_Housesystem10, i18n.tr(mtexts.menutxts['OMHSPagePolich']), '', wx.ITEM_RADIO)
        self.italcab = self.mhousesystem.Append(self.ID_Housesystem11, i18n.tr(mtexts.menutxts['OMHSAlcabitus']), '', wx.ITEM_RADIO)
        self.itporph = self.mhousesystem.Append(self.ID_Housesystem12, i18n.tr(mtexts.menutxts['OMHSPorphyrius']), '', wx.ITEM_RADIO)
        if shown(self.ID_HouseSystem):
            self.mview.Append(wx.MenuItem(self.mview, self.ID_HouseSystem, mtexts.menutxts['OMHouseSystem'], subMenu=self.mhousesystem))
            self.setHouse()
            self.Bind(wx.EVT_MENU_RANGE, self.onHouseSystem, id=self.ID_Housesystem1, id2=self.ID_Housesystem12)
        self.mnodes = wx.Menu()
        self.meanitem = self.mnodes.Append(self.ID_NodeMean, i18n.tr(mtexts.menutxts['OMNMean']), '', wx.ITEM_RADIO)
        self.trueitem = self.mnodes.Append(self.ID_NodeTrue, i18n.tr(mtexts.menutxts['OMNTrue']), '', wx.ITEM_RADIO)
        if shown(self.ID_Nodes):
            self.mview.Append(wx.MenuItem(self.mview, self.ID_Nodes, mtexts.menutxts['OMNodes'], subMenu=self.mnodes))
            self.setNode()
            self.Bind(wx.EVT_MENU_RANGE, self.onNodes, id=self.ID_NodeMean, id2=self.ID_NodeTrue)
        sep(self.mview)
        new(self.mview, i18n.tr('Chart look...'), i18n.tr('Colour theme and line weight of the chart'), self.onChartLook)
        self.updateViewMenu()
        finish(self.mview, 'View')

        # Tables, grouped: positions; dignities; aspects and points; fixed stars; time lords; directions and transits; hours and visibility
        self.mtables = wx.Menu()
        self.ID_PositionsWorkspace = wx.NewIdRef()
        new(self.mtables, i18n.tr('Positions and data...\tCtrl+Shift+P'),
            i18n.tr('Browse zodiacal specula, mundane positions, motion and chart data in one window'),
            self.onPositionsWorkspace, self.ID_PositionsWorkspace)
        sep(self.mtables)
        add(self.mtables, self.ID_ZodPars, 'TMZodPars', self.onZodPars)
        add(self.mtables, self.ID_Midpoints, 'TMMidpoints', self.onMidpoints)
        add(self.mtables, self.ID_Strip, 'TMStrip', self.onStrip)
        sep(self.mtables)
        if shown(self.ID_AlmutenZodiacal) or shown(self.ID_AlmutenChart) or shown(self.ID_AlmutenTopical):
            self.talmutens = wx.Menu()
            self.mtables.Append(wx.MenuItem(self.mtables, self.ID_TAlmutens, mtexts.menutxts['TMAlmutens'], subMenu=self.talmutens))
            add(self.talmutens, self.ID_AlmutenZodiacal, 'TMAlmutenZodiacal', self.onAlmutenZodiacal)
            add(self.talmutens, self.ID_AlmutenChart, 'TMAlmutenChart', self.onAlmutenChart)
            add(self.talmutens, self.ID_AlmutenTopical, 'TMAlmutenTopical', self.onAlmutenTopical)
        self.ID_TradConditions, self.ID_TradTemperament, self.ID_ZRFortune, self.ID_ZRSpirit, self.ID_Decennials = 143, 145, 146, 147, 148
        new(self.mtables, i18n.tr('Planetary conditions'), i18n.tr('Sect, hayz, synodic phase, stations, joys, latitude, Via Combusta, void of course'), self.onConditions, self.ID_TradConditions)
        new(self.mtables, i18n.tr('Temperament'), i18n.tr('Temperament worksheet'), self.onTemperament, self.ID_TradTemperament)
        sep(self.mtables)
        add(self.mtables, self.ID_Aspects, 'TMAspects', self.onAspects)
        add(self.mtables, self.ID_Antiscia, 'TMAntiscia', self.onAntiscia)
        add(self.mtables, self.ID_Lots, 'TMLots', self.onLots)
        sep(self.mtables)
        self.ID_FixedStarsWorkspace = new(self.mtables, i18n.tr('Fixed Stars...'),
            i18n.tr('Catalogue, conjunctions and aspects, birth angles and paranatellonta'),
            self.onFixedStarsWorkspace).GetId()
        sep(self.mtables)
        add(self.mtables, self.ID_Profections, 'TMProfections', self.onProfections)
        add(self.mtables, self.ID_Firdaria, 'TMFirdaria', self.onFirdaria)
        # the time lords of the Hellenistic astrologers in a submenu
        self.mhellenistic = wx.Menu()
        new(self.mhellenistic, i18n.tr('Zodiacal releasing from Fortune'), i18n.tr('Periods of the signs from the Lot of Fortune (Valens)'), self.onZRFortune, self.ID_ZRFortune)
        new(self.mhellenistic, i18n.tr('Zodiacal releasing from Spirit'), i18n.tr('Periods of the signs from the Lot of Spirit (Valens)'), self.onZRSpirit, self.ID_ZRSpirit)
        new(self.mhellenistic, i18n.tr('Decennials'), i18n.tr('Periods of 10 years 9 months of the planets (Valens)'), self.onDecennials, self.ID_Decennials)
        self.ID_Circumambulation = new(self.mhellenistic, i18n.tr('Circumambulation'), i18n.tr('The Ascendant directed through the bounds (Ptolemy)'), self.onCircumambulation).GetId()
        self.mtables.AppendSubMenu(self.mhellenistic, i18n.tr('Hellenistic'), i18n.tr('Zodiacal releasing, decennials and circumambulation'))
        sep(self.mtables)
        add(self.mtables, self.ID_PrimaryDirs, 'TMPrimaryDirs', self.onPrimaryDirs)
        sep(self.mtables)
        self.ID_HoursRiseSetWorkspace = new(self.mtables, i18n.tr('Planetary hours and rise/set...'),
            i18n.tr('Planetary hours, daylight boundaries, rise/set and culmination times'),
            self.onHoursRiseSetWorkspace).GetId()
        sep(self.mtables)
        self.ID_Heliacal = new(self.mtables, i18n.tr('Heliacal phenomena and phasis'), i18n.tr('Visibility of the planets and stations around the birth'), self.onHeliacal).GetId()
        finish(self.mtables, mtexts.menutxts['MTable'])

        # Charts: returns (Solar and Lunar, the others grouped); transits and progressions; lunations; other charts
        self.mcharts = wx.Menu()
        self.ID_ReturnsList = 160
        self.returnids = []
        if shown(self.ID_Revolutions):
            self.mcharts.Append(self.ID_Revolutions, i18n.tr('Solar return...\tCtrl+Shift+F2'), i18n.tr('The return of the Sun to its place in the chart'))
            self.Bind(wx.EVT_MENU, lambda e: self.onRevolutions(e, revolutions.Revolutions.SUN), id=self.ID_Revolutions)
            self.returnids.append(new(self.mcharts, i18n.tr('Lunar return...'), i18n.tr('The return of the Moon to its place in the chart'), lambda e: self.onRevolutions(e, revolutions.Revolutions.MOON)).GetId())
        new(self.mcharts, i18n.tr('Lunar returns of the year...'), i18n.tr('Lunar returns covering a solar year'), self.onReturnsList, self.ID_ReturnsList)
        if shown(self.ID_Revolutions):
            mreturns = wx.Menu()
            for pl, key in ((revolutions.Revolutions.MERCURY, 'Mercury'), (revolutions.Revolutions.VENUS, 'Venus'), (revolutions.Revolutions.MARS, 'Mars'),
                            (revolutions.Revolutions.JUPITER, 'Jupiter'), (revolutions.Revolutions.SATURN, 'Saturn')):
                self.returnids.append(new(mreturns, key + ' return...', 'The return of ' + key + ' to its place in the chart', lambda e, pl=pl: self.onRevolutions(e, pl)).GetId())
            self.ID_OtherReturns = wx.NewIdRef()
            self.mcharts.Append(wx.MenuItem(self.mcharts, self.ID_OtherReturns, 'Other planetary returns', subMenu=mreturns))
            self.returnids.append(self.ID_OtherReturns)
        sep(self.mcharts)
        add(self.mcharts, self.ID_Transits, 'PMTransits', self.onTransits)
        self.ID_CompareGrid = new(self.mcharts, i18n.tr('Compare charts...'), i18n.tr('Show 2 or 4 independent chart wheels'), self.onCompareGrid).GetId()
        self.ID_MultiWheel = new(self.mcharts, i18n.tr('Multi-wheel...'), i18n.tr('Show radix with up to three chart rings'), self.onMultiWheel).GetId()
        # Exact transits (Tables) and Sun transits are one search
        self.ID_TransitSearch = new(self.mcharts, i18n.tr('Transit search...'), i18n.tr('Exact transits over months or years, by planet, aspect and natal point'),
                                    self.onTransitSearch).GetId()
        add(self.mcharts, self.ID_SecondaryDirs, 'PMSecondaryDirs', self.onSecondaryDirs)
        add(self.mcharts, self.ID_ProfectionsChart, 'PMProfections', self.onProfectionsChart)
        sep(self.mcharts)
        self.ID_LunationNavigator = new(self.mcharts, i18n.tr('Syzygies and lunar phases...'),
            i18n.tr('Browse lunations without changing the prenatal syzygy'),
            self.onLunationNavigator).GetId()
        sep(self.mcharts)
        add(self.mcharts, self.ID_Elections, 'PMElections', self.onElections)
        add(self.mcharts, self.ID_SquareChart, 'PMSquareChart', self.onSquareChart)
        add(self.mcharts, self.ID_HelioChart, 'PMHelioChart', self.onHelioChart)
        finish(self.mcharts, mtexts.menutxts['MCharts'])

        # Tools
        self.mtools = wx.Menu()
        add(self.mtools, self.ID_FindTime, 'HMFindTime', self.onFindTime)
        add(self.mtools, self.ID_Synastry, 'HMSynastry', self.onSynastry)
        add(self.mtools, self.ID_Ephemeris, 'HMEphemeris', self.onEphemeris)
        self.ID_DodecaCalc = new(self.mtools, i18n.tr('Dodecatemoria calculator...'), i18n.tr('The dodecatemorion of any degree'), self.onDodecaCalc).GetId()
        finish(self.mtools, 'Tools')

        # Settings: the Settings window (settingswnd), the language and saving; the dialogs
        # of Morinus 6 open from the Settings window and keep their shortcuts
        self.moptions = wx.Menu()
        self.settingswnd = None
        new(self.moptions, i18n.tr('Settings...\tCtrl+,'), i18n.tr('All the settings, by category'), self.onSettings)
        add(self.moptions, self.ID_Languages, 'OMLanguages', self.onLanguages)
        sep(self.moptions)
        if shown(self.ID_AutoSaveOpts):
            self.autosave = self.moptions.Append(self.ID_AutoSaveOpts, i18n.tr(mtexts.menutxts['OMAutoSave']), i18n.tr(mtexts.menutxts['OMAutoSaveDoc']), wx.ITEM_CHECK)
            self.setAutoSave()
            self.Bind(wx.EVT_MENU, self.onAutoSaveOpts, id=self.ID_AutoSaveOpts)
        add(self.moptions, self.ID_SaveOpts, 'OMSave', self.onSaveOpts)
        add(self.moptions, self.ID_Reload, 'OMReload', self.onReload)
        finish(self.moptions, 'Settings' if mtexts.menutxts['MOptions'].replace('&', '') == 'Options' else mtexts.menutxts['MOptions'])
        accels = []
        for iid, key, handler in ((self.ID_Appearance1, 'OMAppearance1', self.onAppearance1), (self.ID_Appearance2, 'OMAppearance2', self.onAppearance2),
                                  (self.ID_Colors, 'OMColors', self.onColors), (self.ID_Dignities, 'OMDignities', self.onDignities),
                                  (self.ID_Triplicities, 'OMTriplicities', self.onTriplicities), (self.ID_Terms, 'OMTerms', self.onTerms),
                                  (self.ID_Decans, 'OMDecans', self.onDecans), (self.ID_ChartAlmuten, 'OMChartAlmuten', self.onChartAlmuten),
                                  (self.ID_Topical, 'OMTopical', self.onTopicals), (self.ID_Ayanamsha, 'OMAyanamsha', self.onAyanamsha),
                                  (self.ID_Orbs, 'OMOrbs', self.onOrbs), (self.ID_PrimaryDirsOpt, 'OMPrimaryDirs', self.onPrimaryDirsOpt),
                                  (self.ID_PrimaryKeys, 'OMPrimaryKeys', self.onPrimaryKeys), (self.ID_PDsInChartOpt, 'OMPDsInChartOpt', self.onPDsInChartOpt),
                                  (self.ID_LotsOpt, 'OMLots', self.onLotsOpt), (self.ID_Syzygy, 'OMSyzygy', self.onSyzygy),
                                  (self.ID_FixedStarsOpt, 'OMFixedStarsOpt', self.onFixedStarsOpt), (self.ID_ProfectionsOpt, 'OMProfectionsOpt', self.onProfectionsOpt),
                                  (self.ID_FirdariaOpt, 'OMFirdariaOpt', self.onFirdariaOpt), (self.ID_DefLocationOpt, 'OMDefLocationOpt', self.onDefLocationOpt),
                                  (self.ID_MenuSelFirst, 'OMMenuSelFirst', self.onMenuSelFirst), (self.ID_MenuSelSecond, 'OMMenuSelSecond', self.onMenuSelSecond)):
            self.Bind(wx.EVT_MENU, handler, id=iid)
            keys = mtexts.menutxts[key].partition('\t')[2]
            entry = wx.AcceleratorEntry()
            if shown(iid) and keys and entry.FromString(keys):
                entry.Set(entry.GetFlags(), entry.GetKeyCode(), iid)
                accels.append(entry)
        # The shortcuts of Morinus's own tables and charts that became tabs of the
        # workspaces (their menu items were removed): F1, F5, F6, F10, F11,
        # Ctrl+F1, Ctrl+F2, Ctrl+F5, Ctrl+Shift+F7 and Ctrl+Shift+F8.
        for iid, key, handler in ((self.ID_Positions, 'TMPositions', self.onPositions), (self.ID_Misc, 'TMMisc', self.onMisc),
                                  (self.ID_MunPos, 'TMMunPos', self.onMunPos), (self.ID_RiseSet, 'TMRiseSet', self.onRiseSet),
                                  (self.ID_Speeds, 'TMSpeeds', self.onSpeeds), (self.ID_FixedStars, 'TMFixStars', self.onFixedStars),
                                  (self.ID_FixedStarsAsps, 'TMFixStarsAsps', self.onFixedStarsAsps), (self.ID_PlanetaryHours, 'TMPlanetaryHours', self.onPlanetaryHours),
                                  (self.ID_SyzygyChart, 'PMSyzygy', self.onSyzygyChart), (self.ID_SyzygyChart2, 'PMSyzygy2', self.onSyzygyChart2),
                                  (self.ID_ExactTransits, 'TMExactTransits', self.onTransitSearch), (self.ID_SunTransits, 'PMSunTransits', self.onSunTransitSearch),
                                  (self.ID_UserSpeculum, 'TMUserSpeculum', lambda e: self.showPositionsWorkspace(positionscatalog.MENU_TABS['onUserSpeculum']))):
            self.Bind(wx.EVT_MENU, lambda e, h=handler: None if self.splash else h(e), id=iid)
            keys = mtexts.menutxts[key].partition('\t')[2]
            entry = wx.AcceleratorEntry()
            if keys and entry.FromString(keys):
                entry.Set(entry.GetFlags(), entry.GetKeyCode(), iid)
                accels.append(entry)
        # Ctrl+K opens the same command palette whether or not the toolbar is shown.
        self.ID_CommandSearch = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onCommandSearch, id=self.ID_CommandSearch)
        accels.append(wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('K'), self.ID_CommandSearch))
        self.SetAcceleratorTable(wx.AcceleratorTable(accels))

        # Help
        self.mhelp = wx.Menu()
        add(self.mhelp, self.ID_Help, 'HEMHelp', self.onHelp)
        add(self.mhelp, self.ID_About, 'HEMAbout', self.onAbout)
        finish(self.mhelp, mtexts.menutxts['MHelp'])
        self.SetMenuBar(menubar)

    def buildToolBar(self):
        """New, Open, Save, Chart data, Settings, the house system and the command search."""
        tb = self.toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.TB_FLAT)
        menubar = self.GetMenuBar()
        art = lambda a: wx.ArtProvider.GetBitmap(a, wx.ART_TOOLBAR, (22, 22))
        self.toolids = []
        for iid, artid, key in ((self.ID_New, wx.ART_NEW, 'HMNew'), (self.ID_Load, wx.ART_FILE_OPEN, 'HMLoad'),
                                (self.ID_Save, wx.ART_FILE_SAVE, 'HMSave'), (self.ID_Data, wx.ART_EDIT, 'HMData')):
            if menubar.FindItemById(iid):
                text, _, keys = mtexts.menutxts[key].partition('\t')
                text = text.replace('&', '')
                tb.AddTool(iid, i18n.tr(text), art(artid), shortHelp=text + (' (' + keys + ')' if keys else ''))
                self.toolids.append(iid)
        icon = wx.ArtProvider.GetBitmap('preferences-system', wx.ART_TOOLBAR, (22, 22))	# the desktop's icon where there is one
        tool = tb.AddTool(wx.ID_ANY, i18n.tr('Settings'), icon if icon.IsOk() else art(wx.ART_HELP_SETTINGS), shortHelp=i18n.tr('Settings (Ctrl+,)'))
        self.Bind(wx.EVT_TOOL, self.onSettings, id=tool.GetId())
        self.ID_SidebarTool = wx.NewIdRef()
        tb.AddCheckTool(self.ID_SidebarTool, i18n.tr('Planet sidebar'), art(wx.ART_REPORT_VIEW), shortHelp=i18n.tr('Planet sidebar'))
        tb.ToggleTool(self.ID_SidebarTool, tradoptions.get('show_sidebar'))
        self.Bind(wx.EVT_TOOL, self.onViewSidebar, id=self.ID_SidebarTool)
        tb.AddSeparator()
        tb.AddControl(wx.StaticText(tb, -1, i18n.tr(' Houses: ')))
        self.tbhouses = wx.Choice(tb, -1, choices=[mtexts.menutxts[k].partition('\t')[0].replace('&', '') for k in settingswnd.HOUSESYSTEMS])
        self.tbhouses.SetToolTip(i18n.tr('House system (View > House system)'))
        self.tbhouses.SetSelection(self.options.hsys)
        self.tbhouses.Bind(wx.EVT_CHOICE, self.onToolHouse)
        tb.AddControl(self.tbhouses)
        tb.AddStretchableSpace()
        self.command_button = wx.Button(tb, -1, i18n.tr('Find command...  Ctrl+K'))
        self.command_button.SetToolTip(i18n.tr('Search menus and settings by name or description (Ctrl+K)'))
        self.command_button.Bind(wx.EVT_BUTTON, self.onCommandSearch)
        tb.AddControl(self.command_button)
        tb.Realize()
        tb.Show(tradoptions.get('show_toolbar'))

    def onCommandSearch(self, event):
        """Use one searchable palette regardless of toolbar visibility."""
        commandsearch.show(self)

    def onToolHouse(self, event):
        self.onHouseSystem(wx.CommandEvent(wx.wxEVT_MENU, self.hsbase + self.tbhouses.GetSelection()))
        self.setHouse()

    def onViewToolBar(self, event):
        tradoptions.set({'show_toolbar': self.viewtoolbar.IsChecked()})
        if self.options.autosave:
            tradoptions.save()
        self.toolbar.Show(self.viewtoolbar.IsChecked())
        self.SendSizeEvent()

    def updateViewMenu(self):
        """The View menu's switches as the options are."""
        for attr, item in self.viewchecks.items():
            item.Check(getattr(self.options, attr))
        if self.options.showobject in self.ringitems:
            self.ringitems[self.options.showobject].Check(True)
        self.viewbw.Check(self.options.bw)

    def onViewOption(self, attr, value):
        """A switch of the View menu: an option of Appearance I."""
        setattr(self.options, attr, value)
        self.updateViewMenu()
        self.enableOptMenus(True)
        if self.options.autosave:
            if self.options.saveAppearance1():
                self.moptions.Enable(self.ID_SaveOpts, False)
        if not self.splash:
            self.closeChildWnds()
            self.clickedPlId = None
            self.drawBkg()
            self.Refresh()

    def onNew(self, event):
        dlg = datadlg.DataDlg(self, self.options.langid, self.options.netbook)
        dlg.CenterOnParent()
        dlg.initialize()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            self.dirty = True
            direc = dlg.placerbE.GetValue()
            hemis = dlg.placerbN.GetValue()
            place = chart.Place(dlg.birthplace.GetValue(), int(dlg.londeg.GetValue()), int(dlg.lonmin.GetValue()), 0, direc, int(dlg.latdeg.GetValue()), int(dlg.latmin.GetValue()), 0, hemis, int(dlg.alt.GetValue()))
            plus = True
            if dlg.pluscb.GetCurrentSelection() == 1:
                plus = False
            time = chart.Time(int(dlg.year.GetValue()), int(dlg.month.GetValue()), int(dlg.day.GetValue()), int(dlg.hour.GetValue()), int(dlg.minute.GetValue()), int(dlg.sec.GetValue()), dlg.timeckb.GetValue(), dlg.calcb.GetCurrentSelection(), dlg.zonecb.GetCurrentSelection(), plus, int(dlg.zhour.GetValue()), int(dlg.zminute.GetValue()), dlg.daylightckb.GetValue(), place)
            male = dlg.genderrbM.GetValue()
            self.horoscope = chart.Chart(dlg.name.GetValue(), male, time, place, dlg.typecb.GetCurrentSelection(), dlg.notes.GetValue(), self.options)
            self.splash = False
            self.enableMenus(True)
            self.clickedPlId = None
            self.drawBkg()
            self.Refresh()
            self.handleCaption(True)
            self.destroyDlgs()
        dlg.Destroy()
        return

    def onData(self, event):
        dlg = datadlg.DataDlg(self, self.options.langid, self.options.netbook)
        dlg.CenterOnParent()
        dlg.fill(self.horoscope)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            changed = dlg.check(self.horoscope)
            if self.dirty and changed:
                dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtsfiles['DiscardCurrHor']), '', wx.YES_NO | wx.ICON_QUESTION)
                if dlgm.ShowModal() == wx.ID_NO:
                    self.save()
                dlgm.Destroy()
            if changed:
                self.dirty = True
            direc = dlg.placerbE.GetValue()
            hemis = dlg.placerbN.GetValue()
            place = chart.Place(dlg.birthplace.GetValue(), int(dlg.londeg.GetValue()), int(dlg.lonmin.GetValue()), 0, direc, int(dlg.latdeg.GetValue()), int(dlg.latmin.GetValue()), 0, hemis, int(dlg.alt.GetValue()))
            plus = True
            if dlg.pluscb.GetCurrentSelection() == 1:
                plus = False
            time = chart.Time(int(dlg.year.GetValue()), int(dlg.month.GetValue()), int(dlg.day.GetValue()), int(dlg.hour.GetValue()), int(dlg.minute.GetValue()), int(dlg.sec.GetValue()), dlg.timeckb.GetValue(), dlg.calcb.GetCurrentSelection(), dlg.zonecb.GetCurrentSelection(), plus, int(dlg.zhour.GetValue()), int(dlg.zminute.GetValue()), dlg.daylightckb.GetValue(), place)
            male = dlg.genderrbM.GetValue()
            self.horoscope = chart.Chart(dlg.name.GetValue(), male, time, place, dlg.typecb.GetCurrentSelection(), dlg.notes.GetValue(), self.options)
            self.splash = False
            self.enableMenus(True)
            self.clickedPlId = None
            self.drawBkg()
            self.Refresh()
            self.handleCaption(True)
            if changed:
                self.closeChildWnds()
                self.destroyDlgs()
        dlg.Destroy()
        return

    def onHereAndNow(self, event):
        self.dirty = True
        place = chart.Place(self.options.deflocname, self.options.defloclondeg, self.options.defloclonmin, 0, self.options.defloceast, self.options.defloclatdeg, self.options.defloclatmin, 0, self.options.deflocnorth, self.options.deflocalt)
        now = datetime.datetime.now()
        time = chart.Time(now.year, now.month, now.day, now.hour, now.minute, now.second, False, chart.Time.GREGORIAN, chart.Time.ZONE, self.options.deflocplus, self.options.defloczhour, self.options.defloczminute, self.options.deflocdst, place)
        self.horoscope = chart.Chart(mtexts.txtsdeflocdlgopts['HereAndNow'], True, time, place, chart.Chart.HORARY, '', self.options)
        self.splash = False
        self.enableMenus(True)
        self.clickedPlId = None
        self.drawBkg()
        self.Refresh()
        self.handleCaption(True)
        return

    def showFindTime(self, bc, fnd, arplac):
        place = chart.Place('London, GBR', 0, 6, 0, False, 51, 31, 0, True, 10)
        h, m, s = util.decToDeg(fnd[3])
        time = chart.Time(fnd[0], fnd[1], fnd[2], h, m, s, bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, place)
        d = astrology.swe_deltat(time.jd)
        rflag, obl, serr = astrology.swe_calc(time.jd + d, astrology.SE_ECL_NUT, 0)
        if arplac[2]:
            timeMidnight = chart.Time(time.year, time.month, time.day, 0, 0, 0, bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, place)
            place = self.calcPlace(time.time, timeMidnight.sidTime, arplac[0], arplac[1], obl[0])
        self.horoscope = chart.Chart('Search', True, time, place, chart.Chart.RADIX, '', self.options)
        if not self.splash:
            self.destroyDlgs()
            self.closeChildWnds()
        self.dirty = True
        self.splash = False
        self.fpath = ''
        self.enableMenus(True)
        self.clickedPlId = None
        self.drawBkg()
        self.Refresh()
        self.handleCaption(True)
        return

    def calcPlace(self, gmt, gmst0, mclon, asclon, obl):
        robl = math.radians(obl)
        deltaGMST = gmt * 1.00273790927949
        gmstNat = util.normalizeTime(gmst0 + deltaGMST)
        ramc = 0.0
        if mclon == 90.0:
            ramc = 90.0
        elif mclon == 270.0:
            ramc = 270.0
        else:
            rmclon = math.radians(mclon)
            X = math.degrees(math.atan(math.tan(rmclon) * math.cos(robl)))
            if mclon >= 0.0 and mclon < 90.0:
                ramc = X
            elif mclon > 90.0 and mclon < 270.0:
                ramc = X + 180.0
            elif mclon > 270.0 and mclon < 360.0:
                ramc = X + 360.0
        lmstNat = ramc / 15.0
        lonInTime = gmstNat - lmstNat
        if not (-12.0 <= lonInTime and lonInTime <= 12.0):
            if lonInTime < -12.0:
                lonInTime += 24.0
            elif lonInTime > 12.0:
                lonInTime -= 24.0
        lon = 0.0
        east = False
        if lonInTime == 0.0:
            lon = 0.0
        elif 0.0 < lonInTime and lonInTime <= 12.0:
            lon = lonInTime * 15.0
        elif -12.0 <= lonInTime and lonInTime < 0.0:
            lon = lonInTime * 15.0
            east = True
        rasclon = math.radians(asclon)
        rramc = math.radians(ramc)
        lat = 30.0
        north = True
        if math.sin(robl) != 0.0:
            lat = math.degrees(math.atan(-(math.cos(rramc) * (1 / math.tan(rasclon)) + math.sin(rramc) * math.cos(robl)) / math.sin(robl)))
            if lat < 0.0:
                north = False
        lon = math.fabs(lon)
        lat = math.fabs(lat)
        ld, lm, ls = util.decToDeg(lon)
        lad, lam, las = util.decToDeg(lat)
        return chart.Place('Place', ld, lm, ls, east, lad, lam, las, north, 10)

    def onLoad(self, event):
        if self.dirty:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtsfiles['DiscardCurrHor']), '', wx.YES_NO | wx.ICON_QUESTION)
            if dlgm.ShowModal() == wx.ID_NO:
                dlgm.Destroy()
                return
            dlgm.Destroy()
        dlg = wx.FileDialog(self, i18n.tr(mtexts.txtsfiles['OpenHor']), '', '', mtexts.txtsfiles['HORFiles'], wx.FD_OPEN)
        if os.path.isdir(self.fpathhors):
            dlg.SetDirectory(self.fpathhors)
        else:
            dlg.SetDirectory('.')
        if dlg.ShowModal() == wx.ID_OK:
            dpath = dlg.GetDirectory()
            fpath = dlg.GetPath()
            if not fpath.endswith('.hor'):
                fpath += '.hor'
            chrt = self.subLoad(fpath, dpath)
            if chrt != None:
                self.horoscope = chrt
                self.splash = False
                self.clickedPlId = None
                self.drawBkg()
                self.Refresh()
                self.fpathhors = dpath
                self.fpath = fpath
                self.enableMenus(True)
                self.handleCaption(True)
                self.dirty = False
                self.filehistory.AddFileToHistory(fpath)
                self.destroyDlgs()
        dlg.Destroy()
        return

    def subLoad(self, fpath, dpath, dontclose=False):
        chrt = None
        try:
            f = open(fpath, 'rb')
            name = pickle.load(f, encoding='utf-8')
            male = pickle.load(f, encoding='utf-8')
            htype = pickle.load(f, encoding='utf-8')
            bc = pickle.load(f, encoding='utf-8')
            year = pickle.load(f, encoding='utf-8')
            month = pickle.load(f, encoding='utf-8')
            day = pickle.load(f, encoding='utf-8')
            hour = pickle.load(f, encoding='utf-8')
            minute = pickle.load(f, encoding='utf-8')
            second = pickle.load(f, encoding='utf-8')
            cal = pickle.load(f, encoding='utf-8')
            zt = pickle.load(f, encoding='utf-8')
            plus = pickle.load(f, encoding='utf-8')
            zh = pickle.load(f, encoding='utf-8')
            zm = pickle.load(f, encoding='utf-8')
            daylightsaving = pickle.load(f, encoding='utf-8')
            placename = pickle.load(f, encoding='utf-8')
            deglon = pickle.load(f, encoding='utf-8')
            minlon = pickle.load(f, encoding='utf-8')
            seclon = pickle.load(f, encoding='utf-8')
            east = pickle.load(f, encoding='utf-8')
            deglat = pickle.load(f, encoding='utf-8')
            minlat = pickle.load(f, encoding='utf-8')
            seclat = pickle.load(f, encoding='utf-8')
            north = pickle.load(f, encoding='utf-8')
            altitude = pickle.load(f, encoding='utf-8')
            notes = pickle.load(f, encoding='utf-8')
            f.close()
            if not self.splash and not dontclose:
                self.closeChildWnds()
            place = chart.Place(placename, deglon, minlon, 0, east, deglat, minlat, seclat, north, altitude)
            time = chart.Time(year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, daylightsaving, place)
            chrt = chart.Chart(name, male, time, place, htype, notes, self.options)
        except IOError:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtsfiles['FileError']), i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlgm.ShowModal()
            dlgm.Destroy()

        return chrt

    def onSave(self, event):
        self.save()

    def save(self):
        dlg = wx.FileDialog(self, i18n.tr(mtexts.txtsfiles['SaveHor']), '', self.horoscope.name, mtexts.txtsfiles['HORFiles'], wx.FD_SAVE)
        if os.path.isdir(self.fpathhors):
            dlg.SetDirectory(self.fpathhors)
        else:
            dlg.SetDirectory('.')
        if dlg.ShowModal() == wx.ID_OK:
            dpath = dlg.GetDirectory()
            fpath = dlg.GetPath()
            if not fpath.endswith('.hor'):
                fpath += '.hor'
            if os.path.isfile(fpath):
                dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtsfiles['FileExists']), i18n.tr(mtexts.txtsfiles['Message']), wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                if dlgm.ShowModal() == wx.ID_NO:
                    dlgm.Destroy()
                    return
                dlgm.Destroy()
            try:
                f = open(fpath, 'wb')
                pickle.dump(self.horoscope.name, f, 2)
                pickle.dump(self.horoscope.male, f, 2)
                pickle.dump(self.horoscope.htype, f, 2)
                pickle.dump(self.horoscope.time.bc, f, 2)
                pickle.dump(self.horoscope.time.origyear, f, 2)
                pickle.dump(self.horoscope.time.origmonth, f, 2)
                pickle.dump(self.horoscope.time.origday, f, 2)
                pickle.dump(self.horoscope.time.hour, f, 2)
                pickle.dump(self.horoscope.time.minute, f, 2)
                pickle.dump(self.horoscope.time.second, f, 2)
                pickle.dump(self.horoscope.time.cal, f, 2)
                pickle.dump(self.horoscope.time.zt, f, 2)
                pickle.dump(self.horoscope.time.plus, f, 2)
                pickle.dump(self.horoscope.time.zh, f, 2)
                pickle.dump(self.horoscope.time.zm, f, 2)
                pickle.dump(self.horoscope.time.daylightsaving, f, 2)
                pickle.dump(self.horoscope.place.placename, f, 2)
                pickle.dump(self.horoscope.place.deglon, f, 2)
                pickle.dump(self.horoscope.place.minlon, f, 2)
                pickle.dump(self.horoscope.place.seclon, f, 2)
                pickle.dump(self.horoscope.place.east, f, 2)
                pickle.dump(self.horoscope.place.deglat, f, 2)
                pickle.dump(self.horoscope.place.minlat, f, 2)
                pickle.dump(self.horoscope.place.seclat, f, 2)
                pickle.dump(self.horoscope.place.north, f, 2)
                pickle.dump(self.horoscope.place.altitude, f, 2)
                pickle.dump(self.horoscope.notes, f, 2)
                self.fpathhors = dpath
                self.fpath = fpath
                self.handleCaption(True)
                f.close()
                self.dirty = False
            except IOError:
                dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtsfiles['FileError']), i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
                dlgm.ShowModal()
                dlgm.Destroy()

        dlg.Destroy()

    def onSaveAsBitmap(self, event):
        name = self.horoscope.name
        if name == '':
            name = mtexts.txtscommon['Horoscope']
        dlg = wx.FileDialog(self, i18n.tr(mtexts.txtsfiles['SaveAsBmp']), '', name, mtexts.txtsfiles['BMPFiles'], wx.FD_SAVE)
        if os.path.isdir(self.fpathimgs):
            dlg.SetDirectory(self.fpathimgs)
        else:
            dlg.SetDirectory('.')
        if dlg.ShowModal() == wx.ID_OK:
            dpath = dlg.GetDirectory()
            fpath = dlg.GetPath()
            if not fpath.endswith('.png'):
                fpath += '.png'
            if os.path.isfile(fpath):
                dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtsfiles['FileExists']), i18n.tr(mtexts.txtsfiles['Message']), wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                if dlgm.ShowModal() == wx.ID_NO:
                    dlgm.Destroy()
                    return
                dlgm.Destroy()
            self.buffer.SaveFile(fpath, wx.BITMAP_TYPE_PNG)
            self.fpathimgs = dpath
        dlg.Destroy()

    def onSynastry(self, event):
        dlg = wx.FileDialog(self, i18n.tr(mtexts.txtsfiles['OpenHor']), '', '', mtexts.txtsfiles['HORFiles'], wx.FD_OPEN)
        if os.path.isdir(self.fpathhors):
            dlg.SetDirectory(self.fpathhors)
        else:
            dlg.SetDirectory('.')
        chrt = None
        if dlg.ShowModal() == wx.ID_OK:
            dpath = dlg.GetDirectory()
            fpath = dlg.GetPath()
            if not fpath.endswith('.hor'):
                fpath += '.hor'
            chrt = self.subLoad(fpath, dpath, True)
        dlg.Destroy()
        if chrt != None:
            tw = transitframe.TransitFrame(self, self.title, chrt, self.horoscope, self.options, transitframe.TransitFrame.COMPOUND)
            tw.Show(True)
        return

    def onFindTime(self, event):
        findtimdlg = findtimedlg.FindTimeDlg(self)
        findtimdlg.fill()
        findtimdlg.CenterOnParent()
        findtimdlg.Show()

    def onEphemeris(self, event):
        """Coordinated graphical, daily, and station/ingress ephemeris."""
        ephemerisworkspace.show(self)

    def onClose(self, event):
        if self.dirty:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtsfiles['DiscardCurrHor']), '', wx.YES_NO | wx.ICON_QUESTION)
            if dlgm.ShowModal() == wx.ID_NO:
                dlgm.Destroy()
                return
            dlgm.Destroy()
        self.destroyDlgs()
        self.fpath = ''
        self.dirty = False
        self.splash = True
        self.enableMenus(False)
        self.closeChildWnds()
        self.drawSplash()
        self.handleCaption(False)
        self.Refresh()

    def onExit(self, event):
        if self.dirty:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtsfiles['DiscardCurrHor']), '', wx.YES_NO | wx.ICON_QUESTION)
            if dlgm.ShowModal() == wx.ID_NO:
                dlgm.Destroy()
                return
            dlgm.Destroy()
        self.destroyDlgs()
        self.Destroy()

    def OnFileHistory(self, evt):
        if self.dirty:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtsfiles['DiscardCurrHor']), '', wx.YES_NO | wx.ICON_QUESTION)
            if dlgm.ShowModal() == wx.ID_NO:
                dlgm.Destroy()
                return
            dlgm.Destroy()
        fileNum = evt.GetId() - wx.ID_FILE1
        path = self.filehistory.GetHistoryFile(fileNum)
        if os.path.exists(path):
            dname = os.path.dirname(path)
            chrt = self.subLoad(path, dname)
            if chrt != None:
                self.horoscope = chrt
                self.splash = False
                self.clickedPlId = None
                self.drawBkg()
                self.Refresh()
                self.fpathhors = dname
                self.fpath = path
                self.enableMenus(True)
                self.handleCaption(True)
                self.dirty = False
                self.filehistory.AddFileToHistory(path)
                self.destroyDlgs()
        else:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtsfiles['FileError']), i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            self.filehistory.RemoveFileFromHistory(fileNum)
        return

    def destroyDlgs(self):
        if self.trdatedlg != None:
            self.trdatedlg.Destroy()
            self.trdatedlg = None
        if self.trmondlg != None:
            self.trmondlg.Destroy()
            self.trmondlg = None
        if self.suntrdlg != None:
            self.suntrdlg.Destroy()
            self.suntrdlg = None
        if self.revdlg != None:
            self.revdlg.Destroy()
            self.revdlg = None
        if self.secdirdlg != None:
            self.secdirdlg.Destroy()
            self.secdirdlg = None
        if self.pdrangedlg != None:
            self.pdrangedlg.Destroy()
            self.pdrangedlg = None
        return

    def onReturnsList(self, event):
        if self.splash:
            return
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        frame = returnslistframe.ReturnsListFrame(self, self.title, self.horoscope, self.options)
        frame.Show(True)

    def onConditions(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            frame = conditionswnd.ConditionsFrame(self, self.title, self.horoscope, self.options)
            frame.Show(True)

    def onZRFortune(self, event):
        self.showReleasing(zodiacalreleasing.FORTUNE)

    def onZRSpirit(self, event):
        self.showReleasing(zodiacalreleasing.SPIRIT)

    def onDecennials(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            frame = decennialswnd.DecennialsFrame(self, self.title, self.horoscope, self.options)
            frame.Show(True)

    def onCircumambulation(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            frame = circumambulationwnd.CircumambulationFrame(self, self.title, self.horoscope, self.options)
            frame.Show(True)

    def onHeliacal(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            frame = heliacalwnd.HeliacalFrame(self, self.title, self.horoscope, self.options)
            frame.Show(True)

    def onFixedStarsWorkspace(self, event):
        fixedstarsworkspace.show(self, 0)

    def onStarAngles(self, event):
        fixedstarsworkspace.show(self, 2)

    def onDodecaCalc(self, event):
        dlg = dodecacalcdlg.DodecaCalcDlg(self)
        dlg.CenterOnParent()
        dlg.ShowModal()
        dlg.Destroy()

    def showReleasing(self, lot):
        if not self.splash:
            wait = wx.BusyCursor()
            frame = zodiacalreleasingwnd.ReleasingFrame(self, self.title, self.horoscope, self.options, lot)
            frame.Show(True)

    def onTemperament(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            frame = temperamentwnd.TemperamentFrame(self, self.title, self.horoscope, self.options)
            frame.Show(True)

    def showPositionsWorkspace(self, tab=0):
        """Compatibility entry point for the four original positional tables."""
        if not self.splash:
            return positionsworkspace.show(self, tab)

    def onPositionsWorkspace(self, event):
        self.showPositionsWorkspace(0)

    def onPositions(self, event):
        self.showPositionsWorkspace(positionscatalog.MENU_TABS['onPositions'])

    def onAlmutenZodiacal(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            almutenfr = almutenzodsframe.AlmutenZodsFrame(self, self.title, self.horoscope, self.options)
            almutenfr.Show(True)

    def onAlmutenChart(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            almutenfr = almutenchartframe.AlmutenChartFrame(self, self.title, self.horoscope, self.options)
            almutenfr.Show(True)

    def onAlmutenTopical(self, event):
        if not self.splash:
            if self.horoscope.options.topicals != None and len(self.horoscope.almutens.topicals.names) != 0:
                wait = wx.BusyCursor()
                topicalframe = almutentopicalsframe.AlmutenTopicalsFrame(self, self.horoscope, self.title)
                topicalframe.Show(True)
            else:
                dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NoTopicalsCreated']), '', wx.OK | wx.ICON_INFORMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
        return

    def onAntiscia(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            antisciafr = antisciaframe.AntisciaFrame(self, self.title, self.horoscope, self.options)
            antisciafr.Show(True)

    def onMisc(self, event):
        self.showPositionsWorkspace(positionscatalog.MENU_TABS['onMisc'])

    def onMunPos(self, event):
        self.showPositionsWorkspace(positionscatalog.MENU_TABS['onMunPos'])

    def onAspects(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            aspsframe = aspectsframe.AspectsFrame(self, self.title, self.horoscope, self.options)
            aspsframe.Show(True)

    def onMidpoints(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            midsframe = midpointsframe.MidPointsFrame(self, self.title, self.horoscope, self.options)
            midsframe.Show(True)

    def onRiseSet(self, event):
        hoursrisesetworkspace.show(self, 1)

    def onSpeeds(self, event):
        self.showPositionsWorkspace(positionscatalog.MENU_TABS['onSpeeds'])

    def onZodPars(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            zodparsfr = zodparsframe.ZodParsFrame(self, self.title, self.horoscope, self.options)
            zodparsfr.Show(True)

    def onFixedStars(self, event):
        fixedstarsworkspace.show(self, 0)

    def onFixedStarsAsps(self, event):
        fixedstarsworkspace.show(self, 1)

    def onLots(self, event):
        if not self.splash:
            oneselected = True in self.options.lotsvisible
            if not oneselected:
                dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NoSelLots']), '', wx.OK | wx.ICON_INFORMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
                return
            wait = wx.BusyCursor()
            lotsfr = lotsframe.LotsFrame(self, self.title, self.horoscope, self.options)
            lotsfr.Show(True)

    def onStrip(self, event):
        if not self.splash:
            wait = wx.BusyCursor()
            stripfr = stripframe.StripFrame(self, self.title, self.horoscope, self.options)
            stripfr.Show(True)

    def onHoursRiseSetWorkspace(self, event):
        hoursrisesetworkspace.show(self, 0)

    def onPlanetaryHours(self, event):
        hoursrisesetworkspace.show(self, 0)

    def onExactTransits(self, event):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        else:
            if self.trmondlg == None:
                self.trmondlg = transitmdlg.TransitMonthDlg(None, self.horoscope.time)
            self.trmondlg.CenterOnParent()
            val = self.trmondlg.ShowModal()
            if val == wx.ID_OK:
                year = int(self.trmondlg.year.GetValue())
                month = int(self.trmondlg.month.GetValue())
                wait = wx.BusyCursor()
                trans = transits.Transits()
                trans.month(year, month, self.horoscope)
                tw = transitmframe.TransitMonthFrame(self, self.title, trans.transits, year, month, self.horoscope, self.options)
                tw.Show(True)
            return

    def onProfections(self, event):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        pdlg = proftabledlg.ProfTableDlg(self)
        pdlg.initialize()
        pdlg.CenterOnParent()
        val = pdlg.ShowModal()
        if val == wx.ID_OK:
            mainsigs = pdlg.mainrb.GetValue()
            pchart = self.horoscope
            wait = wx.BusyCursor()
            y = self.horoscope.time.year
            m = self.horoscope.time.month
            d = self.horoscope.time.day
            t = self.horoscope.time.time
            if self.horoscope.time.month == 2 and self.horoscope.time.day == 29:
                d -= 1
            pcharts = []
            cyc = 0
            while cyc < 12:
                if self.options.zodprof:
                    prof = profections.Profections(self.horoscope, y, m, d, t, cyc)
                    pchart = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, self.horoscope.place, chart.Chart.PROFECTION, '', self.options, False)
                    pchart.calcProfPos(prof)
                elif not self.options.usezodprojsprof and (y + cyc == self.horoscope.time.year or (y + cyc - self.horoscope.time.year) % 12 == 0) and m == self.horoscope.time.month and d == self.horoscope.time.day:
                    pchart = self.horoscope
                else:
                    prof = munprofections.MunProfections(self.horoscope, y, m, d, t, cyc)
                    proflondeg, proflonmin, proflonsec = util.decToDeg(prof.lonZ)
                    profplace = chart.Place(mtexts.txtscommon['Profections'], proflondeg, proflonmin, proflonsec, prof.east, self.horoscope.place.deglat, self.horoscope.place.minlat, self.horoscope.place.seclat, self.horoscope.place.north, self.horoscope.place.altitude)
                    pchart = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, profplace, chart.Chart.PROFECTION, '', self.options, False, self.options.usezodprojsprof)
                    pchartpls = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, self.horoscope.place, chart.Chart.PROFECTION, '', self.options, False, self.options.usezodprojsprof)
                    pchart.planets.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.planets.planets, self.horoscope.place.lat, self.horoscope.obl[0])
                    pchart.fortune.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.fortune, self.horoscope.place.lat, self.horoscope.obl[0])
                pcharts.append((pchart, y + cyc, m, d, t))
                cyc += 1

            profsfr = profstableframe.ProfsTableFrame(self, self.title, pcharts, self.options, mainsigs)
            profsfr.Show(True)
            pstepdlg = profectiontablestepperdlg.ProfectionTableStepperDlg(profsfr, self.horoscope, self.options)
            pstepdlg.CenterOnParent()
            pstepdlg.Show(True)
        pdlg.Destroy()

    def onUserSpeculum(self, event):
        if not self.splash:
            speculum = 0
            if self.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
                speculum = 1
            if True in self.options.speculums[speculum]:
                if self.horoscope.userprompd != None:
                    wait = wx.BusyCursor()
                    usrframe = userframe.UserFrame(self, self.title, self.horoscope, self.options, self.horoscope.userprompd)
                    usrframe.Show(True)
                elif self.horoscope.usersigpd != None:
                    wait = wx.BusyCursor()
                    usrframe = userframe.UserFrame(self, self.title, self.horoscope, self.options, self.horoscope.usersigpd)
                    usrframe.Show(True)
                else:
                    dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['CheckUser']), '', wx.OK | wx.ICON_INFORMATION)
                    dlgm.ShowModal()
                    dlgm.Destroy()
            else:
                dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['SelectColumn']), '', wx.OK | wx.ICON_INFORMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
        return

    def onFirdaria(self, event):
        if not self.splash and self.horoscope.time.bc:
            # the periods are dated with Python dates, which have no BC years
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        if not self.splash:
            wait = wx.BusyCursor()
            firdfr = firdariaframe.FirdariaFrame(self, self.title, self.horoscope, self.options)
            firdfr.Show(True)

    def onPrimaryDirs(self, event):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        else:
            if self.pdrangedlg == None:
                self.pdrangedlg = primdirsrangedlg.PrimDirsRangeDlg(None)
            self.pdrangedlg.CenterOnParent()
            val = self.pdrangedlg.ShowModal()
            if val == wx.ID_OK:
                pdrange = primdirs.PrimDirs.RANGEALL
                if self.pdrangedlg.range25rb.GetValue():
                    pdrange = primdirs.PrimDirs.RANGE25
                elif self.pdrangedlg.range50rb.GetValue():
                    pdrange = primdirs.PrimDirs.RANGE50
                elif self.pdrangedlg.range75rb.GetValue():
                    pdrange = primdirs.PrimDirs.RANGE75
                elif self.pdrangedlg.range100rb.GetValue():
                    pdrange = primdirs.PrimDirs.RANGE100
                direction = primdirs.PrimDirs.BOTHDC
                if self.pdrangedlg.directrb.GetValue():
                    direction = primdirs.PrimDirs.DIRECT
                elif self.pdrangedlg.converserb.GetValue():
                    direction = primdirs.PrimDirs.CONVERSE
                keytxt = ''
                if self.options.pdkeydyn:
                    keytxt = mtexts.typeListDyn[self.options.pdkeyd]
                else:
                    keytxt = mtexts.typeListStat[self.options.pdkeys]
                txt = mtexts.typeListDirs[self.options.primarydir] + '; ' + keytxt + '\n' + mtexts.txtscommon['BusyInfo']
                self.progbar = wx.ProgressDialog(i18n.tr(mtexts.txtscommon['Calculating']), i18n.tr(txt), parent=self, style=wx.PD_CAN_ABORT | wx.PD_APP_MODAL)
                self.progbar.Fit()
                self.pds = None
                self.pdready = False
                self.abort = primdirs.AbortPD()
                thId = _thread.start_new_thread(self.calcPDs, (pdrange, direction, self))
                self.timer = wx.Timer(self)
                self.Bind(wx.EVT_TIMER, self.OnTimer)
                self.timer.Start(500)
            return

    def calcPDs(self, pdrange, direction, win):
        if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC:
            self.pds = placidiansapd.PlacidianSAPD(self.horoscope, self.options, pdrange, direction, self.abort)
        elif self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
            self.pds = placidianutppd.PlacidianUTPPD(self.horoscope, self.options, pdrange, direction, self.abort)
        elif self.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
            self.pds = regiomontanpd.RegiomontanPD(self.horoscope, self.options, pdrange, direction, self.abort)
        else:
            self.pds = campanianpd.CampanianPD(self.horoscope, self.options, pdrange, direction, self.abort)
        pdlock.acquire()
        self.pdready = True
        pdlock.release()
        evt = PDReadyEvent()
        wx.PostEvent(win, evt)

    def OnTimer(self, event):
        pdlock.acquire()
        if not self.pdready:
            keepGoing, skip = self.progbar.Pulse()
            if not keepGoing:
                self.abort.aborting()
        pdlock.release()

    def OnPDReady(self, event):
        self.timer.Stop()
        del self.timer
        self.progbar.Destroy()
        del self.progbar
        if self.abort.abort:
            self.Refresh()
        elif self.pds != None and len(self.pds.pds) > 0:
            pdw = primdirslistframe.PrimDirsListFrame(self, self.horoscope, self.options, self.pds, self.title.replace(mtexts.typeList[self.horoscope.htype], mtexts.txtsprimdirslist['PrimaryDirs']))
            pdw.Show(True)
        else:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NoPDsWithSettings']), i18n.tr(mtexts.txtscommon['Information']), wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
        if self.pds != None:
            del self.pds
        del self.abort
        return

    def onTransits(self, event):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        else:
            if self.trdatedlg == None:
                self.trdatedlg = timespacedlg.TimeSpaceDlg(None, mtexts.txtscommon['Transits'], self.options.langid, self.options.netbook)
                self.trdatedlg.initialize(self.horoscope)
            self.trdatedlg.CenterOnParent()
            val = self.trdatedlg.ShowModal()
            if val == wx.ID_OK:
                wait = wx.BusyCursor()
                direc = self.trdatedlg.placerbE.GetValue()
                hemis = self.trdatedlg.placerbN.GetValue()
                place = chart.Place(self.trdatedlg.birthplace.GetValue(), int(self.trdatedlg.londeg.GetValue()), int(self.trdatedlg.lonmin.GetValue()), 0, direc, int(self.trdatedlg.latdeg.GetValue()), int(self.trdatedlg.latmin.GetValue()), 0, hemis, int(self.trdatedlg.alt.GetValue()))
                plus = True
                if self.trdatedlg.pluscb.GetCurrentSelection() == 1:
                    plus = False
                time = chart.Time(int(self.trdatedlg.year.GetValue()), int(self.trdatedlg.month.GetValue()), int(self.trdatedlg.day.GetValue()), int(self.trdatedlg.hour.GetValue()), int(self.trdatedlg.minute.GetValue()), int(self.trdatedlg.sec.GetValue()), self.trdatedlg.timeckb.GetValue(), self.trdatedlg.calcb.GetCurrentSelection(), self.trdatedlg.zonecb.GetCurrentSelection(), plus, int(self.trdatedlg.zhour.GetValue()), int(self.trdatedlg.zminute.GetValue()), self.trdatedlg.daylightckb.GetValue(), place)
                trans = chart.Chart(self.horoscope.name, self.horoscope.male, time, place, chart.Chart.TRANSIT, '', self.options, False)
                tw = transitframe.TransitFrame(self, self.title, trans, self.horoscope, self.options)
                tw.Show(True)
            return

    def onRevolutions(self, event, planet=None):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        if self.revdlg == None:
            self.revdlg = revolutionsdlg.RevolutionsDlg(None)
            self.revdlg.initialize(self.horoscope)
        if planet is not None:
            self.revdlg.setPlanet(planet)
        self.revdlg.CenterOnParent()
        val = self.revdlg.ShowModal()
        if val == wx.ID_OK:
            wx.BeginBusyCursor()
            revs = revolutions.Revolutions()
            result = revs.compute(self.revdlg.typecb.GetCurrentSelection(), int(self.revdlg.year.GetValue()), int(self.revdlg.month.GetValue()), int(self.revdlg.day.GetValue()), self.horoscope)
            wx.EndBusyCursor()
            t1, t2, t3, t4, t5, t6 = (
             revs.t[0], revs.t[1], revs.t[2], revs.t[3], revs.t[4], revs.t[5])
            if result:
                if self.options.ayanamsha != 0 and self.revdlg.typecb.GetCurrentSelection() == 3:
                    t1, t2, t3, t4, t5, t6 = self.calcPrecNutCorrectedSolar(revs)
                dlg = timespacedlg.TimeSpaceDlg(self, revolutionsdlg.returnname(self.revdlg.typecb.GetCurrentSelection()), self.options.langid, self.options.netbook)
                ti = (t1, t2, t3, t4, t5, t6, chart.Time.GREGORIAN, chart.Time.GREENWICH, 0, 0)
                dlg.initialize(self.horoscope, ti)
                dlg.CenterOnParent()
                val = dlg.ShowModal()
                if val == wx.ID_OK:
                    wait = wx.BusyCursor()
                    direc = dlg.placerbE.GetValue()
                    hemis = dlg.placerbN.GetValue()
                    place = chart.Place(dlg.birthplace.GetValue(), int(dlg.londeg.GetValue()), int(dlg.lonmin.GetValue()), 0, direc, int(dlg.latdeg.GetValue()), int(dlg.latmin.GetValue()), 0, hemis, int(dlg.alt.GetValue()))
                    plus = True
                    if dlg.pluscb.GetCurrentSelection() == 1:
                        plus = False
                    time = chart.Time(t1, t2, t3, t4, t5, t6, False, self.horoscope.time.cal, chart.Time.GREENWICH, plus, 0, 0, False, place)
                    revtype = chart.Chart.REVOLUTION
                    if self.revdlg.typecb.GetCurrentSelection() == 3:
                        revtype = chart.Chart.SOLAR
                    elif self.revdlg.typecb.GetCurrentSelection() == 6:
                        revtype = chart.Chart.LUNAR
                    revolution = chart.Chart(self.horoscope.name, self.horoscope.male, time, place, revtype, '', self.options, False)
                    rw = transitframe.TransitFrame(self, self.title, revolution, self.horoscope, self.options)
                    rw.Show(True)
                dlg.Destroy()
            else:
                dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['CouldnotComputeRevolution']), i18n.tr(mtexts.txtscommon['Error']), wx.OK | wx.ICON_EXCLAMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
        return

    def calcPrecNutCorrectedSolar(self, revs):
        time = chart.Time(revs.t[0], revs.t[1], revs.t[2], revs.t[3], revs.t[4], revs.t[5], False, self.horoscope.time.cal, chart.Time.GREENWICH, False, 0, 0, False, self.horoscope.place, False)
        jdSol = time.jd
        JD1900 = 2415020.5
        FBAyanamsa1900 = astrology.swe_get_ayanamsa_ut(JD1900)
        rflag, dat, serr = astrology.swe_calc_ut(JD1900, astrology.SE_ECL_NUT, 0)
        NutLon1900 = dat[2]
        SVP1900 = 360.0 - FBAyanamsa1900 - NutLon1900
        rflag, dat, serr = astrology.swe_calc_ut(self.horoscope.time.jd, astrology.SE_ECL_NUT, 0)
        NutLonNatal = dat[2]
        SVPNatal = 360.0 - self.horoscope.ayanamsha - NutLonNatal
        NatalChartPrecessionFrom1900 = SVPNatal - SVP1900
        NatalSunLon = self.horoscope.planets.planets[planets.Planets.SUN].data[planets.Planet.LON]
        DiffAngle = 50.0
        pflag = astrology.SEFLG_SWIEPH + astrology.SEFLG_SPEED
        while DiffAngle > 1e-05:
            rflag, dat, serr = astrology.swe_calc_ut(jdSol, astrology.SE_SUN, pflag)
            TranSunLon = dat[0]
            TranSunVel = dat[3]
            rflag, dat, serr = astrology.swe_calc_ut(jdSol, astrology.SE_ECL_NUT, 0)
            FBAyanamsaReturn = astrology.swe_get_ayanamsa_ut(jdSol)
            NutLonReturn = dat[2]
            SVPReturn = 360.0 - FBAyanamsaReturn - NutLonReturn
            SolPrecessionFrom1900 = SVPReturn - SVP1900
            Precession = SolPrecessionFrom1900 - NatalChartPrecessionFrom1900
            TranSunLon = TranSunLon + Precession
            DiffAngle = NatalSunLon - TranSunLon
            if math.fabs(DiffAngle) > 180.0:
                DiffAngle = DiffAngle - util.sgn(DiffAngle) * 360.0
            CorrectionJD = DiffAngle / TranSunVel
            jdSol = jdSol + CorrectionJD
            fromjdtime = astrology.swe_revjul(jdSol, astrology.SE_GREG_CAL)

        h, mi, s = util.decToDeg(fromjdtime[3])
        return (fromjdtime[0], fromjdtime[1], fromjdtime[2], h, mi, s)

    def onSunTransits(self, event):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        if self.suntrdlg == None:
            self.suntrdlg = suntransitsdlg.SunTransitsDlg(None)
            self.suntrdlg.initialize(self.horoscope)
        self.suntrdlg.CenterOnParent()
        val = self.suntrdlg.ShowModal()
        if val == wx.ID_OK:
            wx.BeginBusyCursor()
            lons = (
             self.horoscope.houses.ascmc[houses.Houses.ASC], self.horoscope.houses.ascmc[houses.Houses.MC], self.horoscope.planets.planets[planets.Planets.SATURN].data[planets.Planet.LON], self.horoscope.planets.planets[planets.Planets.JUPITER].data[planets.Planet.LON], self.horoscope.planets.planets[planets.Planets.MARS].data[planets.Planet.LON], self.horoscope.planets.planets[planets.Planets.SUN].data[planets.Planet.LON], self.horoscope.planets.planets[planets.Planets.VENUS].data[planets.Planet.LON], self.horoscope.planets.planets[planets.Planets.MERCURY].data[planets.Planet.LON], self.horoscope.planets.planets[planets.Planets.MOON].data[planets.Planet.LON])
            btns = (self.suntrdlg.ascrb.GetValue(), self.suntrdlg.mcrb.GetValue(), self.suntrdlg.saturnrb.GetValue(), self.suntrdlg.jupiterrb.GetValue(), self.suntrdlg.marsrb.GetValue(), self.suntrdlg.sunrb.GetValue(), self.suntrdlg.venusrb.GetValue(), self.suntrdlg.mercuryrb.GetValue(), self.suntrdlg.moonrb.GetValue())
            trlon = lons[0]
            for i in range(len(btns)):
                if btns[i]:
                    trlon = lons[i]

            suntrs = suntransits.SunTransits()
            result = suntrs.compute(int(self.suntrdlg.year.GetValue()), int(self.suntrdlg.month.GetValue()), int(self.suntrdlg.day.GetValue()), self.horoscope, trlon)
            wx.EndBusyCursor()
            if result:
                dlg = timespacedlg.TimeSpaceDlg(self, mtexts.txtssuntransitsdlg['SunTransits'], self.options.langid, self.options.netbook)
                ti = (suntrs.t[0], suntrs.t[1], suntrs.t[2], suntrs.t[3], suntrs.t[4], suntrs.t[5], chart.Time.GREGORIAN, chart.Time.GREENWICH, 0, 0)
                dlg.initialize(self.horoscope, ti)
                dlg.CenterOnParent()
                val = dlg.ShowModal()
                if val == wx.ID_OK:
                    wait = wx.BusyCursor()
                    direc = dlg.placerbE.GetValue()
                    hemis = dlg.placerbN.GetValue()
                    place = chart.Place(dlg.birthplace.GetValue(), int(dlg.londeg.GetValue()), int(dlg.lonmin.GetValue()), 0, direc, int(dlg.latdeg.GetValue()), int(dlg.latmin.GetValue()), 0, hemis, int(dlg.alt.GetValue()))
                    plus = True
                    if dlg.pluscb.GetCurrentSelection() == 1:
                        plus = False
                    time = chart.Time(suntrs.t[0], suntrs.t[1], suntrs.t[2], suntrs.t[3], suntrs.t[4], suntrs.t[5], False, chart.Time.GREGORIAN, chart.Time.GREENWICH, plus, 0, 0, False, place)
                    suntrschart = chart.Chart(self.horoscope.name, self.horoscope.male, time, place, chart.Chart.TRANSIT, '', self.options, False)
                    rw = transitframe.TransitFrame(self, self.title, suntrschart, self.horoscope, self.options)
                    rw.Show(True)
                dlg.Destroy()
            else:
                dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['CouldnotComputeTransit']), i18n.tr(mtexts.txtscommon['Error']), wx.OK | wx.ICON_EXCLAMATION)
                dlgm.ShowModal()
                dlgm.Destroy()
        return

    def onSecondaryDirs(self, event):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        else:
            if self.secdirdlg == None:
                self.secdirdlg = secdirdlg.SecondaryDirsDlg(None)
                self.secdirdlg.initialize()
            self.secdirdlg.CenterOnParent()
            val = self.secdirdlg.ShowModal()
            if val == wx.ID_OK:
                age = int(self.secdirdlg.age.GetValue())
                direct = self.secdirdlg.directrb.GetValue()
                soltime = self.secdirdlg.solartimerb.GetValue()
                zt = chart.Time.LOCALMEAN
                if soltime:
                    zt = chart.Time.LOCALAPPARENT
                zh = 0
                zm = 0
                sdir = secdir.SecDir(self.horoscope, age, direct, soltime)
                y, m, d, hour, minute, second = sdir.compute()
                dlg = timespacedlg.TimeSpaceDlg(self, mtexts.txtssecdirdlg['SecondaryDirs'], self.options.langid, self.options.netbook)
                ti = (y, m, d, hour, minute, second, self.horoscope.time.cal, zt, zh, zm)
                dlg.initialize(self.horoscope, ti)
                dlg.CenterOnParent()
                val = dlg.ShowModal()
                if val == wx.ID_OK:
                    wait = wx.BusyCursor()
                    direc = dlg.placerbE.GetValue()
                    hemis = dlg.placerbN.GetValue()
                    place = chart.Place(dlg.birthplace.GetValue(), int(dlg.londeg.GetValue()), int(dlg.lonmin.GetValue()), 0, direc, int(dlg.latdeg.GetValue()), int(dlg.latmin.GetValue()), 0, hemis, int(dlg.alt.GetValue()))
                    plus = True
                    if dlg.pluscb.GetCurrentSelection() == 1:
                        plus = False
                    time = chart.Time(y, m, d, hour, minute, second, False, self.horoscope.time.cal, zt, plus, zh, zm, False, place)
                    secdirchart = chart.Chart(self.horoscope.name, self.horoscope.male, time, place, chart.Chart.TRANSIT, '', self.options, False)
                    sf = secdirframe.SecDirFrame(self, self.title, secdirchart, self.horoscope, self.options)
                    sf.Show(True)
                    stepdlg = stepperdlg.StepperDlg(sf, self.horoscope, age, direct, soltime, self.options, self.title)
                    stepdlg.CenterOnParent()
                    stepdlg.Show(True)
                dlg.Destroy()
            return

    def onElections(self, event):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        time = chart.Time(self.horoscope.time.origyear, self.horoscope.time.origmonth, self.horoscope.time.origday, self.horoscope.time.hour, self.horoscope.time.minute, self.horoscope.time.second, self.horoscope.time.bc, self.horoscope.time.cal, self.horoscope.time.zt, self.horoscope.time.plus, self.horoscope.time.zh, self.horoscope.time.zm, self.horoscope.time.daylightsaving, self.horoscope.place)
        electionchart = chart.Chart(self.horoscope.name, self.horoscope.male, time, self.horoscope.place, chart.Chart.TRANSIT, '', self.options, False)
        ef = electionsframe.ElectionsFrame(self, self.title, electionchart, self.horoscope, self.options)
        ef.Show(True)
        estepdlg = electionstepperdlg.ElectionStepperDlg(ef, self.horoscope, self.options, self.title)
        estepdlg.CenterOnParent()
        estepdlg.Show(True)

    def onSquareChart(self, event):
        sc = squarechartframe.SquareChartFrame(self, self.title, self.horoscope, self.options)
        sc.Show(True)

    def onSyzygyChart(self, event):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        syzygychart = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.syzygy.time, self.horoscope.place, chart.Chart.TRANSIT, '', self.options, False)
        # Left/Right (or its menu): the lunations before and after
        ef = transitframe.TransitFrame(self, self.title, syzygychart, self.horoscope, self.options, stepper=lunationnavigator.stepper(self.horoscope, self.options))
        ef.Show(True)

    def onCompareGrid(self, event):
        comparegrid.show(self)

    def onMultiWheel(self, event):
        multiwheel.show(self)

    def onTransitSearch(self, event):
        transitsearch.show(self)

    def onSunTransitSearch(self, event):
        transitsearch.show(self, sun=True)

    def onLunationNavigator(self, event):
        lunationnavigator.show(self)

    def onSyzygyChart2(self, event):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        syzygychart = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.syzygy.time2, self.horoscope.place, chart.Chart.TRANSIT, '', self.options, False)
        # Left/Right (or its menu): the lunations before and after
        ef = transitframe.TransitFrame(self, self.title, syzygychart, self.horoscope, self.options, stepper=lunationnavigator.stepper(self.horoscope, self.options))
        ef.Show(True)

    def onProfectionsChart(self, event):
        if self.horoscope.time.bc:
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NotAvailable']), '', wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            return
        pdlg = profdlg.ProfDlg(self, self.horoscope.time.jd, self.horoscope.place)
        pdlg.initialize(self.horoscope.time.year, self.horoscope.time.month, self.horoscope.time.day, 12, 0, 0)
        pdlg.CenterOnParent()
        val = pdlg.ShowModal()
        if val == wx.ID_OK:
            y = int(pdlg.year.GetValue())
            m = int(pdlg.month.GetValue())
            d = int(pdlg.day.GetValue())
            h = int(pdlg.hour.GetValue())
            mi = int(pdlg.minute.GetValue())
            s = int(pdlg.second.GetValue())
            t = h + mi / 60.0 + s / 3600.0
            if self.options.zodprof:
                prof = profections.Profections(self.horoscope, y, m, d, t)
                pchart = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, self.horoscope.place, chart.Chart.PROFECTION, '', self.options, False)
                pchart.calcProfPos(prof)
            elif not self.options.usezodprojsprof and (y == self.horoscope.time.year or (y - self.horoscope.time.year) % 12 == 0) and m == self.horoscope.time.month and d == self.horoscope.time.day:
                pchart = self.horoscope
            else:
                prof = munprofections.MunProfections(self.horoscope, y, m, d, t)
                proflondeg, proflonmin, proflonsec = util.decToDeg(prof.lonZ)
                profplace = chart.Place(mtexts.txtscommon['Profections'], proflondeg, proflonmin, proflonsec, prof.east, self.horoscope.place.deglat, self.horoscope.place.minlat, self.horoscope.place.seclat, self.horoscope.place.north, self.horoscope.place.altitude)
                pchart = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, profplace, chart.Chart.PROFECTION, '', self.options, False, self.options.usezodprojsprof)
                pchartpls = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, self.horoscope.place, chart.Chart.PROFECTION, '', self.options, False, self.options.usezodprojsprof)
                pchart.planets.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.planets.planets, self.horoscope.place.lat, self.horoscope.obl[0])
                pchart.fortune.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.fortune, self.horoscope.place.lat, self.horoscope.obl[0])
                pchart.calcAspMatrices()
            pf = profectionsframe.ProfectionsFrame(self, self.title.replace(mtexts.typeList[self.horoscope.htype], mtexts.txtscommon['Profections'] + ' (' + str(y) + '.' + str(m) + '.' + str(d) + ' ' + str(h).zfill(2) + ':' + str(mi).zfill(2) + ':' + str(s).zfill(2) + ')'), pchart, self.horoscope, self.options)
            pf.Show(True)
            pstepdlg = profectionstepperdlg.ProfectionStepperDlg(pf, self.horoscope, y, m, d, t, self.options, self.title)
            pstepdlg.CenterOnParent()
            pstepdlg.Show(True)
        pdlg.Destroy()

    def onHelioChart(self, event):
        hc = heliochartframe.HelioChartFrame(self, self.title, self.horoscope, self.options)
        hc.Show(True)

    def onAppearance1(self, event):
        wx.BeginBusyCursor()
        dlg = appearance1dlg.Appearance1Dlg(self)
        dlg.CenterOnParent()
        wx.EndBusyCursor()
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        topocentric = self.options.topocentric
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.updateViewMenu()
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveAppearance1():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    if topocentric != self.options.topocentric:
                        self.horoscope.recalc()
                    self.clickedPlId = None
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()
        return

    def onAppearance2(self, event):
        wx.BeginBusyCursor()
        dlg = appearance2dlg.Appearance2Dlg(self)
        dlg.CenterOnParent()
        wx.EndBusyCursor()
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveAppearance2():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()

    def onDignities(self, event):
        dlg = dignitiesdlg.DignitiesDlg(self, self.options)
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveDignities():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.clickedPlId = None
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()
        return

    def onTriplicities(self, event):
        wx.BeginBusyCursor()
        dlg = triplicitiesdlg.TriplicitiesDlg(self, self.options)
        dlg.CenterOnParent()
        wx.EndBusyCursor()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveTriplicities():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.horoscope.calcAlmutens()
        dlg.Destroy()

    def onTerms(self, event):
        wx.BeginBusyCursor()
        dlg = termsdlg.TermsDlg(self, self.options)
        dlg.CenterOnParent()
        wx.EndBusyCursor()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveTerms():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.horoscope.calcAlmutens()
                    self.clickedPlId = None
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()
        return

    def onDecans(self, event):
        wx.BeginBusyCursor()
        dlg = decansdlg.DecansDlg(self, self.options)
        dlg.CenterOnParent()
        wx.EndBusyCursor()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveDecans():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.horoscope.calcAlmutens()
                    self.clickedPlId = None
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()
        return

    def onChartAlmuten(self, event):
        wx.BeginBusyCursor()
        dlg = almutenchartdlg.AlmutenChartDlg(self)
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        dlg.CenterOnParent()
        wx.EndBusyCursor()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveChartAlmuten():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.horoscope.calcAlmutens()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()

    def onTopicals(self, event):
        wx.BeginBusyCursor()
        dlg = almutentopicalsdlg.AlmutenTopicalsDlg(self, self.options)
        dlg.fill(self.options)
        dlg.CenterOnParent()
        wx.EndBusyCursor()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveTopicalandLots():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.horoscope.calcAlmutens()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()

    def onAyanamsha(self, event):
        dlg = ayanamshadlg.AyanamshaDlg(self)
        dlg.CenterOnParent()
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        ayan = self.options.ayanamsha
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveAyanamsa():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    if ayan != self.options.ayanamsha:
                        self.horoscope.recalc()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()

    def onColors(self, event):
        dlg = colorsdlg.ColorsDlg(self)
        dlg.CenterOnParent()
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveColors():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.clickedPlId = None
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()
        return

    def onChartLook(self, event):
        colours, look = chartlookdlg.show(self, self.options, None if self.splash else self.horoscope)
        if colours or look:
            self.enableOptMenus(True)
            if self.options.autosave:
                tradoptions.save()
                if self.options.saveColors():
                    self.moptions.Enable(self.ID_SaveOpts, False)
            if not self.splash:
                self.closeChildWnds()
                self.clickedPlId = None
                self.drawBkg()
                self.Refresh()

    def onHouseSystem(self, event):
        hs = event.GetId() - self.hsbase
        if self.options.hsys != hs:
            self.options.hsys = hs
            self.enableOptMenus(True)
            if self.options.autosave:
                if self.options.saveHouseSystem():
                    self.moptions.Enable(self.ID_SaveOpts, False)
            if not self.splash:
                self.closeChildWnds()
                self.horoscope.setHouseSystem()
                self.horoscope.calcHcsAspMatrix()
                self.horoscope.calcHCsFixedStarAspMatrix()
                self.horoscope.calcLots()
                self.horoscope.calcAlmutens()
                self.clickedPlId = None
                self.drawBkg()
                self.Refresh()
        return

    def onNodes(self, event):
        typ = event.GetId() - self.nodebase
        nodes = (True, False)
        if self.options.meannode != nodes[typ]:
            self.options.meannode = nodes[typ]
            self.enableOptMenus(True)
            if self.options.autosave:
                if self.options.saveNodes():
                    self.moptions.Enable(self.ID_SaveOpts, False)
            if not self.splash:
                self.closeChildWnds()
                self.horoscope.setNodes()
                self.horoscope.calcPlsAspMatrix()
                self.horoscope.calcPlsFixedStarAspMatrix()
                self.clickedPlId = None
                self.drawBkg()
                self.Refresh()
        return

    def onOrbs(self, event):
        nofs = False
        if not self.checkFixedStars():
            nofs = True
        elif len(self.options.fixedstars) == 0:
            nofs = True
        dlg = orbsdlg.OrbsDlg(self, self.options, nofs)
        dlg.CenterOnParent()
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveOrbs():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.horoscope.calcLots()
                    self.horoscope.calcAspMatrices()
                    self.horoscope.calcFixedStarAspMatrices()
                    self.horoscope.calcAlmutens()
                    self.clickedPlId = None
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()
        return

    def onPrimaryDirsOpt(self, event):
        wx.BeginBusyCursor()
        dlg = None
        if self.options.netbook:
            dlg = primarydirsdlgsmall.PrimDirsDlgSmall(self, self.options, common.common.ephepath)
        else:
            dlg = primarydirsdlg.PrimDirsDlg(self, self.options, common.common.ephepath)
        dlg.CenterOnParent()
        wx.EndBusyCursor()
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            changed, changedU1, changedU2 = dlg.check(self.options)
            if changed or changedU1 or changedU2:
                if changedU1 and not self.splash:
                    uprompd = None
                    if self.options.pduser:
                        uprompd = userpd.UserPD(self.options.pduserlon[0], self.options.pduserlon[1], self.options.pduserlon[2], self.options.pduserlat[0], self.options.pduserlat[1], self.options.pduserlat[2], self.options.pdusersouthern, self.horoscope.place.lat, self.horoscope.houses.ascmc2, self.horoscope.obl[0])
                    self.horoscope.setUserPromPD(uprompd)
                if changedU2 and not self.splash:
                    usigpd = None
                    if self.options.pduser2:
                        usigpd = userpd.UserPD(self.options.pduser2lon[0], self.options.pduser2lon[1], self.options.pduser2lon[2], self.options.pduser2lat[0], self.options.pduser2lat[1], self.options.pduser2lat[2], self.options.pduser2southern, self.horoscope.place.lat, self.horoscope.houses.ascmc2, self.horoscope.obl[0])
                    self.horoscope.setUserSigPD(usigpd)
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.savePrimaryDirs():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()
        return

    def onPrimaryKeys(self, event):
        dlg = primarykeysdlg.PrimaryKeysDlg(self, self.options)
        dlg.CenterOnParent()
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.savePrimaryKeys():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()

    def onPDsInChartOpt(self, event):
        dlg = pdsinchartdlgopts.PDsInChartsDlgOpts(self)
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.savePDsInChart():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()

    def onSyzygy(self, event):
        dlg = syzygydlg.SyzygyDlg(self)
        dlg.CenterOnParent()
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveSyzygy():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.horoscope.calcSyzygy()
                    self.horoscope.calcLots()
                    self.horoscope.calcAlmutens()
                    self.clickedPlId = None
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()
        return

    def onLotsOpt(self, event):
        wx.BeginBusyCursor()
        dlg = lotsdlg.LotsDlg(self, self.options)
        dlg.CenterOnParent()
        dlg.fill(self.options)
        wx.EndBusyCursor()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            ch, rem = dlg.check(self.options)
            if ch:
                self.enableOptMenus(True)
                if rem:
                    if self.options.topicals != None:
                        del self.options.topicals
                        self.options.topicals = None
                if self.options.autosave:
                    if self.options.saveTopicalandLots():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.horoscope.calcAntiscia()
                    self.horoscope.calcLots()
                    self.horoscope.calcFortune()
                    self.horoscope.calcAlmutens()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()
        return

    def onFixedStarsOpt(self, event):
        if not self.checkFixedStars():
            return
        else:
            dlg = fixedstarsdlg.FixedStarsDlg(self, self.options.fixedstars, common.common.ephepath)
            dlg.CenterOnParent()
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                if dlg.check(self.options.fixedstars, self.options):
                    self.enableOptMenus(True)
                    self.options.clearPDFSSel()
                    if self.options.autosave:
                        if self.options.saveFixedstars():
                            self.moptions.Enable(self.ID_SaveOpts, False)
                    if not self.splash:
                        self.closeChildWnds()
                        self.horoscope.calcFixedStars()
                        self.horoscope.calcFixedStarAspMatrices()
                        self.clickedPlId = None
                        self.drawBkg()
                        self.Refresh()
            dlg.Destroy()
            return

    def onProfectionsOpt(self, event):
        dlg = profdlgopts.ProfDlgOpts(self)
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveProfections():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()

    def onFirdariaOpt(self, event):
        dlg = firdariadlg.FirdariaDlg(self)
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveFirdaria():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()

    def onDefLocationOpt(self, event):
        dlg = defaultlocdlg.DefaultLocDlg(self, self.options.langid, self.options.netbook)
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveDefLocation():
                        self.moptions.Enable(self.ID_SaveOpts, False)
                if not self.splash:
                    self.closeChildWnds()
                    self.drawBkg()
                    self.Refresh()
        dlg.Destroy()

    def onMenuSelFirst(self, event):
        dlg = menuseldlg.MenuSelDlg(self)
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveMenuSel():
                        self.moptions.Enable(self.ID_SaveOpts, False)
        dlg.Destroy()

    def onMenuSelSecond(self, event):
        dlg = menuseldlg2.MenuSelDlg(self)
        defaultsbtn.add(dlg, self.options)
        dlg.fill(self.options)
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveMenuSel():
                        self.moptions.Enable(self.ID_SaveOpts, False)
        dlg.Destroy()

    def onLanguages(self, event):
        dlg = langsdlg.LanguagesDlg(self, self.options.langid)
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.check(self.options):
                self.enableOptMenus(True)
                if self.options.autosave:
                    if self.options.saveLanguages():
                        self.moptions.Enable(self.ID_SaveOpts, False)
        dlg.Destroy()

    def onSettings(self, event):
        settingswnd.show(self)

    def onTradOpts(self, index):
        if tradoptsdlg.show(self, index, self.options.autosave):
            if not self.options.autosave:
                self.enableOptMenus(True)

    def onAutoSaveOpts(self, event):
        self.options.autosave = self.autosave.IsChecked()
        if self.options.autosave:
            tradoptions.save()
            if self.options.save():
                self.moptions.Enable(self.ID_SaveOpts, False)

    def onSaveOpts(self, event):
        tradoptions.save()
        if self.options.save():
            self.moptions.Enable(self.ID_SaveOpts, False)

    def onReload(self, event):
        dlg = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['AreYouSure']), i18n.tr(mtexts.txtscommon['Confirm']), wx.YES_NO | wx.ICON_QUESTION)
        val = dlg.ShowModal()
        if val == wx.ID_YES:
            if self.options.checkOptsFiles():
                self.options.removeOptsFiles()
            self.options.reload()
            if os.path.exists(tradoptions.FILENAME):
                os.remove(tradoptions.FILENAME)
            tradoptions.load()
            self.enableOptMenus(False)
            self.setHouse()
            self.setNode()
            self.setAutoSave()
            self.updateViewMenu()
            if not self.splash:
                self.closeChildWnds()
                self.horoscope.recalc()
                self.clickedPlId = None
                self.drawBkg()
                self.Refresh()
        return

    def onHelp(self, event):
        fname = os.path.join('Res', mtexts.helptxt)
        if not os.path.exists(fname):
            txt = fname + ' ' + mtexts.txtsfiles['NotFound']
            dlgm = wx.MessageDialog(self, i18n.tr(txt), i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
        else:
            hframe = htmlhelpframe.HtmlHelpFrame(self, -1, mtexts.txtscommon['ProgramTitle'], fname)
            hframe.Show(True)

    def onAbout(self, event):
        info = wx.adv.AboutDialogInfo()
        info.Name = mtexts.txtscommon['ProgramTitle']
        info.Version = '6.2'
        info.Copyright = mtexts.txtscommon['FreeSoft']
        info.Description = mtexts.txtscommon['Description'] + str(astrology.swe_version())
        info.WebSite = ('http://sites.google.com/site/pymorinus/', 'http://sites.google.com/site/pymorinus/')
        info.Developers = ['Robert Nagy (Hungary); robert.pluto@gmail.com (programming and astrology)\nPhilippe Epaud(France); philipeau@free.fr (french translation)\nMargherita Fiorello (Italy); margherita.fiorello@gmail.com (astrology)\nMartin Gansten (Sweden); http://www.martingansten.com/ (astrology)\nRoberto Luporini (Italy); roberto.luporini@tiscali.it (Astrological astronomy)\nPetr Radek (Czech Rep.); petr_radek@raz-dva.cz (astrology)\nEndre Csaba Simon (Finland); secsaba@gmail.com (programming and astrology)\nDenis Steinhoff (Israel); denis@steindan.com (astrology, russian translation)\nV\xc3\xa1clav Jan \xc5\xa0pirhanzl (Czech Rep.); vjs.morinus@gmail.com (MacOS version)']
        info.License = mtexts.licensetxt
        wx.adv.AboutBox(info)

    def setHouse(self):
        sysh = (
         self.itplac, self.itkoch, self.itregio, self.itcampa, self.itequal, self.itwhole, self.itaxial, self.itmorin, self.ithoriz, self.itpage, self.italcab, self.itporph)
        sysh[self.options.hsys].Check(True)
        if getattr(self, 'tbhouses', None):
            self.tbhouses.SetSelection(self.options.hsys)

    def setNode(self):
        if self.options.meannode:
            self.meanitem.Check(True)
        else:
            self.trueitem.Check(True)

    def setAutoSave(self):
        self.autosave.Check(self.options.autosave)

    def checkFixedStars(self):
        res = True
        fname = os.path.join(common.common.ephepath, starnames.CATALOGUE)
        if not os.path.exists(fname):
            txt = fname + ' ' + mtexts.txtsfiles['NotFound']
            dlgm = wx.MessageDialog(self, i18n.tr(txt), i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
            res = False
        return res

    def closeChildWnds(self):
        li = self.GetChildren()
        for ch in li:
            x, y = ch.GetClientSize()
            if ch.GetName() != 'status_line' and y > 50 and ch is not self.settingswnd and ch is not self.sidebar and ch not in getattr(self, 'keep_open', ()) and not isinstance(ch, (wx.ToolBar, wx.PopupWindow)):
                ch.Destroy()

    def enableMenus(self, bEnable):
        """Enables the items that need a chart (New and Here and now only without one)."""
        menubar = self.GetMenuBar()
        for iid in (self.ID_New, self.ID_HereAndNow):
            if menubar.FindItemById(iid):
                menubar.Enable(iid, not bEnable)
        ids = [self.ID_Data, self.ID_Save, self.ID_SaveAsBitmap, self.ID_Synastry, self.ID_Close, self.ID_TAlmutens] + list(range(self.ID_Positions, self.ID_PrimaryDirs + 1))
        ids += list(range(self.ID_Transits, self.ID_HelioChart + 1)) + self.returnids
        ids += [self.ID_TradConditions, self.ID_TradTemperament, self.ID_ZRFortune, self.ID_ZRSpirit, self.ID_Decennials, self.ID_Circumambulation, self.ID_Heliacal, self.ID_ReturnsList, self.ID_PositionsWorkspace, self.ID_FixedStarsWorkspace, self.ID_HoursRiseSetWorkspace, self.ID_LunationNavigator, self.ID_TransitSearch, self.ID_CompareGrid, self.ID_MultiWheel]
        for iid in ids:
            if menubar.FindItemById(iid):
                menubar.Enable(iid, bEnable)
        if getattr(self, 'toolbar', None):
            for iid in self.toolids:
                self.toolbar.EnableTool(iid, menubar.IsEnabled(iid))

    def enableOptMenus(self, bEnable):
        self.moptions.Enable(self.ID_SaveOpts, bEnable)
        self.moptions.Enable(self.ID_Reload, bEnable)

    def handleCaption(self, bHor):
        if bHor:
            path = self.fpath
            if self.fpath == '':
                path = '-----'
            txt = self.origtitle + ' - ' + '[' + path + ']'
            self.title = txt
        else:
            self.title = self.origtitle
        self.SetTitle(i18n.tr(self.title))

    def drawSplash(self):
        splashpath = os.path.join('Res', 'Morinus.jpg')
        self.buffer = wx.Image(splashpath).ConvertToBitmap()
        self.updateStatus()
        if getattr(self, 'sidebar', None):
            self.placeSidebar()

    def drawBkg(self):
        self.placeSidebar()
        self.gchart = graphchart.GraphChart(self.horoscope, self.chartSize(), self.options, self.options.bw, self.clickedPlId)
        self.buffer = self.gchart.drawChart()
        self.updateStatus()
        if self.sidebar.IsShown():
            self.sidebar.setChart(self.horoscope)

    def chartSize(self):
        """The client area less the actual sidebar width."""
        w, h = self.GetClientSize()
        if self.sidebar.IsShown():
            w -= self.sidebar.GetSize().width
        return wx.Size(max(w, 50), h)

    def placeSidebar(self):
        show = tradoptions.get('show_sidebar') and not self.splash
        if show:
            w, h = self.GetClientSize()
            sw = sidebar.fit_width(w, self.sidebar_width)
            self.sidebar.SetSize(w - sw, 0, sw, h)
        self.sidebar.Show(show)

    def onSidebarResize(self, preferred, finished):
        """Resize the chart area; persist the width only on release."""
        if self.splash:
            return
        width = sidebar.fit_width(self.GetClientSize().width, preferred)
        if width == self.sidebar.GetSize().width and not finished:
            return
        self.sidebar_width = width
        now = _time.monotonic()
        if finished:
            tradoptions.set({'sidebar_width': width})
            if self.options.autosave:
                tradoptions.save()
        # Drawing the full wheel is expensive; throttle resize repaints.
        if finished or now - self._sidebar_last_draw >= 0.08:
            self._sidebar_last_draw = now
            self.drawBkg()
            self.Refresh()
        else:
            self.placeSidebar()

    def onViewSidebar(self, event):
        show = event.IsChecked()
        tradoptions.set({'show_sidebar': show})
        if self.options.autosave:
            tradoptions.save()
        self.viewsidebar.Check(show)
        self.toolbar.ToggleTool(self.ID_SidebarTool, show)
        if not self.splash:
            self.drawBkg()
            self.Refresh()

    def updateStatus(self):
        """The status bar: the chart, sect, the planetary day and hour, the house system, zodiac and nodes."""
        if self.splash:
            for i in range(4):
                self.statusbar.SetStatusText('', i)
            return
        h = self.horoscope
        t = h.time
        zones = (mtexts.txtscommon['ZN'], mtexts.txtscommon['UT'], mtexts.txtscommon['LC'], mtexts.txtscommon['LC'])
        date = '%s%d.%s.%02d  %02d:%02d:%02d %s' % ('-' if t.bc else '', t.origyear, mtexts.months[t.origmonth - 1], t.origday, t.hour, t.minute, t.second, zones[t.zt])
        self.statusbar.SetStatusText('   '.join(x for x in (h.name, date, h.place.placename) if x), 0)
        day = h.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].abovehorizon
        if self.options.usedaynightorb:
            day = h.abovehorizonwithorb
        self.statusbar.SetStatusText(i18n.tr('Day chart' if day else 'Night chart'), 1)
        names = [mtexts.txtscommon[k] for k in ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')]
        ar = (6, 2, 5, 1, 4, 0, 3)
        self.statusbar.SetStatusText(i18n.tr('%s day, %s hour') % (names[ar[t.ph.weekday]], names[t.ph.planetaryhour]), 2)
        zodiac = self.gchart.ayans[self.options.ayanamsha] if self.options.ayanamsha else mtexts.txtsayanamsha['Tropical']
        node = mtexts.menutxts['OMNMean' if self.options.meannode else 'OMNTrue'].split('\t')[0].replace('&', '')
        self.statusbar.SetStatusText(i18n.tr('%s \u00b7 %s \u00b7 %s node') % (self.gchart.hsystem[self.options.hsys], zodiac, node.lower()), 3)

    def onEraseBackground(self, event):
        dc = wx.ClientDC(self)
        x = y = 0
        if self.splash:
            size = self.GetClientSize()
            x = size.x // 2 - self.buffer.GetWidth() // 2
            y = size.y // 2 - self.buffer.GetHeight() // 2
            bkgclr = self.options.clrbackground
            if self.options.bw:
                bkgclr = (255, 255, 255)
            self.SetBackgroundColour(bkgclr)
            self.ClearBackground()
        dc.DrawBitmap(self.buffer, x, y)

    def onPaint(self, event):
        # GTK3 only allows drawing from a PaintDC in the paint handler
        dc = wx.PaintDC(self)
        x = y = 0
        if self.splash:
            size = self.GetClientSize()
            x = size.x // 2 - self.buffer.GetWidth() // 2
            y = size.y // 2 - self.buffer.GetHeight() // 2
            bkgclr = self.options.clrbackground
            if self.options.bw:
                bkgclr = (255, 255, 255)
            dc.SetBackground(wx.Brush(bkgclr))
            dc.Clear()
        dc.DrawBitmap(self.buffer, x, y)

    def onLeftUp(self, event):
        if not self.splash and self.options.enableclick:
            self.clickedPlId = self.gchart.onClick(event.GetPosition())
            self.gchart = graphchart.GraphChart(self.horoscope, self.chartSize(), self.options, self.options.bw, self.clickedPlId)
            self.buffer = self.gchart.drawChart()
            self.sidebar.select(self.clickedPlId)
            self.Refresh()

    def onSize(self, event):
        if self.splash:
            self.Refresh()
        else:
            self.drawBkg()
            self.Refresh()
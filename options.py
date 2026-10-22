# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
import os
import wx
import pickle
import copy
import lots
import mtexts

class Options:

    def __init__(self):
        self.def_houses = self.houses = True
        self.def_bw = self.bw = False
        self.def_tablesize = self.tablesize = 0.75
        # the look of this version (Appearance I and II, Colors): white, black planets,
        # terms, decans and duads shown, every speculum column
        self.def_showterms = self.showterms = True
        self.def_showdecans = self.showdecans = True
        self.def_showobject = self.showobject = 4
        self.def_showfixedstarsnodes = self.showfixedstarsnodes = False
        self.def_showfixedstarshcs = self.showfixedstarshcs = False
        self.def_showfixedstarslof = self.showfixedstarslof = False
        self.def_showfixedstarsoutoforb = self.showfixedstarsoutoforb = False
        self.def_maxascmcsize = self.maxascmcsize = 2
        self.def_housesystem = self.housesystem = True
        self.def_topocentric = self.topocentric = False
        self.def_enableclick = self.enableclick = True
        self.def_showdata = self.showdata = True
        self.def_netbook = self.netbook = False
        self.speculums = [
         [
          True, True, True, True, True, True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True, True, True]]
        self.def_speculums = copy.deepcopy(self.speculums)
        self.intime = False
        self.def_intime = self.intime
        self.dignities = [
         [
          [
           False, False, False, False, False, False, False, False, False, True, True, False], [False, False, False, False, False, False, True, False, False, False, False, False]],
         [
          [
           False, False, False, False, False, False, False, False, True, False, False, True], [False, False, False, True, False, False, False, False, False, False, False, False]],
         [
          [
           True, False, False, False, False, False, False, True, False, False, False, False], [False, False, False, False, False, False, False, False, False, True, False, False]],
         [
          [
           False, False, False, False, True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False, False, False, False, False]],
         [
          [
           False, True, False, False, False, False, True, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, True]],
         [
          [
           False, False, True, False, False, True, False, False, False, False, False, False], [False, False, False, False, False, True, False, False, False, False, False, False]],
         [
          [
           False, False, False, True, False, False, False, False, False, False, False, False], [False, True, False, False, False, False, False, False, False, False, False, False]]]
        self.def_dignities = copy.deepcopy(self.dignities)
        self.seltrip = 0
        self.def_seltrip = self.seltrip
        self.trips = [
         [
          [
           3, 1, 0],
          [
           0, 5, 1],
          [
           4, 2, 6],
          [
           4, 6, 2]],
         [
          [
           3, 1, 7],
          [
           0, 5, 7],
          [
           2, 2, 7],
          [
           4, 6, 7]],
         [
          [
           3, 2, 1],
          [
           0, 4, 5],
          [
           1, 6, 2],
          [
           5, 0, 4]]]
        self.def_trips = copy.deepcopy(self.trips)
        self.selterm = 0
        self.def_selterm = self.selterm
        self.terms = [
         [
          [
           [
            1, 6], [4, 6], [5, 8], [2, 5], [0, 5]],
          [
           [
            4, 8], [5, 6], [1, 8], [0, 5], [2, 3]],
          [
           [
            5, 6], [1, 6], [4, 5], [2, 7], [0, 6]],
          [
           [
            2, 7], [4, 6], [5, 6], [1, 7], [0, 4]],
          [
           [
            1, 6], [4, 5], [0, 7], [5, 6], [2, 6]],
          [
           [
            5, 7], [4, 10], [1, 4], [2, 7], [0, 2]],
          [
           [
            0, 6], [5, 8], [1, 7], [4, 7], [2, 2]],
          [
           [
            2, 7], [4, 4], [5, 8], [1, 5], [0, 6]],
          [
           [
            1, 12], [4, 5], [5, 4], [0, 5], [2, 4]],
          [
           [
            5, 7], [1, 7], [4, 8], [0, 4], [2, 4]],
          [
           [
            5, 7], [4, 6], [1, 7], [2, 5], [0, 5]],
          [
           [
            4, 12], [1, 4], [5, 3], [2, 9], [0, 2]]],
         [
          [
           [
            1, 6], [4, 8], [5, 7], [2, 5], [0, 4]],
          [
           [
            4, 8], [5, 7], [1, 7], [0, 2], [2, 6]],
          [
           [
            5, 7], [1, 6], [4, 7], [2, 6], [0, 4]],
          [
           [
            2, 6], [1, 7], [5, 7], [4, 7], [0, 3]],
          [
           [
            1, 6], [5, 7], [0, 6], [4, 6], [2, 5]],
          [
           [
            5, 7], [4, 6], [1, 5], [0, 6], [2, 6]],
          [
           [
            0, 6], [4, 5], [5, 5], [1, 8], [2, 6]],
          [
           [
            2, 6], [4, 7], [1, 8], [5, 6], [0, 3]],
          [
           [
            1, 8], [4, 6], [5, 5], [0, 6], [2, 5]],
          [
           [
            4, 6], [5, 6], [1, 7], [0, 6], [2, 5]],
          [
           [
            0, 6], [5, 6], [4, 8], [1, 5], [2, 5]],
          [
           [
            4, 8], [1, 6], [5, 6], [2, 5], [0, 5]]]]
        self.def_terms = copy.deepcopy(self.terms)
        self.seldecan = 0
        self.def_seldecan = self.seldecan
        self.decans = [
         [
          [
           2, 3, 4],
          [
           5, 6, 0],
          [
           1, 2, 3],
          [
           4, 5, 6],
          [
           0, 1, 2],
          [
           3, 4, 5],
          [
           6, 0, 1],
          [
           2, 3, 4],
          [
           5, 6, 0],
          [
           1, 2, 3],
          [
           4, 5, 6],
          [
           0, 1, 2]],
         [
          [
           2, 3, 1],
          [
           4, 5, 0],
          [
           5, 4, 0],
          [
           6, 2, 1],
          [
           3, 1, 2],
          [
           5, 0, 4],
          [
           4, 0, 5],
          [
           2, 1, 6],
          [
           1, 2, 3],
          [
           0, 4, 5],
          [
           0, 5, 4],
          [
           1, 6, 2]]]
        self.def_decans = copy.deepcopy(self.decans)
        self.def_oneruler = self.oneruler = True
        self.def_usedaynightorb = self.usedaynightorb = False
        self.def_dignityscores = self.dignityscores = [5, 4, 3, 2, 1]
        self.def_useaccidental = self.useaccidental = True
        self.def_housescores = self.housescores = [12, 6, 3, 9, 7, 1, 10, 5, 4, 11, 8, 2]
        self.def_sunphases = self.sunphases = [3, 2, 1]
        self.def_dayhourscores = self.dayhourscores = [7, 6]
        self.def_useexaltationmercury = self.useexaltationmercury = False
        self.def_topicals = self.topicals = None
        self.def_lotsref = self.lotsref = 0
        self.def_lots = self.lots = [[mtexts.txtslots['LotOfFortune'], (lots.Lots.ASC, lots.Lots.MOON, lots.Lots.SUN), (0, 0, 0), True, 0.0, [[-1, 0], [-1, 0], [-1, 0]]]]
        self.lotsvisible = [True]
        self.def_lotsvisible = self.lotsvisible[:]
        self.def_lotsusehouses = self.lotsusehouses = False
        self.def_ayanamsha = self.ayanamsha = 0
        self.def_clrframe = self.clrframe = (0, 0, 0)
        self.def_clrsigns = self.clrsigns = (0, 0, 0)
        self.def_clrAscMC = self.clrAscMC = (0, 128, 192)
        self.def_clrhouses = self.clrhouses = (0, 0, 0)
        self.def_clrhousenumbers = self.clrhousenumbers = (0, 0, 0)
        self.def_clraux = self.clraux = (0, 0, 128)
        self.clraspect = [
         (213, 0, 0), (62, 133, 198), (213, 0, 0), (0, 128, 0), (213, 0, 0)]
        self.def_clraspect = self.clraspect[:]
        self.clrplanets = [
         (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        self.def_clrplanets = self.clrplanets[:]
        self.clrLoF = self.def_clrLoF = (0, 128, 192)
        self.def_clrbackground = self.clrbackground = (255, 255, 255)
        self.def_clrtable = self.clrtable = (0, 0, 0)
        self.def_clrtexts = self.clrtexts = (0, 0, 0)
        self.def_hsys = self.hsys = 0
        self.def_meannode = self.meannode = True
        self.orbs = [
         9.0, 10.0, 7.0, 15.0, 7.0, 7.0, 12.0, 0.0, 0.0]
        self.def_orbs = self.orbs[:]
        self.orbsplanetspar = [
         1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0]
        self.def_orbsplanetspar = self.orbsplanetspar[:]
        self.def_orbscuspAscMC = self.orbscuspAscMC = 5.0
        self.def_orbscuspH = self.orbscuspH = 3.0
        self.def_daynightorb = self.daynightorb = 0.0
        self.def_primarydir = self.primarydir = 0
        self.def_subprimarydir = self.subprimarydir = 0
        self.def_subzodiacal = self.subzodiacal = 0
        self.def_bianchini = self.bianchini = False
        self.sigascmc = [
         True, True]
        self.def_sigascmc = self.sigascmc[:]
        self.sighouses = False
        self.def_sighouses = self.sighouses
        self.sigplanets = [
         True, True, True, True, True, True, True, True, True, True, True, True]
        self.def_sigplanets = self.sigplanets[:]
        self.promplanets = [True, True, True, True, True, True, True, True, True, True, True, True]
        self.def_promplanets = self.promplanets[:]
        self.pdaspects = [
         True, True, True, True, True]
        self.def_pdaspects = self.pdaspects[:]
        self.pdmidpoints = False
        self.def_pdmidpoints = self.pdmidpoints
        self.pdparallels = [
         False, False]
        self.def_pdparallels = self.pdparallels[:]
        self.pdsecmotion = self.def_pdsecmotion = False
        self.pdsecmotioniter = self.def_pdsecmotioniter = 2
        self.zodpromsigasps = [
         True, False]
        self.def_zodpromsigasps = self.zodpromsigasps[:]
        self.ascmchcsasproms = False
        self.def_ascmchcsasproms = self.ascmchcsasproms
        self.pdfixedstars = False
        self.def_pdfixedstars = self.pdfixedstars
        self.pdfixedstarssel = [
         False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        self.def_pdfixedstarssel = self.pdfixedstarssel[:]
        self.pdlof = [
         False, False]
        self.def_pdlof = self.pdlof[:]
        self.pdsyzygy = self.def_pdsyzygy = False
        self.pdterms = False
        self.def_pdterms = self.pdterms
        self.pdantiscia = False
        self.def_pdantiscia = self.pdantiscia
        self.def_pduser = self.pduser = False
        self.pduserlon = [0, 0, 0]
        self.def_pduserlon = self.pduserlon[:]
        self.pduserlat = [0, 0, 0]
        self.def_pduserlat = self.pduserlat[:]
        self.def_pdusersouthern = self.pdusersouthern = False
        self.def_pduser2 = self.pduser2 = False
        self.pduser2lon = [0, 0, 0]
        self.def_pduser2lon = self.pduser2lon[:]
        self.pduser2lat = [0, 0, 0]
        self.def_pduser2lat = self.pduser2lat[:]
        self.def_pduser2southern = self.pduser2southern = False
        self.pdkeydyn = False
        self.def_pdkeydyn = self.pdkeydyn
        self.pdkeyd = 0
        self.def_pdkeyd = self.pdkeyd
        self.pdkeys = 0
        self.def_pdkeys = self.pdkeys
        self.pdkeydeg = 0
        self.def_pdkeydeg = self.pdkeydeg
        self.pdkeymin = 0
        self.def_pdkeymin = self.pdkeymin
        self.pdkeysec = 0
        self.def_pdkeysec = self.pdkeysec
        self.useregressive = False
        self.def_useregressive = self.useregressive
        self.def_pdincharttyp = self.pdincharttyp = 0
        self.def_pdinchartsecmotion = self.pdinchartsecmotion = False
        self.def_syzmoon = self.syzmoon = 0
        self.fixedstars = {'etTau': 3.0, 'alTau': 3.0, 'bePer': 3.0, 'ga-1And': 3.0, 'alSco': 3.0, 'alBoo': 3.0, 'deCnc': 3.0, 'gaCnc': 3.0, 'etUMa': 3.0, 'alOri': 3.0, 'alCen': 3.0, 'alCar': 3.0, 'alGem': 3.0, 'beLeo': 3.0, 'alPsA': 3.0, 'alCrB': 3.0, 'alPeg': 3.0, 'beAnd': 3.0, 'alUMi': 3.0, 'beGem': 3.0, 'M44': 3.0, 'alCMi': 3.0, 'alLeo': 3.0, 'beOri': 3.0, 'alCMa': 3.0, 'alVir': 3.0, 'alSer': 3.0, 'alLyr': 3.0, 'al-2Lib': 3.0, 'beLib': 3.0}
        self.def_fixedstars = self.fixedstars.copy()
        self.def_fixedstarsorb = self.fixedstarsorb = 3.0
        self.def_zodprof = self.zodprof = True
        self.def_usezodprojsprof = self.usezodprojsprof = False
        self.def_isfirbonatti = self.isfirbonatti = True
        self.def_deflocname = self.deflocname = ''
        self.def_deflocplus = self.deflocplus = True
        self.def_defloczhour = self.defloczhour = 0
        self.def_defloczminute = self.defloczminute = 0
        self.def_deflocdst = self.deflocdst = False
        self.def_defloclondeg = self.defloclondeg = 0
        self.def_defloclonmin = self.defloclonmin = 0
        self.def_defloclatdeg = self.defloclatdeg = 0
        self.def_defloclatmin = self.defloclatmin = 0
        self.def_defloceast = self.defloceast = True
        self.def_deflocnorth = self.deflocnorth = True
        self.def_deflocalt = self.deflocalt = 0
        self.menusels = [
         [
          True, True, True, True, True, True, True, True, True, True, True],
         [
          True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
         [
          True, True, True, True, True, True, True, True, True, True],
         [
          True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
         [
          True, True]]
        self.def_menusels = copy.deepcopy(self.menusels)
        self.def_langid = self.langid = 0
        self.autosave = False
        self.def_autosave = self.autosave
        self.optionsfilestxt = ('appearance1.opt', 'appearance2.opt', 'dignities.opt',
                                'triplicities.opt', 'terms.opt', 'decans.opt', 'almutenchart.opt',
                                'almutentopicalandlots.opt', 'ayanamsa.opt', 'colors.opt',
                                'housesystem.opt', 'nodes.opt', 'orbs.opt', 'primarydirs.opt',
                                'primarykeys.opt', 'syzygy.opt', 'fixedstars.opt',
                                'profections.opt', 'firdaria.opt', 'deflocation.opt',
                                'pdsinchart.opt', 'menusel.opt', 'languages.opt',
                                'autosave.opt')
        self.optsdirtxt = 'Opts'
        self.appearance1opt = os.path.join(self.optsdirtxt, self.optionsfilestxt[0])
        self.appearance2opt = os.path.join(self.optsdirtxt, self.optionsfilestxt[1])
        self.dignitiesopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[2])
        self.triplicitiesopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[3])
        self.termsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[4])
        self.decansopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[5])
        self.chartalmutenopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[6])
        self.topicalandlotsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[7])
        self.ayanamsaopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[8])
        self.colorsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[9])
        self.housesystemopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[10])
        self.nodesopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[11])
        self.orbsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[12])
        self.primarydirsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[13])
        self.primarykeysopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[14])
        self.syzygyopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[15])
        self.fixedstarsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[16])
        self.profectionsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[17])
        self.firdariaopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[18])
        self.deflocationopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[19])
        self.pdsinchartopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[20])
        self.menuselopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[21])
        self.languagesopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[22])
        self.autosaveopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[23])
        self.load()
        return

    def reload(self):
        self.houses = self.def_houses
        self.bw = self.def_bw
        self.tablesize = self.def_tablesize
        self.showterms = self.def_showterms
        self.showdecans = self.def_showdecans
        self.showobject = self.def_showobject
        self.showfixedstarsnodes = self.def_showfixedstarsnodes
        self.showfixedstarshcs = self.def_showfixedstarshcs
        self.showfixedstarslof = self.def_showfixedstarslof
        self.showfixedstarsoutoforb = self.def_showfixedstarsoutoforb
        self.maxascmcsize = self.def_maxascmcsize
        self.housesystem = self.def_housesystem
        self.topocentric = self.def_topocentric
        self.enableclick = self.def_enableclick
        self.showdata = self.def_showdata
        self.netbook = self.def_netbook
        self.speculums = copy.deepcopy(self.def_speculums)
        self.intime = self.def_intime
        self.dignities = copy.deepcopy(self.def_dignities)
        self.seltrip = self.def_seltrip
        self.trips = copy.deepcopy(self.def_trips)
        self.selterm = self.def_selterm
        self.terms = copy.deepcopy(self.def_terms)
        self.seldecan = self.def_seldecan
        self.decans = copy.deepcopy(self.def_decans)
        self.oneruler = self.def_oneruler
        self.usedaynightorb = self.def_usedaynightorb
        self.dignityscores = self.def_dignityscores[:]
        self.useaccidental = self.def_useaccidental
        self.housescores = self.def_housescores[:]
        self.sunphases = self.def_sunphases[:]
        self.dayhourscores = self.def_dayhourscores[:]
        self.useexaltationmercury = self.def_useexaltationmercury
        if self.topicals != None:
            del self.topicals
        self.topicals = self.def_topicals
        self.lotsref = self.def_lotsref
        if self.lots != None:
            del self.lots
        self.lots = copy.deepcopy(self.def_lots)
        if self.lotsvisible != None:
            del self.lotsvisible
        self.lotsvisible = self.def_lotsvisible[:]
        self.lotsusehouses = self.def_lotsusehouses
        self.ayanamsha = self.def_ayanamsha
        self.clrframe = self.def_clrframe
        self.clrsigns = self.def_clrsigns
        self.clrAscMC = self.def_clrAscMC
        self.clrhouses = self.def_clrhouses
        self.clrhousenumbers = self.def_clrhousenumbers
        self.clraux = self.def_clraux
        self.clraspect = self.def_clraspect
        self.clrplanets = self.def_clrplanets[:]
        self.clrLoF = self.def_clrLoF
        self.clrbackground = self.def_clrbackground
        self.clrtable = self.def_clrtable
        self.clrtexts = self.def_clrtexts
        self.hsys = self.def_hsys
        self.meannode = self.def_meannode
        self.orbs = self.def_orbs[:]
        self.orbsplanetspar = self.def_orbsplanetspar
        self.orbscuspAscMC = self.def_orbscuspAscMC
        self.orbscuspH = self.def_orbscuspH
        self.daynightorb = self.def_daynightorb
        self.primarydir = self.def_primarydir
        self.subprimarydir = self.def_subprimarydir
        self.subzodiacal = self.def_subzodiacal
        self.bianchini = self.def_bianchini
        self.sigascmc = self.def_sigascmc[:]
        self.sighouses = self.def_sighouses
        self.sigplanets = self.def_sigplanets[:]
        self.promplanets = self.def_promplanets[:]
        self.pdaspects = self.def_pdaspects[:]
        self.pdmidpoints = self.def_pdmidpoints
        self.pdparallels = self.def_pdparallels[:]
        self.pdsecmotion = self.def_pdsecmotion
        self.pdsecmotioniter = self.def_pdsecmotioniter
        self.zodpromsigasps = self.def_zodpromsigasps[:]
        self.ascmchcsasproms = self.def_ascmchcsasproms
        self.pdfixedstars = self.def_pdfixedstars
        del self.pdfixedstarssel[:]
        self.pdfixedstarssel = self.def_pdfixedstarssel[:]
        self.pdlof = self.def_pdlof[:]
        self.pdsyzygy = self.def_pdsyzygy
        self.pdterms = self.def_pdterms
        self.pdantiscia = self.def_pdantiscia
        self.pduser = self.def_pduser
        self.pduserlon = self.def_pduserlon
        self.pduserlat = self.def_pduserlat
        self.pdusersouthern = self.def_pdusersouthern
        self.pduser2 = self.def_pduser2
        self.pduser2lon = self.def_pduser2lon
        self.pduser2lat = self.def_pduser2lat
        self.pduser2southern = self.def_pduser2southern
        self.pdkeydyn = self.def_pdkeydyn
        self.pdkeyd = self.def_pdkeyd
        self.pdkeys = self.def_pdkeys
        self.pdkeydeg = self.def_pdkeydeg
        self.pdkeymin = self.def_pdkeymin
        self.pdkeysec = self.def_pdkeysec
        self.useregressive = self.def_useregressive
        self.pdincharttyp = self.def_pdincharttyp
        self.pdinchartsecmotion = self.def_pdinchartsecmotion
        self.syzmoon = self.def_syzmoon
        self.fixedstars.clear()
        self.fixedstars = self.def_fixedstars.copy()
        self.fixedstarsorb = self.def_fixedstarsorb
        self.zodprof = self.def_zodprof
        self.usezodprojsprof = self.def_usezodprojsprof
        self.isfirbonatti = self.def_isfirbonatti
        self.deflocname = self.def_deflocname
        self.deflocplus = self.def_deflocplus
        self.defloczhour = self.def_defloczhour
        self.defloczminute = self.def_defloczminute
        self.deflocdst = self.def_deflocdst
        self.defloclondeg = self.def_defloclondeg
        self.defloclonmin = self.def_defloclonmin
        self.defloclatdeg = self.def_defloclatdeg
        self.defloclatmin = self.def_defloclatmin
        self.defloceast = self.def_defloceast
        self.deflocnorth = self.def_deflocnorth
        self.deflocalt = self.def_deflocalt
        self.menusels = copy.deepcopy(self.def_menusels)
        self.langid = self.def_langid
        self.autosave = self.def_autosave
        return

    def load(self):
        res = True
        try:
            optfile = self.appearance1opt
            f = open(optfile, 'rb')
            self.houses = pickle.load(f, encoding='utf-8')
            self.bw = pickle.load(f, encoding='utf-8')
            self.tablesize = pickle.load(f, encoding='utf-8')
            self.showterms = pickle.load(f, encoding='utf-8')
            self.showdecans = pickle.load(f, encoding='utf-8')
            self.showobject = pickle.load(f, encoding='utf-8')
            self.showfixedstarsnodes = pickle.load(f, encoding='utf-8')
            self.showfixedstarshcs = pickle.load(f, encoding='utf-8')
            self.showfixedstarslof = pickle.load(f, encoding='utf-8')
            self.showfixedstarsoutoforb = pickle.load(f, encoding='utf-8')
            self.maxascmcsize = pickle.load(f, encoding='utf-8')
            self.housesystem = pickle.load(f, encoding='utf-8')
            self.topocentric = pickle.load(f, encoding='utf-8')
            self.enableclick = pickle.load(f, encoding='utf-8')
            self.showdata = pickle.load(f, encoding='utf-8')
            self.netbook = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.appearance2opt
            f = open(optfile, 'rb')
            self.speculums = pickle.load(f, encoding='utf-8')
            self.intime = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.dignitiesopt
            f = open(optfile, 'rb')
            self.dignities = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.triplicitiesopt
            f = open(optfile, 'rb')
            self.seltrip = pickle.load(f, encoding='utf-8')
            self.trips = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.termsopt
            f = open(optfile, 'rb')
            self.selterm = pickle.load(f, encoding='utf-8')
            self.terms = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.decansopt
            f = open(optfile, 'rb')
            self.seldecan = pickle.load(f, encoding='utf-8')
            self.decans = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.chartalmutenopt
            f = open(optfile, 'rb')
            self.oneruler = pickle.load(f, encoding='utf-8')
            self.usedaynightorb = pickle.load(f, encoding='utf-8')
            self.dignityscores = pickle.load(f, encoding='utf-8')
            self.useaccidental = pickle.load(f, encoding='utf-8')
            self.housescores = pickle.load(f, encoding='utf-8')
            self.sunphases = pickle.load(f, encoding='utf-8')
            self.dayhourscores = pickle.load(f, encoding='utf-8')
            self.useexaltationmercury = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.topicalandlotsopt
            f = open(optfile, 'rb')
            self.topicals = pickle.load(f, encoding='utf-8')
            self.lots = pickle.load(f, encoding='utf-8')
            self.lotsref = pickle.load(f, encoding='utf-8')
            self.lotsvisible = pickle.load(f, encoding='utf-8')
            self.lotsusehouses = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.ayanamsaopt
            f = open(optfile, 'rb')
            self.ayanamsha = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.colorsopt
            f = open(optfile, 'rb')
            self.clrframe = pickle.load(f, encoding='utf-8')
            self.clrsigns = pickle.load(f, encoding='utf-8')
            self.clrAscMC = pickle.load(f, encoding='utf-8')
            self.clrhouses = pickle.load(f, encoding='utf-8')
            self.clrhousenumbers = pickle.load(f, encoding='utf-8')
            self.clraux = pickle.load(f, encoding='utf-8')
            self.clraspect = pickle.load(f, encoding='utf-8')
            self.clrplanets = pickle.load(f, encoding='utf-8')
            self.clrLoF = pickle.load(f, encoding='utf-8')
            self.clrbackground = pickle.load(f, encoding='utf-8')
            self.clrtable = pickle.load(f, encoding='utf-8')
            self.clrtexts = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.housesystemopt
            f = open(optfile, 'rb')
            self.hsys = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.nodesopt
            f = open(optfile, 'rb')
            self.meannode = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.orbsopt
            f = open(optfile, 'rb')
            self.orbs = pickle.load(f, encoding='utf-8')
            self.orbsplanetspar = pickle.load(f, encoding='utf-8')
            self.orbscuspAscMC = pickle.load(f, encoding='utf-8')
            self.orbscuspH = pickle.load(f, encoding='utf-8')
            self.daynightorb = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.primarydirsopt
            f = open(optfile, 'rb')
            self.primarydir = pickle.load(f, encoding='utf-8')
            self.subprimarydir = pickle.load(f, encoding='utf-8')
            self.subzodiacal = pickle.load(f, encoding='utf-8')
            self.bianchini = pickle.load(f, encoding='utf-8')
            self.zodpromsigasps = pickle.load(f, encoding='utf-8')
            self.ascmchcsasproms = pickle.load(f, encoding='utf-8')
            self.pdfixedstars = pickle.load(f, encoding='utf-8')
            self.pdfixedstarssel = pickle.load(f, encoding='utf-8')
            self.pdlof = pickle.load(f, encoding='utf-8')
            self.pdsyzygy = pickle.load(f, encoding='utf-8')
            self.pdterms = pickle.load(f, encoding='utf-8')
            self.pdantiscia = pickle.load(f, encoding='utf-8')
            self.pduser = pickle.load(f, encoding='utf-8')
            self.pduserlon = pickle.load(f, encoding='utf-8')
            self.pduserlat = pickle.load(f, encoding='utf-8')
            self.pdusersouthern = pickle.load(f, encoding='utf-8')
            self.pduser2 = pickle.load(f, encoding='utf-8')
            self.pduser2lon = pickle.load(f, encoding='utf-8')
            self.pduser2lat = pickle.load(f, encoding='utf-8')
            self.pduser2southern = pickle.load(f, encoding='utf-8')
            self.sigascmc = pickle.load(f, encoding='utf-8')
            self.sighouses = pickle.load(f, encoding='utf-8')
            self.sigplanets = pickle.load(f, encoding='utf-8')
            self.promplanets = pickle.load(f, encoding='utf-8')
            self.pdaspects = pickle.load(f, encoding='utf-8')
            self.pdmidpoints = pickle.load(f, encoding='utf-8')
            self.pdparallels = pickle.load(f, encoding='utf-8')
            self.pdsecmotion = pickle.load(f, encoding='utf-8')
            self.pdsecmotioniter = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.primarykeysopt
            f = open(optfile, 'rb')
            self.pdkeydyn = pickle.load(f, encoding='utf-8')
            self.pdkeyd = pickle.load(f, encoding='utf-8')
            self.pdkeys = pickle.load(f, encoding='utf-8')
            self.pdkeydeg = pickle.load(f, encoding='utf-8')
            self.pdkeymin = pickle.load(f, encoding='utf-8')
            self.pdkeysec = pickle.load(f, encoding='utf-8')
            self.useregressive = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.syzygyopt
            f = open(optfile, 'rb')
            self.syzmoon = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.fixedstarsopt
            f = open(optfile, 'rb')
            self.fixedstars = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.profectionsopt
            f = open(optfile, 'rb')
            self.zodprof = pickle.load(f, encoding='utf-8')
            self.usezodprojsprof = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.firdariaopt
            f = open(optfile, 'rb')
            self.isfirbonatti = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.deflocationopt
            f = open(optfile, 'rb')
            self.deflocname = pickle.load(f, encoding='utf-8')
            self.deflocplus = pickle.load(f, encoding='utf-8')
            self.defloczhour = pickle.load(f, encoding='utf-8')
            self.defloczminute = pickle.load(f, encoding='utf-8')
            self.deflocdst = pickle.load(f, encoding='utf-8')
            self.defloclondeg = pickle.load(f, encoding='utf-8')
            self.defloclonmin = pickle.load(f, encoding='utf-8')
            self.defloclatdeg = pickle.load(f, encoding='utf-8')
            self.defloclatmin = pickle.load(f, encoding='utf-8')
            self.defloceast = pickle.load(f, encoding='utf-8')
            self.deflocnorth = pickle.load(f, encoding='utf-8')
            self.deflocalt = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.pdsinchartopt
            f = open(optfile, 'rb')
            self.pdincharttyp = pickle.load(f, encoding='utf-8')
            self.pdinchartsecmotion = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.menuselopt
            f = open(optfile, 'rb')
            self.menusels = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.languagesopt
            f = open(optfile, 'rb')
            self.langid = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.autosaveopt
            f = open(optfile, 'rb')
            self.autosave = pickle.load(f, encoding='utf-8')
            f.close()
        except IOError:
            res = False

        return res

    def saveAppearance1(self):
        try:
            optfile = self.appearance1opt
            f = open(optfile, 'wb')
            pickle.dump(self.houses, f, 2)
            pickle.dump(self.bw, f, 2)
            pickle.dump(self.tablesize, f, 2)
            pickle.dump(self.showterms, f, 2)
            pickle.dump(self.showdecans, f, 2)
            pickle.dump(self.showobject, f, 2)
            pickle.dump(self.showfixedstarsnodes, f, 2)
            pickle.dump(self.showfixedstarshcs, f, 2)
            pickle.dump(self.showfixedstarslof, f, 2)
            pickle.dump(self.showfixedstarsoutoforb, f, 2)
            pickle.dump(self.maxascmcsize, f, 2)
            pickle.dump(self.housesystem, f, 2)
            pickle.dump(self.topocentric, f, 2)
            pickle.dump(self.enableclick, f, 2)
            pickle.dump(self.showdata, f, 2)
            pickle.dump(self.netbook, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveAppearance2(self):
        try:
            optfile = self.appearance2opt
            f = open(optfile, 'wb')
            pickle.dump(self.speculums, f, 2)
            pickle.dump(self.intime, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveDignities(self):
        try:
            optfile = self.dignitiesopt
            f = open(optfile, 'wb')
            pickle.dump(self.dignities, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveTriplicities(self):
        try:
            optfile = self.triplicitiesopt
            f = open(optfile, 'wb')
            pickle.dump(self.seltrip, f, 2)
            pickle.dump(self.trips, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveTerms(self):
        try:
            optfile = self.termsopt
            f = open(optfile, 'wb')
            pickle.dump(self.selterm, f, 2)
            pickle.dump(self.terms, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveDecans(self):
        try:
            optfile = self.decansopt
            f = open(optfile, 'wb')
            pickle.dump(self.seldecan, f, 2)
            pickle.dump(self.decans, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveChartAlmuten(self):
        try:
            optfile = self.chartalmutenopt
            f = open(optfile, 'wb')
            pickle.dump(self.oneruler, f, 2)
            pickle.dump(self.usedaynightorb, f, 2)
            pickle.dump(self.dignityscores, f, 2)
            pickle.dump(self.useaccidental, f, 2)
            pickle.dump(self.housescores, f, 2)
            pickle.dump(self.sunphases, f, 2)
            pickle.dump(self.dayhourscores, f, 2)
            pickle.dump(self.useexaltationmercury, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveTopicalandLots(self):
        try:
            optfile = self.topicalandlotsopt
            f = open(optfile, 'wb')
            pickle.dump(self.topicals, f, 2)
            pickle.dump(self.lots, f, 2)
            pickle.dump(self.lotsref, f, 2)
            pickle.dump(self.lotsvisible, f, 2)
            pickle.dump(self.lotsusehouses, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveAyanamsa(self):
        try:
            optfile = self.ayanamsaopt
            f = open(optfile, 'wb')
            pickle.dump(self.ayanamsha, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveColors(self):
        try:
            optfile = self.colorsopt
            f = open(optfile, 'wb')
            pickle.dump(self.clrframe, f, 2)
            pickle.dump(self.clrsigns, f, 2)
            pickle.dump(self.clrAscMC, f, 2)
            pickle.dump(self.clrhouses, f, 2)
            pickle.dump(self.clrhousenumbers, f, 2)
            pickle.dump(self.clraux, f, 2)
            pickle.dump(self.clraspect, f, 2)
            pickle.dump(self.clrplanets, f, 2)
            pickle.dump(self.clrLoF, f, 2)
            pickle.dump(self.clrbackground, f, 2)
            pickle.dump(self.clrtable, f, 2)
            pickle.dump(self.clrtexts, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveHouseSystem(self):
        try:
            optfile = self.housesystemopt
            f = open(optfile, 'wb')
            pickle.dump(self.hsys, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveNodes(self):
        try:
            optfile = self.nodesopt
            f = open(optfile, 'wb')
            pickle.dump(self.meannode, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveOrbs(self):
        try:
            optfile = self.orbsopt
            f = open(optfile, 'wb')
            pickle.dump(self.orbs, f, 2)
            pickle.dump(self.orbsplanetspar, f, 2)
            pickle.dump(self.orbscuspAscMC, f, 2)
            pickle.dump(self.orbscuspH, f, 2)
            pickle.dump(self.daynightorb, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def savePrimaryDirs(self):
        try:
            optfile = self.primarydirsopt
            f = open(optfile, 'wb')
            pickle.dump(self.primarydir, f, 2)
            pickle.dump(self.subprimarydir, f, 2)
            pickle.dump(self.subzodiacal, f, 2)
            pickle.dump(self.bianchini, f, 2)
            pickle.dump(self.zodpromsigasps, f, 2)
            pickle.dump(self.ascmchcsasproms, f, 2)
            pickle.dump(self.pdfixedstars, f, 2)
            pickle.dump(self.pdfixedstarssel, f, 2)
            pickle.dump(self.pdlof, f, 2)
            pickle.dump(self.pdsyzygy, f, 2)
            pickle.dump(self.pdterms, f, 2)
            pickle.dump(self.pdantiscia, f, 2)
            pickle.dump(self.pduser, f, 2)
            pickle.dump(self.pduserlon, f, 2)
            pickle.dump(self.pduserlat, f, 2)
            pickle.dump(self.pdusersouthern, f, 2)
            pickle.dump(self.pduser2, f, 2)
            pickle.dump(self.pduser2lon, f, 2)
            pickle.dump(self.pduser2lat, f, 2)
            pickle.dump(self.pduser2southern, f, 2)
            pickle.dump(self.sigascmc, f, 2)
            pickle.dump(self.sighouses, f, 2)
            pickle.dump(self.sigplanets, f, 2)
            pickle.dump(self.promplanets, f, 2)
            pickle.dump(self.pdaspects, f, 2)
            pickle.dump(self.pdmidpoints, f, 2)
            pickle.dump(self.pdparallels, f, 2)
            pickle.dump(self.pdsecmotion, f, 2)
            pickle.dump(self.pdsecmotioniter, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def savePrimaryKeys(self):
        try:
            optfile = self.primarykeysopt
            f = open(optfile, 'wb')
            pickle.dump(self.pdkeydyn, f, 2)
            pickle.dump(self.pdkeyd, f, 2)
            pickle.dump(self.pdkeys, f, 2)
            pickle.dump(self.pdkeydeg, f, 2)
            pickle.dump(self.pdkeymin, f, 2)
            pickle.dump(self.pdkeysec, f, 2)
            pickle.dump(self.useregressive, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveSyzygy(self):
        try:
            optfile = self.syzygyopt
            f = open(optfile, 'wb')
            pickle.dump(self.syzmoon, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveFixedstars(self):
        try:
            optfile = self.fixedstarsopt
            f = open(optfile, 'wb')
            pickle.dump(self.fixedstars, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveProfections(self):
        try:
            optfile = self.profectionsopt
            f = open(optfile, 'wb')
            pickle.dump(self.zodprof, f, 2)
            pickle.dump(self.usezodprojsprof, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveFirdaria(self):
        try:
            optfile = self.firdariaopt
            f = open(optfile, 'wb')
            pickle.dump(self.isfirbonatti, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveDefLocation(self):
        try:
            optfile = self.deflocationopt
            f = open(optfile, 'wb')
            pickle.dump(self.deflocname, f, 2)
            pickle.dump(self.deflocplus, f, 2)
            pickle.dump(self.defloczhour, f, 2)
            pickle.dump(self.defloczminute, f, 2)
            pickle.dump(self.deflocdst, f, 2)
            pickle.dump(self.defloclondeg, f, 2)
            pickle.dump(self.defloclonmin, f, 2)
            pickle.dump(self.defloclatdeg, f, 2)
            pickle.dump(self.defloclatmin, f, 2)
            pickle.dump(self.defloceast, f, 2)
            pickle.dump(self.deflocnorth, f, 2)
            pickle.dump(self.deflocalt, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def savePDsInChart(self):
        try:
            optfile = self.pdsinchartopt
            f = open(optfile, 'wb')
            pickle.dump(self.pdincharttyp, f, 2)
            pickle.dump(self.pdinchartsecmotion, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveMenuSel(self):
        try:
            optfile = self.menuselopt
            f = open(optfile, 'wb')
            pickle.dump(self.menusels, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveLanguages(self):
        try:
            optfile = self.languagesopt
            f = open(optfile, 'wb')
            pickle.dump(self.langid, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveAutoSave(self):
        try:
            optfile = self.autosaveopt
            f = open(optfile, 'wb')
            pickle.dump(self.autosave, f, 2)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', i18n.tr(mtexts.txtsfiles['Error']), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return res

    def save(self):
        self.saveAppearance1()
        self.saveAppearance2()
        self.saveDignities()
        self.saveTriplicities()
        self.saveTerms()
        self.saveDecans()
        self.saveChartAlmuten()
        self.saveTopicalandLots()
        self.saveAyanamsa()
        self.saveColors()
        self.saveHouseSystem()
        self.saveNodes()
        self.saveOrbs()
        self.savePrimaryDirs()
        self.savePrimaryKeys()
        self.saveSyzygy()
        self.saveFixedstars()
        self.saveProfections()
        self.saveFirdaria()
        self.saveDefLocation()
        self.savePDsInChart()
        self.saveMenuSel()
        self.saveLanguages()
        self.saveAutoSave()
        return True

    def deleteLots(self):
        if self.lots != None:
            del self.lots
        return

    def clearPDFSSel(self):
        del self.pdfixedstarssel[:]
        for i in range(len(self.fixedstars)):
            self.pdfixedstarssel.append(False)

    def checkOptsFiles(self):
        numfiles = len(self.optionsfilestxt)
        for i in range(numfiles):
            if os.path.exists(os.path.join(self.optsdirtxt, self.optionsfilestxt[i])):
                return True

        return False

    def removeOptsFiles(self):
        numfiles = len(self.optionsfilestxt)
        for i in range(numfiles):
            f = os.path.join(self.optsdirtxt, self.optionsfilestxt[i])
            if os.path.exists(f):
                os.remove(f)
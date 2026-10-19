# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import os, wx, pickle, copy, lots, mtexts

class Options:

    def __init__(self):
        self.def_houses = self.houses = True
        self.def_bw = self.bw = False
        self.def_tablesize = self.tablesize = 0.75
        self.def_showterms = self.showterms = False
        self.def_showdecans = self.showdecans = False
        self.def_showobject = self.showobject = 0
        self.def_showfixedstarsnodes = self.showfixedstarsnodes = False
        self.def_showfixedstarshcs = self.showfixedstarshcs = False
        self.def_showfixedstarslof = self.showfixedstarslof = False
        self.def_showfixedstarsoutoforb = self.showfixedstarsoutoforb = False
        self.def_maxascmcsize = self.maxascmcsize = 3
        self.def_housesystem = self.housesystem = True
        self.def_topocentric = self.topocentric = False
        self.def_enableclick = self.enableclick = True
        self.def_showdata = self.showdata = True
        self.def_netbook = self.netbook = False
        self.speculums = [
         [
          True, True, True, True, False, False, False, False, False, False, False, False, False, False], [True, True, True, True, False, False, False, False, False, False, False]]
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
        self.def_clrframe = self.clrframe = (0, 0, 255)
        self.def_clrsigns = self.clrsigns = (0, 0, 255)
        self.def_clrAscMC = self.clrAscMC = (0, 0, 0)
        self.def_clrhouses = self.clrhouses = (0, 0, 255)
        self.def_clrhousenumbers = self.clrhousenumbers = (0, 0, 255)
        self.def_clraux = self.clraux = (0, 0, 128)
        self.clraspect = [
         (0, 0, 128), (0, 128, 0), (128, 0, 0), (0, 128, 0), (128, 0, 0)]
        self.def_clraspect = self.clraspect[:]
        self.clrplanets = [
         (0, 0, 0), (0, 0, 255), (178, 34, 34), (255, 215, 0), (0, 128, 0), (138, 43, 226), (0, 191, 255), (139, 54, 38)]
        self.def_clrplanets = self.clrplanets[:]
        self.clrLoF = self.def_clrLoF = (205, 96, 144)
        self.def_clrbackground = self.clrbackground = (192, 192, 192)
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
            self.houses = pickle.load(f)
            self.bw = pickle.load(f)
            self.tablesize = pickle.load(f)
            self.showterms = pickle.load(f)
            self.showdecans = pickle.load(f)
            self.showobject = pickle.load(f)
            self.showfixedstarsnodes = pickle.load(f)
            self.showfixedstarshcs = pickle.load(f)
            self.showfixedstarslof = pickle.load(f)
            self.showfixedstarsoutoforb = pickle.load(f)
            self.maxascmcsize = pickle.load(f)
            self.housesystem = pickle.load(f)
            self.topocentric = pickle.load(f)
            self.enableclick = pickle.load(f)
            self.showdata = pickle.load(f)
            self.netbook = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.appearance2opt
            f = open(optfile, 'rb')
            self.speculums = pickle.load(f)
            self.intime = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.dignitiesopt
            f = open(optfile, 'rb')
            self.dignities = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.triplicitiesopt
            f = open(optfile, 'rb')
            self.seltrip = pickle.load(f)
            self.trips = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.termsopt
            f = open(optfile, 'rb')
            self.selterm = pickle.load(f)
            self.terms = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.decansopt
            f = open(optfile, 'rb')
            self.seldecan = pickle.load(f)
            self.decans = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.chartalmutenopt
            f = open(optfile, 'rb')
            self.oneruler = pickle.load(f)
            self.usedaynightorb = pickle.load(f)
            self.dignityscores = pickle.load(f)
            self.useaccidental = pickle.load(f)
            self.housescores = pickle.load(f)
            self.sunphases = pickle.load(f)
            self.dayhourscores = pickle.load(f)
            self.useexaltationmercury = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.topicalandlotsopt
            f = open(optfile, 'rb')
            self.topicals = pickle.load(f)
            self.lots = pickle.load(f)
            self.lotsref = pickle.load(f)
            self.lotsvisible = pickle.load(f)
            self.lotsusehouses = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.ayanamsaopt
            f = open(optfile, 'rb')
            self.ayanamsha = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.colorsopt
            f = open(optfile, 'rb')
            self.clrframe = pickle.load(f)
            self.clrsigns = pickle.load(f)
            self.clrAscMC = pickle.load(f)
            self.clrhouses = pickle.load(f)
            self.clrhousenumbers = pickle.load(f)
            self.clraux = pickle.load(f)
            self.clraspect = pickle.load(f)
            self.clrplanets = pickle.load(f)
            self.clrLoF = pickle.load(f)
            self.clrbackground = pickle.load(f)
            self.clrtable = pickle.load(f)
            self.clrtexts = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.housesystemopt
            f = open(optfile, 'rb')
            self.hsys = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.nodesopt
            f = open(optfile, 'rb')
            self.meannode = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.orbsopt
            f = open(optfile, 'rb')
            self.orbs = pickle.load(f)
            self.orbsplanetspar = pickle.load(f)
            self.orbscuspAscMC = pickle.load(f)
            self.orbscuspH = pickle.load(f)
            self.daynightorb = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.primarydirsopt
            f = open(optfile, 'rb')
            self.primarydir = pickle.load(f)
            self.subprimarydir = pickle.load(f)
            self.subzodiacal = pickle.load(f)
            self.bianchini = pickle.load(f)
            self.zodpromsigasps = pickle.load(f)
            self.ascmchcsasproms = pickle.load(f)
            self.pdfixedstars = pickle.load(f)
            self.pdfixedstarssel = pickle.load(f)
            self.pdlof = pickle.load(f)
            self.pdsyzygy = pickle.load(f)
            self.pdterms = pickle.load(f)
            self.pdantiscia = pickle.load(f)
            self.pduser = pickle.load(f)
            self.pduserlon = pickle.load(f)
            self.pduserlat = pickle.load(f)
            self.pdusersouthern = pickle.load(f)
            self.pduser2 = pickle.load(f)
            self.pduser2lon = pickle.load(f)
            self.pduser2lat = pickle.load(f)
            self.pduser2southern = pickle.load(f)
            self.sigascmc = pickle.load(f)
            self.sighouses = pickle.load(f)
            self.sigplanets = pickle.load(f)
            self.promplanets = pickle.load(f)
            self.pdaspects = pickle.load(f)
            self.pdmidpoints = pickle.load(f)
            self.pdparallels = pickle.load(f)
            self.pdsecmotion = pickle.load(f)
            self.pdsecmotioniter = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.primarykeysopt
            f = open(optfile, 'rb')
            self.pdkeydyn = pickle.load(f)
            self.pdkeyd = pickle.load(f)
            self.pdkeys = pickle.load(f)
            self.pdkeydeg = pickle.load(f)
            self.pdkeymin = pickle.load(f)
            self.pdkeysec = pickle.load(f)
            self.useregressive = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.syzygyopt
            f = open(optfile, 'rb')
            self.syzmoon = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.fixedstarsopt
            f = open(optfile, 'rb')
            self.fixedstars = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.profectionsopt
            f = open(optfile, 'rb')
            self.zodprof = pickle.load(f)
            self.usezodprojsprof = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.firdariaopt
            f = open(optfile, 'rb')
            self.isfirbonatti = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.deflocationopt
            f = open(optfile, 'rb')
            self.deflocname = pickle.load(f)
            self.deflocplus = pickle.load(f)
            self.defloczhour = pickle.load(f)
            self.defloczminute = pickle.load(f)
            self.deflocdst = pickle.load(f)
            self.defloclondeg = pickle.load(f)
            self.defloclonmin = pickle.load(f)
            self.defloclatdeg = pickle.load(f)
            self.defloclatmin = pickle.load(f)
            self.defloceast = pickle.load(f)
            self.deflocnorth = pickle.load(f)
            self.deflocalt = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.pdsinchartopt
            f = open(optfile, 'rb')
            self.pdincharttyp = pickle.load(f)
            self.pdinchartsecmotion = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.menuselopt
            f = open(optfile, 'rb')
            self.menusels = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.languagesopt
            f = open(optfile, 'rb')
            self.langid = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.autosaveopt
            f = open(optfile, 'rb')
            self.autosave = pickle.load(f)
            f.close()
        except IOError:
            res = False

        return res

    def saveAppearance1(self):
        try:
            optfile = self.appearance1opt
            f = open(optfile, 'wb')
            pickle.dump(self.houses, f)
            pickle.dump(self.bw, f)
            pickle.dump(self.tablesize, f)
            pickle.dump(self.showterms, f)
            pickle.dump(self.showdecans, f)
            pickle.dump(self.showobject, f)
            pickle.dump(self.showfixedstarsnodes, f)
            pickle.dump(self.showfixedstarshcs, f)
            pickle.dump(self.showfixedstarslof, f)
            pickle.dump(self.showfixedstarsoutoforb, f)
            pickle.dump(self.maxascmcsize, f)
            pickle.dump(self.housesystem, f)
            pickle.dump(self.topocentric, f)
            pickle.dump(self.enableclick, f)
            pickle.dump(self.showdata, f)
            pickle.dump(self.netbook, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveAppearance2(self):
        try:
            optfile = self.appearance2opt
            f = open(optfile, 'wb')
            pickle.dump(self.speculums, f)
            pickle.dump(self.intime, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveDignities(self):
        try:
            optfile = self.dignitiesopt
            f = open(optfile, 'wb')
            pickle.dump(self.dignities, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveTriplicities(self):
        try:
            optfile = self.triplicitiesopt
            f = open(optfile, 'wb')
            pickle.dump(self.seltrip, f)
            pickle.dump(self.trips, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveTerms(self):
        try:
            optfile = self.termsopt
            f = open(optfile, 'wb')
            pickle.dump(self.selterm, f)
            pickle.dump(self.terms, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveDecans(self):
        try:
            optfile = self.decansopt
            f = open(optfile, 'wb')
            pickle.dump(self.seldecan, f)
            pickle.dump(self.decans, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveChartAlmuten(self):
        try:
            optfile = self.chartalmutenopt
            f = open(optfile, 'wb')
            pickle.dump(self.oneruler, f)
            pickle.dump(self.usedaynightorb, f)
            pickle.dump(self.dignityscores, f)
            pickle.dump(self.useaccidental, f)
            pickle.dump(self.housescores, f)
            pickle.dump(self.sunphases, f)
            pickle.dump(self.dayhourscores, f)
            pickle.dump(self.useexaltationmercury, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveTopicalandLots(self):
        try:
            optfile = self.topicalandlotsopt
            f = open(optfile, 'wb')
            pickle.dump(self.topicals, f)
            pickle.dump(self.lots, f)
            pickle.dump(self.lotsref, f)
            pickle.dump(self.lotsvisible, f)
            pickle.dump(self.lotsusehouses, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveAyanamsa(self):
        try:
            optfile = self.ayanamsaopt
            f = open(optfile, 'wb')
            pickle.dump(self.ayanamsha, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveColors(self):
        try:
            optfile = self.colorsopt
            f = open(optfile, 'wb')
            pickle.dump(self.clrframe, f)
            pickle.dump(self.clrsigns, f)
            pickle.dump(self.clrAscMC, f)
            pickle.dump(self.clrhouses, f)
            pickle.dump(self.clrhousenumbers, f)
            pickle.dump(self.clraux, f)
            pickle.dump(self.clraspect, f)
            pickle.dump(self.clrplanets, f)
            pickle.dump(self.clrLoF, f)
            pickle.dump(self.clrbackground, f)
            pickle.dump(self.clrtable, f)
            pickle.dump(self.clrtexts, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveHouseSystem(self):
        try:
            optfile = self.housesystemopt
            f = open(optfile, 'wb')
            pickle.dump(self.hsys, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveNodes(self):
        try:
            optfile = self.nodesopt
            f = open(optfile, 'wb')
            pickle.dump(self.meannode, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveOrbs(self):
        try:
            optfile = self.orbsopt
            f = open(optfile, 'wb')
            pickle.dump(self.orbs, f)
            pickle.dump(self.orbsplanetspar, f)
            pickle.dump(self.orbscuspAscMC, f)
            pickle.dump(self.orbscuspH, f)
            pickle.dump(self.daynightorb, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def savePrimaryDirs(self):
        try:
            optfile = self.primarydirsopt
            f = open(optfile, 'wb')
            pickle.dump(self.primarydir, f)
            pickle.dump(self.subprimarydir, f)
            pickle.dump(self.subzodiacal, f)
            pickle.dump(self.bianchini, f)
            pickle.dump(self.zodpromsigasps, f)
            pickle.dump(self.ascmchcsasproms, f)
            pickle.dump(self.pdfixedstars, f)
            pickle.dump(self.pdfixedstarssel, f)
            pickle.dump(self.pdlof, f)
            pickle.dump(self.pdsyzygy, f)
            pickle.dump(self.pdterms, f)
            pickle.dump(self.pdantiscia, f)
            pickle.dump(self.pduser, f)
            pickle.dump(self.pduserlon, f)
            pickle.dump(self.pduserlat, f)
            pickle.dump(self.pdusersouthern, f)
            pickle.dump(self.pduser2, f)
            pickle.dump(self.pduser2lon, f)
            pickle.dump(self.pduser2lat, f)
            pickle.dump(self.pduser2southern, f)
            pickle.dump(self.sigascmc, f)
            pickle.dump(self.sighouses, f)
            pickle.dump(self.sigplanets, f)
            pickle.dump(self.promplanets, f)
            pickle.dump(self.pdaspects, f)
            pickle.dump(self.pdmidpoints, f)
            pickle.dump(self.pdparallels, f)
            pickle.dump(self.pdsecmotion, f)
            pickle.dump(self.pdsecmotioniter, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def savePrimaryKeys(self):
        try:
            optfile = self.primarykeysopt
            f = open(optfile, 'wb')
            pickle.dump(self.pdkeydyn, f)
            pickle.dump(self.pdkeyd, f)
            pickle.dump(self.pdkeys, f)
            pickle.dump(self.pdkeydeg, f)
            pickle.dump(self.pdkeymin, f)
            pickle.dump(self.pdkeysec, f)
            pickle.dump(self.useregressive, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveSyzygy(self):
        try:
            optfile = self.syzygyopt
            f = open(optfile, 'wb')
            pickle.dump(self.syzmoon, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveFixedstars(self):
        try:
            optfile = self.fixedstarsopt
            f = open(optfile, 'wb')
            pickle.dump(self.fixedstars, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveProfections(self):
        try:
            optfile = self.profectionsopt
            f = open(optfile, 'wb')
            pickle.dump(self.zodprof, f)
            pickle.dump(self.usezodprojsprof, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveFirdaria(self):
        try:
            optfile = self.firdariaopt
            f = open(optfile, 'wb')
            pickle.dump(self.isfirbonatti, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveDefLocation(self):
        try:
            optfile = self.deflocationopt
            f = open(optfile, 'wb')
            pickle.dump(self.deflocname, f)
            pickle.dump(self.deflocplus, f)
            pickle.dump(self.defloczhour, f)
            pickle.dump(self.defloczminute, f)
            pickle.dump(self.deflocdst, f)
            pickle.dump(self.defloclondeg, f)
            pickle.dump(self.defloclonmin, f)
            pickle.dump(self.defloclatdeg, f)
            pickle.dump(self.defloclatmin, f)
            pickle.dump(self.defloceast, f)
            pickle.dump(self.deflocnorth, f)
            pickle.dump(self.deflocalt, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def savePDsInChart(self):
        try:
            optfile = self.pdsinchartopt
            f = open(optfile, 'wb')
            pickle.dump(self.pdincharttyp, f)
            pickle.dump(self.pdinchartsecmotion, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveMenuSel(self):
        try:
            optfile = self.menuselopt
            f = open(optfile, 'wb')
            pickle.dump(self.menusels, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveLanguages(self):
        try:
            optfile = self.languagesopt
            f = open(optfile, 'wb')
            pickle.dump(self.langid, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return

    def saveAutoSave(self):
        try:
            optfile = self.autosaveopt
            f = open(optfile, 'wb')
            pickle.dump(self.autosave, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError'] + ' (' + optfile + ')', mtexts.txtsfiles['Error'], wx.OK | wx.ICON_EXCLAMATION)
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
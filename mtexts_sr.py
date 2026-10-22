"""Serbian (Latin script) texts of Morinus 6.2, by the names of mtexts's English
tables without 'eng' (menutxts for menutxtseng...). A key that is missing keeps
its English text: only codes and proper names are left out (roman house numbers,
GMT, Naibod...); tests/test_serbian.py checks that nothing else is.

The terms follow the glossary of the translation: Luna for the Moon as an
astrological factor (Mesec for the body in the sky), MC and IC, tačka/tačke for
lots, antiscija/antiscije, termin, aplikacioni/separacioni, solarni/lunarni povratak.
The part after a tab in menu texts is a keyboard shortcut and stays as it is."""

menutxts = {
	'MHoroscope': '&Datoteka', 'HMNew': '&Nova karta\tCtrl+N', 'HMNewDoc': 'Napravi novu kartu',
	'HMData': '&Podaci\tCtrl+D', 'HMDataDoc': 'Podaci otvorene karte', 'HMHereAndNow': '&Ovde i sada\tCtrl+H',
	'HMHereAndNowDoc': 'Karta za ovo mesto i ovaj trenutak', 'HMLoad': '&Otvori\tCtrl+L', 'HMLoadDoc': 'Otvori sačuvanu kartu',
	'HMSave': '&Sačuvaj\tCtrl+S', 'HMSaveDoc': 'Sačuvaj kartu', 'HMSaveAsBmp': 'Sačuvaj kao &sliku\tCtrl+B',
	'HMSaveAsBmpDoc': 'Sačuvaj kartu kao sliku', 'HMSynastry': 'Sin&astrija\tCtrl+Y', 'HMSynastryDoc': 'Otvori drugu kartu',
	'HMFindTime': '&Pronađi vreme\tCtrl+F', 'HMFindTimeDoc': 'Pronađi vreme i mesto po položajima planeta',
	'HMEphemeris': '&Efemeride\tCtrl+E', 'HMEphemerisDoc': 'Grafičke efemeride', 'HMClose': '&Zatvori\tCtrl+C',
	'HMCloseDoc': 'Zatvori kartu', 'HMExit': '&Izlaz\tAlt+X', 'HMExitDoc': 'Izađi iz programa',
	'MTable': '&Tabele', 'TMPositions': 'Položaji\tF1', 'TMPositionsDoc': 'Položaji planeta i kuća', 'TMAlmutens': 'Almuteni',
	'TMAlmutenZodiacal': 'Tačke\tF2', 'TMAlmutenZodiacalDoc': 'Almuteni zodijakalnih tačaka', 'TMAlmutenChart': 'Karta\tF3',
	'TMAlmutenChartDoc': 'Almuten karte', 'TMAlmutenTopical': 'Tematski\tF4', 'TMAlmutenTopicalDoc': 'Tematski almuteni',
	'TMMisc': 'Razno\tF5', 'TMMiscDoc': 'Razni podaci', 'TMMunPos': 'Mundane pozicije\tF6', 'TMMunPosDoc': 'Mundane pozicije',
	'TMAntiscia': 'Antiscije\tF7', 'TMAntisciaDoc': 'Antiscije', 'TMAspects': 'Aspekti\tF8', 'TMAspectsDoc': 'Tabela aspekata',
	'TMMidpoints': 'Središnje tačke\tF9', 'TMMidpointsDoc': 'Središnje tačke planeta', 'TMRiseSet': 'Izlasci i zalasci\tF10',
	'TMRiseSetDoc': 'Vremena izlaska i zalaska', 'TMSpeeds': 'Brzine\tF11', 'TMSpeedsDoc': 'Brzine planeta',
	'TMZodPars': 'Zodijakalne paralele\tF12', 'TMZodParsDoc': 'Zodijakalne paralele', 'TMFixStars': 'Fiksne zvezde\tCtrl+F1',
	'TMFixStarsDoc': 'Položaji fiksnih zvezda', 'TMFixStarsAsps': 'Konjunkcije fiksnih zvezda\tCtrl+F2',
	'TMFixStarsAspsDoc': 'Konjunkcije fiksnih zvezda', 'TMLots': 'Tačke\tCtrl+F3', 'TMLotsDoc': 'Tačke (lotovi)',
	'TMStrip': 'Traka od 30°\tCtrl+F4', 'TMStripDoc': 'Traka od 30 stepeni', 'TMPlanetaryHours': 'Planetarni časovi\tCtrl+F5',
	'TMPlanetaryHoursDoc': 'Planetarni časovi', 'TMExactTransits': 'Tačni tranziti\tCtrl+F6', 'TMExactTransitsDoc': 'Tranziti za zadati mesec',
	'TMProfections': 'Profekcije\tCtrl+F7', 'TMProfectionsDoc': 'Tabela profekcija', 'TMUserSpeculum': 'Spekulum korisnika\tCtrl+F8',
	'TMUserSpeculumDoc': 'Spekulum zadate ekliptičke tačke', 'TMFirdaria': 'Firdarija\tCtrl+F9', 'TMFirdariaDoc': 'Firdarija',
	'TMPrimaryDirs': 'Primarne direkcije\tCtrl+F12', 'TMPrimaryDirsDoc': 'Spisak primarnih direkcija',
	'MCharts': '&Karte', 'PMTransits': 'Tranziti\tCtrl+Shift+F1', 'PMTransitsDoc': 'Tranziti za zadati datum',
	'PMRevolutions': 'Povratci\tCtrl+Shift+F2', 'PMRevolutionsDoc': 'Izračunava povratke', 'PMSunTransits': 'Tranziti Sunca\tCtrl+Shift+F3',
	'PMSunTransitsDoc': 'Izračunava tranzite Sunca', 'PMSecondaryDirs': 'Sekundarne direkcije\tCtrl+Shift+F4',
	'PMSecondaryDirsDoc': 'Izračunava sekundarne direkcije', 'PMElections': 'Elekcije\tCtrl+Shift+F5', 'PMElectionsDoc': 'Karta za elekciju',
	'PMSquareChart': 'Kvadratna karta\tCtrl+Shift+F6', 'PMSquareChartDoc': 'Karta u kvadratnom obliku', 'PMSyzygy': 'Sizigija\tCtrl+Shift+F7',
	'PMSyzygyDoc': 'Prenatalna lunacija', 'PMSyzygy2': 'Sizigija 2\tCtrl+Shift+F8', 'PMSyzygyDoc2': 'Prenatalna lunacija druge vrste',
	'PMProfections': 'Profekcije\tCtrl+Shift+F9', 'PMProfectionsDoc': 'Karta profekcije', 'PMHelioChart': 'Heliocentrična\tCtrl+Shift+F12',
	'PMHelioChartDoc': 'Heliocentrični položaji', 'MOptions': '&Podešavanja', 'OMAppearance1': '&Izgled I\tShift+A',
	'OMAppearance1Doc': 'Podešavanja izgleda I', 'OMAppearance2': 'I&zgled II\tShift+P', 'OMAppearance2Doc': 'Podešavanja izgleda II',
	'OMDignities': '&Dostojanstva\tShift+G', 'OMDignitiesDoc': 'Podešavanja dostojanstava', 'OMMinorDignities': 'Manja dostojanstva',
	'OMTriplicities': 'T&ripliciteti\tShift+I', 'OMTriplicitiesDoc': 'Izbor triplicitetnih vladara', 'OMTerms': '&Termini\tShift+T',
	'OMTermsDoc': 'Izbor termina', 'OMDecans': 'D&ekani\tShift+N', 'OMDecansDoc': 'Izbor dekana', 'OMAlmutens': 'Almuteni',
	'OMChartAlmuten': 'Karta\tShift+E', 'OMChartAlmutenDoc': 'Almuten karte', 'OMTopical': 'Tematski\tShift+J',
	'OMTopicalDoc': 'Tematski almuteni', 'OMAyanamsha': '&Ajanamša\tShift+Y', 'OMAyanamshaDoc': 'Izbor ajanamše',
	'OMColors': '&Boje\tShift+C', 'OMColorsDoc': 'Podešavanja boja', 'OMHouseSystem': 'Sistemi kuća',
	'OMHSPlacidus': 'Plasidus\tShift+F1', 'OMHSKoch': 'Koh\tShift+F2', 'OMHSRegiomontanus': 'Regiomontanus\tShift+F3',
	'OMHSCampanus': 'Kampanus\tShift+F4', 'OMHSEqual': 'Jednake kuće\tShift+F5', 'OMHSWholeSign': 'Cele kuće (whole sign)\tShift+F6',
	'OMHSAxial': 'Aksijalni\tShift+F7', 'OMHSMorinus': 'Morinus\tShift+F8', 'OMHSHorizontal': 'Horizontalni\tShift+F9',
	'OMHSPagePolich': 'Pejdž-Poliš\tShift+F10', 'OMHSAlcabitus': 'Alkabitius\tShift+F11', 'OMHSPorphyrius': 'Porfirije\tShift+F12',
	'OMNodes': 'Čvorovi', 'OMNMean': 'Srednji\tShift+M', 'OMNTrue': 'Pravi\tShift+W', 'OMOrbs': '&Orbisi\tShift+O',
	'OMOrbsDoc': 'Podešavanja orbisa', 'OMPrimaryDirs': 'Primarne &direkcije\tShift+D', 'OMPrimaryDirsDoc': 'Podešavanja primarnih direkcija',
	'OMLots': 'Tačke\tShift+Q', 'OMLotsDoc': 'Podešavanja tačaka', 'OMSyzygy': 'Si&zigija\tShift+Z', 'OMSyzygyDoc': 'Podešavanja sizigije',
	'OMFixedStarsOpt': '&Fiksne zvezde\tShift+F', 'OMFixedStarsOptDoc': 'Izbor fiksnih zvezda', 'OMProfectionsOpt': 'Profekcije\tShift+V',
	'OMProfectionsOptDoc': 'Podešavanja profekcija', 'OMFirdariaOpt': 'Firdarija\tAlt+F', 'OMFirdariaOptDoc': 'Podešavanja firdarije',
	'OMDefLocationOpt': 'Podrazumevano mesto\tAlt+D', 'OMDefLocationOptDoc': 'Mesto za nove karte', 'OMMenuSel': 'Izbor stavki menija',
	'OMMenuSelFirst': 'Prvi deo\tCtrl+Shift+F11', 'OMMenuSelFirstDoc': 'Izbor stavki menija, prvi deo', 'OMMenuSelSecond': 'Drugi deo\tCtrl+Shift+F12',
	'OMMenuSelSecondDoc': 'Izbor stavki menija, drugi deo', 'OMLanguages': 'Jezik\tShift+X', 'OMLanguagesDoc': 'Izbor jezika',
	'OMPrimaryKeys': 'Primarni &ključevi\tShift+K', 'OMPrimaryKeysDoc': 'Ključevi primarnih direkcija', 'OMPDsInChartOpt': 'PD u karti\tShift+B',
	'OMPDsInChartOptDoc': 'Primarne direkcije u karti', 'OMAutoSave': '&Automatski čuvaj\tShift+U', 'OMAutoSaveDoc': 'Uključuje i isključuje automatsko čuvanje',
	'OMSave': '&Sačuvaj\tShift+S', 'OMSaveDoc': 'Čuva podešavanja', 'OMReload': '&Vrati podrazumevana\tShift+R',
	'OMReloadDoc': 'Vraća podrazumevana podešavanja', 'MHelp': 'P&omoć', 'HEMHelp': '&Pomoć\tShift+H', 'HEMHelpDoc': 'Pomoć',
	'HEMAbout': '&O programu\tAlt+A', 'HEMAboutDoc': 'Podaci o programu',
}

txtsfiles = {
	'DiscardCurrHor': 'Odbaciti trenutnu kartu?', 'OpenHor': 'Otvori kartu', 'HORFiles': 'Karte HOR (*.hor)|*.hor',
	'FileError': 'Greška u datoteci!', 'Error': 'Greška', 'NotFound': 'nije pronađeno', 'SaveHor': 'Sačuvaj kartu',
	'FileExists': 'Datoteka već postoji. Zameniti je?', 'Message': 'Poruka', 'Horoscope': 'Karta', 'SaveAsBmp': 'Sačuvaj kao sliku',
	'BMPFiles': 'Slike PNG (*.png)|*.png', 'Untitled': 'Bez naziva', 'SaveAsText': 'Sačuvaj kao tekst', 'TXTFiles': 'Tekst (*.txt)|*.txt',
	'SavePDs': 'Sačuvaj primarne direkcije', 'OptFileError': 'Greška u datoteci podešavanja!', 'DBFileError': 'Baza mesta ne može da se otvori!',
}

txtsgraphephemwnd = {
	'Ephemeris': 'Efemeride', 'Jan': 'jan', 'Feb': 'feb', 'Mar': 'mar', 'Apr': 'apr', 'May': 'maj', 'Jun': 'jun', 'Jul': 'jul',
	'Aug': 'avg', 'Sep': 'sep', 'Oct': 'okt', 'Nov': 'nov', 'Dec': 'dec',
}

txtspositions = {
	'Longitude': 'Dužina', 'Latitude': 'Širina', 'Rectascension': 'Rektascenzija', 'Declination': 'Deklinacija',
	'AscDiffLat': 'Asc. razlika', 'Semiarcus': 'Poluluk', 'Meridiandist': 'Meridijanska dist.', 'Horizondist': 'Horizontska dist.',
	'TemporalHour': 'Temporalni čas', 'HourlyDist': 'Časovna dist.', 'AscDiffPole': 'Asc. razlika pola', 'PoleHeight': 'Visina pola',
	'AODO': 'AO/DO (pol)', 'Pole': 'Pol', 'SelectColumn': 'Izaberite bar jednu kolonu u Podešavanja › Izgled II.',
}

txtsalmutencharttable = {
	'Essential': 'Esencijalno', 'DegreeWins': 'Pobednici stepena', 'Syzygy': 'Sizigija', 'TotalShares1': 'Ukupno', 'TotalShares2': 'udela',
	'TotalScores1': 'Ukupno', 'TotalScores2': 'poena', 'Accidental': 'Akcidentalno', 'HouseScores1': 'Poeni', 'HouseScores2': 'kuće',
	'DayRulerScores1': 'Vladar dana', 'DayRulerScores2': 'poeni', 'HourRulerScores1': 'Vladar časa', 'HourRulerScores2': 'poeni',
	'PhaseScores1': 'Faza', 'PhaseScores2': 'poeni', 'Total': 'Ukupno', 'EssentialScores1': 'Esencijalni', 'EssentialScores2': 'poeni',
	'AccidentalScores1': 'Akcidentalni', 'AccidentalScores2': 'poeni', 'GrandScores1': 'Sveukupni', 'GrandScores2': 'poeni',
}

txtsalmutentopicals = {
	'DegreeWins': 'Pobednici stepena', 'TotalShares1': 'Ukupno', 'TotalShares2': 'udela', 'TotalScores1': 'Ukupno', 'TotalScores2': 'poena',
}

txtsalmutenzods = {'Almuten': 'Almuten', 'Syzygy': 'Sizigija'}

txtsmisc = {'SidTime': 'Sideričko vreme', 'OblEcl': 'Nagib ekliptike', 'JulianDay': 'Julijanski dan'}

txtsmunpos = {'HousePercent': 'Kuća (%)', 'MLoF': 'Mundana Fortuna'}

txtsantiscia = {'Antiscion': 'Antiscija', 'Contraantiscion': 'Kontra-antiscija', 'Longitude': 'Dužina', 'Latitude': 'Širina'}

txtsmidpoints = {'Longitude': 'Dužina'}

txtsriseset = {'Rise': 'Izlazak', 'Set': 'Zalazak'}

txtsspeeds = {'InLong': 'Po dužini', 'InLat': 'Po širini'}

txtszodpars = {'ZodPars': 'Zodijakalne paralele', 'Parallel': 'Paralela', 'ContraParallel': 'Kontraparalela'}

txtsfixedstars = {
	'Name': 'Ime', 'Nomencl': 'Oznaka', 'Longitude': 'Dužina', 'Latitude': 'Širina', 'Rectascension': 'Rektascenzija', 'Declination': 'Deklinacija',
}

txtslots = {'Name': 'Ime', 'Formula': 'Formula', 'Longitude': 'Dužina', 'Almuten': 'Almuten', 'LotOfFortune': 'Fortuna'}

txtshours = {'LocalBirthTime': 'Lokalno vreme rođenja', 'RiseTime': 'Izlazak Sunca', 'SetTime': 'Zalazak Sunca'}

txtstransits = {'Transits': 'Tranziti', 'Day': 'Dan', 'Time': 'Vreme', 'Transit': 'Tranzit', 'House': 'Kuća'}

txtsprofwnd = {
	'Pro': 'Prof.', 'Age': 'Godine', 'Date': 'Datum',
	'LeftClick': 'Kliknite levim tasterom na polje godina za mesečne profekcije',
}

txtsprofmonwnd = {'Pro': 'Prof.', 'Age': 'Godine', 'Date': 'Datum'}

txtsfirdaria = {
	'Firdaria': 'Firdarija', 'Diurnal': 'Dnevna', 'Nocturnal': 'Noćna', 'AlBiruni': 'Al Biruni', 'Bonatus': 'Bonatus', 'Years': 'Godine',
}

txtsdatadlg = {
	'Data': 'Podaci', 'Long': 'Dužina', 'Lat': 'Širina', 'E': 'I', 'W': 'Z', 'N': 'S', 'S': 'J', 'Name': 'Ime',
	'HelpName': 'Ime karte ili natusa', 'Male': 'Muški', 'Female': 'Ženski', 'Gender': 'Pol', 'Type': 'Vrsta',
	'HelpType': 'Vrsta karte koja se računa', 'BC': 'p. n. e.', 'Year': 'Godina',
	'HelpYear': 'Švajcarske efemeride pokrivaju period od 5000. p. n. e. do 5000. n. e.',
	'HelpYear2': 'Mošijerove efemeride pokrivaju period od 3000. p. n. e. do 3000. n. e.', 'Month': 'Mesec',
	'HelpMonth': 'Mora biti od 1 do 12', 'HelpDay': 'Mora biti od 1 do 31', 'Day': 'Dan', 'Hour': 'Sat',
	'HelpHour': 'Mora biti od 0 do 23', 'Min': 'Min', 'HelpMin': 'Mora biti od 0 do 59', 'Sec': 'Sek', 'Deg': 'Step',
	'HelpLonDeg': 'Mora biti od 0 do 180', 'HelpLatDeg': 'Mora biti od 0 do 90', 'Place': 'Mesto', 'HelpPlace': 'Mesto karte',
	'HelpZoneHour': 'Mora biti od 0 do 12', 'HelpDaylight': 'Oduzima jedan sat', 'Daylight': 'Letnje računanje vremena',
	'PlanetaryHour': 'Planetarni čas', 'Altitude': 'Nadmorska visina', 'HelpAltitude': 'Mora biti od 0 do 10000', 'Notes': 'Beleške',
	'HelpNotes': 'Beleške o karti', 'InvalidDate': 'Neispravan datum!', 'Error': 'Greška', 'Gregorian': 'Gregorijanski',
	'Julian': 'Julijanski', 'Zone': 'Zona', 'Greenwich': 'Grinič', 'LocalMean': 'Lokalno srednje', 'LocalApparent': 'Lokalno pravo',
}

txtsfindtimedlg = {
	'FindTime': 'Pronađi vreme', 'Use': 'Koristi', 'Minute': 'Minut', 'Second': 'Sekund', 'BC': 'p. n. e.', 'D': 's', 'M': 'm', 'S': 's',
	'Retrograde': 'Retrograd', 'ApproxPlanets': 'Približnost (planete)', 'Date': 'Datum', 'Time': 'Vreme (GMT)', 'Start': 'Počni',
	'Show': 'Prikaži', 'BusyInfo': 'U zavisnosti od brzine računara ovo može da potraje.', 'Calculating': 'Računam',
	'NoChartWithSettings': 'Nema karata sa ovim podešavanjima!', 'Information': 'Obaveštenje', 'Year': 'Godina',
	'HelpDeg': 'Mora biti od 0 do 359', 'HelpMin': 'Mora biti od 0 do 59', 'HelpApproxDeg': 'Mora biti od 0 do 4',
	'InvalidAsc': 'Za Asc = 0 ili 180 geografska širina nije određena',
	'HelpYear': 'Švajcarske efemeride pokrivaju period od 5000. p. n. e. do 5000. n. e.',
	'HelpYear2': 'Mošijerove efemeride pokrivaju period od 3000. p. n. e. do 3000. n. e.',
	'HelpMonth': 'Mora biti od 1 do 12', 'HelpDay': 'Mora biti od 1 do 31', 'YE': 'G', 'MO': 'M', 'DA': 'D', 'HO': 'č',
	'HelpHour': 'Mora biti od 0 do 23', 'ForceTheDate': 'Zadaj datum (samo za traženje mesta); po GMT',
}

txtsgraphephemdlg = {
	'Ephemeris': 'Efemeride', 'Year': 'Godina',
	'HelpYear': 'Švajcarske efemeride pokrivaju period od 5000. p. n. e. do 5000. n. e.',
	'HelpYear2': 'Mošijerove efemeride pokrivaju period od 3000. p. n. e. do 3000. n. e.',
}

txtsplacesdlg = {
	'Place': 'Mesto', 'Country': 'Država', 'Long': 'Dužina', 'Lat': 'Širina', 'Zone': 'Zona', 'Alt': 'Visina', 'Places': 'Mesta',
	'Deg': 'Step', 'HelpLonDeg': 'Mora biti od 0 do 180', 'Min': 'Min', 'HelpMin': 'Mora biti od 0 do 59', 'E': 'I', 'W': 'Z',
	'N': 'S', 'S': 'J', 'HelpLatDeg': 'Mora biti od 0 do 90', 'HelpPlace': 'Mesto karte', 'Hour': 'Sat',
	'HelpZoneHour': 'Mora biti od 0 do 12', 'HelpAltitude': 'Mora biti od 0 do 10000', 'Add': 'Dodaj', 'Remove': 'Ukloni',
	'RemoveAll': 'Ukloni sve', 'Search': 'Traži',
	'NotFound': 'Nije pronađeno!\nMožda nema internet veze\nili je ime mesta pogrešno napisano',
	'PlaceEmpty': 'Polje za mesto je prazno!', 'TooFewChars': 'Upišite bar tri slova u polje za mesto.',
	'MaxNumberOnlineSearch': 'Najviše rezultata pretrage na internetu',
}

txtsappearance1dlg = {
	'Appearance1': 'Izgled I', 'InChart': 'U karti', 'Houses': 'Kuće', 'Terms': 'Termini', 'Decans': 'Dekani', 'None': 'Ništa',
	'FixedStars': 'Fiksne zvezde', 'Nodes': 'Čvorovi', 'IntermHCs': 'Međukuće', 'LoF': 'Fortuna', 'Antiscia': 'Antiscije',
	'Topocentric': 'Topocentrično', 'Color': 'Boja', 'BlackAndWhite': 'Crno-belo', 'InColor': 'U boji',
	'MaxAscMCWidth': 'Najveća debljina Asc-MC', 'TableSize': 'Veličina tabela', 'EnableClick': 'Klik na planetu',
	'ShowData': 'Prikaži podatke', 'Netbook': 'Mali ekran', 'Lots': 'Tačke', 'FSOutOrb': 'Prikaži i van orbisa',
	'Dodecatemoria': 'Dodekatemorije',
}

txtsappearance2dlg = {
	'Appearance2': 'Izgled II', 'Placidian': 'Plasidus', 'Regiomontanian': 'Regiomontanus', 'Rectascension': 'Rektascenzija',
	'InTime': 'U vremenu', 'Longitude': 'Dužina', 'Latitude': 'Širina', 'Declination': 'Deklinacija', 'AscDiffLat': 'Asc. razlika',
	'Semiarcus': 'Poluluk', 'Meridiandist': 'Meridijanska dist.', 'Horizondist': 'Horizontska dist.', 'TemporalHour': 'Temporalni čas',
	'HourlyDist': 'Časovna dist.', 'AscDiffPole': 'Asc. razlika pola', 'PoleHeight': 'Visina pola', 'AODO': 'AO/DO (pol)', 'Pole': 'Pol',
	'HelpPMP': 'Plasidusova mundana pozicija', 'HelpZD': 'Zenitna distanca', 'HelpQ': 'Ascenziona razlika pod sopstvenim polom',
	'HelpW': 'Kosa ascenzija/descenzija pod sopstvenim polom (Regiomontanova mundana pozicija)', 'HelpCMP': 'Kampanusova mundana pozicija',
}

txtsdignitiesdlg = {'Dignities': 'Dostojanstva', 'Domicile': 'Domicil', 'Exaltation': 'Egzaltacija'}

txtsdecansdlg = {'Decans': 'Dekani', 'Chaldean': 'Haldejski', 'Triplicity': 'Po triplicitetu'}

txtstriplicitiesdlg = {
	'Triplicities': 'Tripliciteti', 'Dorothean': 'Doroteje', 'Ptolemaic': 'Ptolomej', 'Morinus': 'Morinus', 'Fire': 'Vatra',
	'Earth': 'Zemlja', 'Air': 'Vazduh', 'Water': 'Voda', 'Primary': 'Prvi', 'Secondary': 'Drugi', 'Participating': 'Particip.',
}

txtstermsdlg = {
	'Terms': 'Termini',
	'NumFieldsCannotBeEmpty': 'Problem sa podacima! Brojna polja ne smeju biti prazna! Kliknite na upitnik pa na polje da vidite dozvoljene vrednosti!',
	'Error': 'Greška', 'RangeError2': 'Vrednost van opsega!', 'RangeError3': 'Vrednost van opsega! Vrednosti moraju biti manje od ',
	'MultiPlanets': 'Ista planeta je izabrana više puta', 'NOT30': 'Zbir stepeni nije jednak 30', 'Egyptian': 'Egipatski', 'Ptolemaic': 'Ptolomejevi',
}

txtssyzygydlg = {'Syzygy': 'Sizigija', 'SyzMoon': 'Luna', 'SyzAbove': 'Iznad horizonta', 'SyzAboveNatal': 'Iznad horizonta (radiks)'}

txtsfixedstarsdlg = {
	'FixedStars': 'Fiksne zvezde', 'Name': 'Ime', 'Nomencl': 'Oznaka', 'Long': 'Dužina', 'Lat': 'Širina',
	'FixedStarRef': '01.01.1950. u ponoć (GMT)', 'DeselectAll': 'Poništi sve', 'LeftToSelect': 'Preostalo', 'Search': 'Traži',
}

txtscolorsdlg = {
	'Colors': 'Boje', 'Chart': 'Karta', 'Frame': 'Okvir', 'Signs': 'Znaci', 'AscMC': 'AscMC', 'Houses': 'Kuće', 'Auxiliary': 'Pomoćne',
	'Housenames': 'Brojevi kuća', 'Positions': 'Položaji', 'Dignities': 'Dostojanstva', 'Domicile': 'Domicil', 'Exal': 'Egzal.',
	'Peregrine': 'Peregrin', 'Fall': 'Pad', 'Detriment': 'Izgnanstvo', 'Individual': 'Pojedinačne', 'General': 'Opšte',
	'Background': 'Pozadina', 'Table': 'Tabela', 'Texts': 'Tekst', 'UseIndividual': 'Pojedinačne boje', 'Planets': 'Planete',
}

txtsorbsdlg = {
	'Orbs': 'Orbisi', 'AscMC': 'Asc-MC', 'Interm': 'Međukuće', 'FixedStars': 'Fiksne zvezde', 'All': 'Sve',
	'RangeError': 'Vrednost van opsega! Vrednosti moraju biti manje od ', 'Error': 'Greška', 'PlanetsInHouse': 'Planete u kućama',
	'Parallels': 'Paralele', 'DayNight': 'Dan/noć',
}

txtsvalidators = {
	'NumFieldsCannotBeEmpty': 'Problem sa podacima! Brojna polja ne smeju biti prazna! Kliknite na upitnik pa na polje da vidite dozvoljene vrednosti!',
	'Error': 'Greška', 'RangeError': 'Vrednost van opsega! Kliknite na upitnik pa na polje da vidite dozvoljene vrednosti!',
	'FieldsCannotBeEmpty': 'Problem sa podacima! Polja ne smeju biti prazna!', 'RangeError2': 'Vrednost van opsega!',
	'RangeError3': 'Vrednost van opsega! Vrednosti moraju biti manje od ',
}

txtspopupmenu = {
	'SaveAsBmp': 'Sačuvaj kao sliku', 'SaveTable': 'Sačuvaj tabelu kao sliku', 'BlackAndWhite': 'Crno-belo', 'TableBW': 'Tabela',
	'SaveChart': 'Sačuvaj kartu kao sliku', 'ChartBW': 'Crno-bela karta', 'Chart': 'Karta', 'Comparison': 'Poređenje',
	'Positions': 'Položaji', 'Square': 'Kvadratna', 'Windows': 'Prikaz', 'PrimaryDirs': 'Primarne direkcije', 'Direct': 'Direktne',
	'Converse': 'Konverzne', 'PDRadix': 'Radiks',
}

txtssecdirdlg = {
	'SecondaryDirs': 'Sekundarne direkcije', 'Age': 'Godine', 'ApparentSolarTime': 'Pravo sunčevo vreme', 'MeanTime': 'Srednje vreme',
	'Direct': 'Direktne', 'Converse': 'Konverzne',
}

txtsstepperdlg = {'SecondaryDirs': 'Sekundarne direkcije', 'Days': 'Dani'}

txtselectionsstepperdlg = {'Elections': 'Elekcije', 'Year': 'Godina', 'Month': 'Mesec', 'Day': 'Dan', 'Hour': 'Sat', 'Min': 'Min', 'Sec': 'Sek'}

_years = {
	'HelpYear': 'Švajcarske efemeride pokrivaju period od 5000. p. n. e. do 5000. n. e.',
	'HelpYear2': 'Mošijerove efemeride pokrivaju period od 3000. p. n. e. do 3000. n. e.',
	'HelpMonth': 'Mora biti od 1 do 12', 'HelpDay': 'Mora biti od 1 do 31',
}

txtsrevolutionsdlg = dict(_years, **{
	'Revolutions': 'Povratci', 'StartingDate': 'Prvi povratak posle (ponoć, UT)', 'Year': 'Godina', 'Month': 'Mesec', 'Day': 'Dan',
	'InvalidDate': 'Neispravan datum!', 'Error': 'Greška',
})

txtssuntransitsdlg = dict(_years, **{
	'SunTransits': 'Tranziti Sunca', 'StartingDate': 'Početno vreme (ponoć, GMT)', 'Year': 'Godina', 'Month': 'Mesec', 'Day': 'Dan',
	'Ascendant': 'Ascendent', 'MediumCoeli': 'MC',
})

txtsalmutenchartdlg = {
	'AlmutenOfTheChart': 'Almuten karte', 'Essential': 'Esencijalno', 'Triplicities': 'Tripliciteti', 'OneRuler': 'Jedan vladar (dan/noć)',
	'AllThree': 'Sva tri', 'UseDayNightOrbAlmutens': 'Koristi orbis dana/noći', 'RulershipScores': 'Poeni vladanja', 'Domicile': 'Domicil',
	'Exaltation': 'Egzaltacija', 'Triplicity': 'Triplicitet', 'Term': 'Termin', 'Decan': 'Dekan', 'Day': 'Dan', 'Hour': 'Čas',
	'HelpLessThanFive': 'Mora biti od 0 do 5', 'Accidental': 'Akcidentalno', 'Use': 'Koristi', 'HouseScores': 'Poeni kuća',
	'SunPhaseScores': 'Poeni faze prema Suncu', 'Strong': 'Jaka', 'Medium': 'Srednja', 'Weak': 'Slaba', 'HelpLessThanNine': 'Mora biti od 0 do 9',
	'HelpLessThanTwelve': 'Mora biti od 0 do 12', 'RulerScores': 'Poeni vladara', 'MercuryInVirgo': 'Koristi egzaltaciju (Merkur u Devici)',
}

txtsalmutentopicalsdlg = {
	'Type': 'Vrsta', 'Value': 'Vrednost', 'Rulership': 'Vladanje', 'MaxRowNum': 'Najveći broj redova je ', 'Name': 'Ime',
	'RowAlreadyExists': 'Taj red već postoji!', 'LotOfFortune': 'Fortuna', 'TopicalAlmutens': 'Tematski almuteni', 'Almutens': 'Almuteni',
	'Add': 'Dodaj', 'Remove': 'Ukloni', 'RemoveAll': 'Ukloni sve', 'Editor': 'Uređivanje', 'HelpTopicalName': 'Ime tematskog almutena koji se dodaje',
	'AddRow': 'Dodaj red', 'RemoveRow': 'Ukloni red', 'MaxTopicalNum': 'Najveći broj tematskih almutena je ', 'NameIsEmpty': 'Polje za ime je prazno!',
	'NameAlreadyExists': 'To ime već postoji!', 'NoRowsAdded': 'Nijedan red nije dodat!', 'TopicalPlanet': 'Planeta', 'TopicalPlanets': 'Planete',
	'TopicalHousecusp': 'Vrh kuće', 'TopicalLot': 'Tačka', 'TopicalSyzygy': 'Sizigija',
	'TopicalinHouse1': 'u 1. kući', 'TopicalinHouse2': 'u 2. kući', 'TopicalinHouse3': 'u 3. kući', 'TopicalinHouse4': 'u 4. kući',
	'TopicalinHouse5': 'u 5. kući', 'TopicalinHouse6': 'u 6. kući', 'TopicalinHouse7': 'u 7. kući', 'TopicalinHouse8': 'u 8. kući',
	'TopicalinHouse9': 'u 9. kući', 'TopicalinHouse10': 'u 10. kući', 'TopicalinHouse11': 'u 11. kući', 'TopicalinHouse12': 'u 12. kući',
	'TopicalDefault': 'Podrazumevano', 'TopicalConjunction': 'Konjunkcija', 'TopicalOpposition': 'Opozicija',
	'TopicalOppositionRadix': 'Opozicija (radiks)', 'TopicalMoon': 'Luna', 'TopicalSelf': 'Sama', 'TopicalSign': 'Znak',
	'TopicalExaltation': 'Egzaltacija', 'TopicalTriplicity1': 'Triplicitet 1', 'TopicalTriplicity2': 'Triplicitet 2',
	'TopicalTriplicity3': 'Triplicitet 3', 'TopicalTerm': 'Termin', 'TopicalDecan': 'Dekan', 'LightOfTheTime': 'Svetlo vremena',
}

txtslotsdlg = {
	'Name': 'Ime', 'Formula': 'Formula', 'Diurnal': 'Dnevna', 'MaxLotsNum': 'Najveći broj tačaka je ',
	'LotAlreadyExists': 'Tačka sa tim imenom već postoji!', 'LotNameEmpty': 'Ime tačke je prazno!', 'Lots': 'Tačke', 'Add': 'Dodaj',
	'Modify': 'Izmeni', 'Remove': 'Ukloni', 'RemoveAll': 'Ukloni sve', 'Ascendant': 'Ascendent', 'LoFCannotBeRemoved': 'Fortuna ne može da se obriše',
	'ToggleDiurnal': 'Dnevna/noćna', 'Fortune': 'Fortuna', 'Reference': 'Polazna tačka', 'Degrees': 'Stepeni',
	'DegreeProblem': 'Stepen mora biti manji od', 'AlreadyReferring': 'Tačka na koju se poziva već se poziva na drugu',
	'FormulaWontBeCopied': 'Formula neće biti kopirana', 'AlreadyReferred': 'Na ovu tačku se poziva druga, pa ona ne može da se poziva na treću',
	'UseHousesNotDegrees': 'Cele kuće (znakovi) umesto stepeni',
}

txtstransitmdlg = dict(((k, v) for k, v in _years.items() if k != 'HelpDay'), **{
	'Transit': 'Tranzit', 'Year': 'Godina', 'Month': 'Mesec', 'InvalidDate': 'Neispravan datum!', 'Error': 'Greška',
})

txtsprimdirsdlg = {
	'PrimaryDirs': 'Primarne direkcije', 'Mundane': 'Mundane', 'HelpMundane': 'Koriste se širine i signifikatora i promisora',
	'Zodiacal': 'Zodijakalne', 'HelpZodiacal': 'Bar jedna od širina se ne koristi', 'Both': 'Obe', 'PlacidianSemiArc': 'Plasidus (poluluk)',
	'HelpPlacidianSemiArc': 'Kako se poluluk signifikatora odnosi prema njegovoj meridijanskoj distanci, tako se poluluk promisora odnosi prema njegovoj sekundarnoj distanci',
	'PlacidianUnderThePole': 'Plasidus (pod polom)', 'HelpPlacidianUnderThePole': 'Projektuje planete pod njihov sopstveni pol',
	'Regiomontanian': 'Regiomontanus', 'HelpRegiomontanian': 'Regiomontanova direkcija', 'Campanian': 'Kampanus',
	'HelpCampanian': 'Kampanusova direkcija', 'UseSZ': 'Koristi širinu', 'SZNeither': 'Nijednu',
	'HelpSZNeither': 'Ne koristi se ni širina promisora ni širina signifikatora', 'SZPromissor': 'Promisora',
	'HelpSZPromissor': 'Koristi se širina promisora', 'SZSignificator': 'Signifikatora', 'HelpSZSignificator': 'Koristi se širina signifikatora',
	'SZBoth': 'Obe', 'HelpSZBoth': 'Koriste se i širina promisora i širina signifikatora', 'ZodiacalOpts': 'Zodijakalne opcije',
	'ZodAspsPromsToSigs1': 'Aspekti promisora', 'ZodAspsPromsToSigs2': 'na signifikatore', 'ZodPromsToSigAsps1': 'Promisori na',
	'ZodPromsToSigAsps2': 'aspekte signifikatora', 'ZodAscMCHCsAsProms': 'Asc i MC kao promisori', 'Promissors': 'Promisori',
	'Significators': 'Signifikatori', 'Promissor': 'Promisor', 'Significator': 'Signifikator', 'SecondaryMotion': 'Sek. kretanje',
	'Antiscia': 'Antiscije', 'MidPoints': 'Središnje tačke', 'LoF': 'Fortuna', 'Terms': 'Termini', 'FixedStars': 'Fiksne zvezde',
	'Parallel': 'Paralela', 'Reset': 'Poništi', 'SelectAll': 'Izaberi sve', 'HouseCusps': 'Međukuće', 'RaptParallel': 'Raptna paralela',
	'smiter1': '1. iteracija', 'smiter2': '2. iteracija', 'smiter3': '3. iteracija',
}

txtsuserpddlg = {
	'Long': 'Dužina', 'Deg': 'Step', 'HelpPDDeg': 'Mora biti od 0 do 359', 'Min': 'Min', 'HelpMin': 'Mora biti od 0 do 59', 'Sec': 'Sek',
	'Lat': 'Širina', 'HelpLatDeg': 'Mora biti od 0 do 90', 'SouthernLatitude': 'Južna širina',
}

txtsfixedstarspddlg = {'Name': 'Ime', 'Nomencl': 'Oznaka', 'FixedStars': 'Fiksne zvezde', 'SelectAll': 'Izaberi sve', 'Reset': 'Poništi'}

txtsprimarykeysdlg = {
	'PrimaryKeys': 'Primarni ključevi', 'Keys': 'Ključevi', 'Dynamic': 'Dinamički', 'Static': 'Statički', 'Deg': 'Step', 'Min': 'Min',
	'HelpMin': 'Mora biti od 0 do 59', 'Sec': 'Sek', 'Coefficient': 'Koeficijent', 'UseRegrSun1': 'Za pravi sunčev luk i konverzne',
	'UseRegrSun2': 'direkcije koristi regresivno Sunce',
	'RangeError': 'Vrednost van opsega! Kliknite na upitnik pa na polje da vidite dozvoljene vrednosti!', 'Error': 'Greška',
	'Naibod': 'Najbod', 'Cardan': 'Kardan', 'Ptolemy': 'Ptolomej', 'User': 'Korisnički',
	'TrueSolarEquatorialArc': 'Pravi sunčev ekvatorski luk', 'TrueSolarEclipticalArc': 'Pravi sunčev ekliptički luk',
	'BirthdaySolarEquatorialArc': 'Pravi sunčev ekvatorski luk (rođendan)', 'BirthdaySolarEclipticalArc': 'Pravi sunčev ekliptički luk (rođendan)',
	'DynamicKey': 'Dinamički ključ', 'StaticKey': 'Statički ključ',
}

txtsprimdirsrangedlg = {'PrimaryDirs': 'Primarne direkcije', 'Age': 'Godine', 'Direct': 'Direktne', 'Converse': 'Konverzne', 'Both': 'Obe'}

txtspdsinchartoptsdlg = {
	'PDsInChart': 'PD u karti', 'FromMundanePos': 'Od planeta', 'FromZodiacalPos': 'Od njihovih ekliptičkih projekcija',
	'PseudoAstronomical': 'Potpuno pseudoastronomski', 'SecondaryMotion': 'Sekundarno kretanje',
}

txtsprimdirslist = dict(_years, **{
	'Start': 'Početak', 'Back': 'Nazad', 'Forward': 'Napred', 'End': 'Kraj', 'ToFirstPage': 'Na prvu stranu', 'ToBackPage': 'Stranu nazad',
	'ToForwardPage': 'Stranu napred', 'ToLastPage': 'Na poslednju stranu', 'RaptParallel': 'Raptna paralela', 'HelpHour': 'Mora biti od 0 do 23',
	'HelpMin': 'Mora biti od 0 do 59', 'Rectification': 'Rektifikacija', 'Calculate': 'Izračunaj', 'PrimaryDirs': 'Primarne direkcije',
	'Date': 'Datum', 'Arc': 'Luk', 'User': 'Korisnik', 'Syzygy': 'Sizigija', 'PDsInChartIngress': 'Ulasci', 'PDsInChart': 'PD u karti',
	'PDClickError': 'Kliknite desnim tasterom na direkciju u spisku', 'SwitchToEnglish': 'Ovo radi samo na engleskom jeziku.',
})

txtspdsinchartstepperdlg = dict(_years, **{
	'PDsInChart': 'PD u karti', 'Year': 'Godina', 'Month': 'Mesec', 'Day': 'Dan', 'Hour': 'Sat', 'HelpHour': 'Mora biti od 0 do 23',
	'Min': 'Min', 'HelpMin': 'Mora biti od 0 do 59', 'Sec': 'Sek', 'Direct': 'Direktne', 'Converse': 'Konverzne', 'Arc': 'Luk',
	'Show': 'Prikaži', 'Error': 'Greška', 'InvalidDate': 'Neispravan datum!', 'TimeSmallerThanBirthTime': 'Vreme ne može biti pre rođenja!',
})

txtsayanamsha = {
	'None': 'Ništa', 'Ayanamsa': 'Ajanamša', 'BabylonianKuglerI': 'Vavilonska, Kugler I', 'BabylonianKuglerII': 'Vavilonska, Kugler II',
	'BabylonianKuglerIII': 'Vavilonska, Kugler III', 'BabylonianHuber': 'Vavilonska, Huber', 'BabylonianMercier': 'Vavilonska, Mersije',
	'Aldebaran15Tau': 'Aldebaran 15 Bik', 'Hipparchos': 'Hiparh', 'Sassanian': 'Sasanidska', 'GalacticCenter0Sag': 'Galaktički centar na 0 Strelca',
	'Aldebaran15Tau2': 'Aldebaran 15 Bik', 'GalacticCenter0Sag2': 'Galaktički centar', 'Tropical': 'Tropski',
}

txtsprofdlg = dict(_years, **{
	'Profections': 'Profekcije', 'Year': 'Godina', 'Month': 'Mesec', 'Day': 'Dan', 'Hour': 'Sat', 'Min': 'Min', 'Sec': 'Sek',
	'InvalidDate': 'Neispravan datum!', 'Error': 'Greška', 'TimeSmallerThanBirthTime': 'Vreme ne može biti pre rođenja!',
	'PlacidianAnnualProfection': 'Plasidusova godišnja profekcija', 'ZodiacalAnnualProfection': 'Zodijakalna godišnja profekcija',
	'JulianDay': 'Julijanski dan', 'UseZodProjs': 'Koristi zodijakalne projekcije planeta', 'HelpHour': 'Mora biti od 0 do 23',
	'HelpMin': 'Mora biti od 0 do 59',
})

txtsprofdlgopts = {
	'Profections': 'Profekcije', 'PlacidianAnnualProfection': 'Plasidusova godišnja profekcija',
	'ZodiacalAnnualProfection': 'Zodijakalna godišnja profekcija', 'UseZodProjs': 'Koristi zodijakalne projekcije planeta',
}

txtsfirdariadlg = {'Firdaria': 'Firdarija', 'Nocturnal': 'Noćna'}

txtsdeflocdlgopts = {
	'DefaultLocation': 'Podrazumevano mesto', 'Long': 'Dužina', 'Lat': 'Širina', 'E': 'I', 'W': 'Z', 'N': 'S', 'S': 'J', 'Min': 'Min',
	'HelpMin': 'Mora biti od 0 do 59', 'Deg': 'Step', 'HelpLonDeg': 'Mora biti od 0 do 180', 'HelpLatDeg': 'Mora biti od 0 do 90',
	'Place': 'Mesto', 'HelpPlace': 'Mesto karte', 'HelpZoneHour': 'Mora biti od 0 do 12', 'HereAndNow': 'Ovde i sada',
	'Altitude': 'Nadmorska visina', 'HelpAltitude': 'Mora biti od 0 do 10000', 'Hour': 'Sat', 'HelpDaylight': 'Oduzima jedan sat',
	'Daylight': 'Letnje računanje vremena',
}

txtsprofstepperdlg = {'Profections': 'Profekcije', 'Dozen': 'Po 12'}

txtsproftabledlg = {'Profections': 'Profekcije', 'ProfsMainSignificatorsOnly': 'Samo glavni signifikatori', 'ProfsAll': 'Sve'}

txtsproftablemondlg = {'MonthlyProfections': 'Mesečne profekcije', 'Steps12': '12 koraka', 'Steps13': '13 koraka'}

txtscommon = {
	'Ok': 'U redu', 'Cancel': 'Otkaži', 'Close': 'Zatvori', 'HelpOk': 'Prihvati izmene', 'HelpCancel': 'Odbaci izmene',
	'AreYouSure': 'Da li ste sigurni?', 'Confirm': 'Potvrda', 'Planets': 'Planete', 'Day': 'Dan', 'Hour': 'Čas', 'Radix': 'Radiks',
	'Solar': 'Solarni povratak', 'Lunar': 'Lunarni povratak', 'Revolution': 'Povratak', 'Transit': 'Tranzit', 'Horary': 'Horar',
	'Profections': 'Profekcije', 'PDsInChart': 'PD u karti', 'Horoscope': 'Karta',
	'January': 'januar', 'February': 'februar', 'March': 'mart', 'April': 'april', 'May': 'maj', 'June': 'jun', 'July': 'jul',
	'August': 'avgust', 'September': 'septembar', 'October': 'oktobar', 'November': 'novembar', 'December': 'decembar',
	'Monday': 'ponedeljak', 'Tuesday': 'utorak', 'Wednesday': 'sreda', 'Thursday': 'četvrtak', 'Friday': 'petak', 'Saturday': 'subota',
	'Sunday': 'nedelja', 'Saturn': 'Saturn', 'Jupiter': 'Jupiter', 'Mars': 'Mars', 'Sun': 'Sunce', 'Venus': 'Venera',
	'Mercury': 'Merkur', 'Moon': 'Luna', 'ANode': 'Severni čvor', 'DNode': 'Južni čvor',
	'Aries': 'Ovan', 'Taurus': 'Bik', 'Gemini': 'Blizanci', 'Cancer': 'Rak', 'Leo': 'Lav', 'Virgo': 'Devica', 'Libra': 'Vaga',
	'Scorpio': 'Škorpija', 'Sagittarius': 'Strelac', 'Capricorn': 'Jarac', 'Aquarius': 'Vodolija', 'Pisces': 'Ribe',
	'Ari': 'Ova', 'Tau': 'Bik', 'Gem': 'Bli', 'Can': 'Rak', 'Vir': 'Dev', 'Lib': 'Vag', 'Sco': 'Ško', 'Sag': 'Str', 'Cap': 'Jar',
	'Aqu': 'Vod', 'Pis': 'Rib', 'Aspects': 'Aspekti', 'Conjunction': 'Konjunkcija', 'Sextile': 'Sekstil', 'Square': 'Kvadrat',
	'Trine': 'Trigon', 'Opposition': 'Opozicija', 'Nodes': 'Čvorovi', 'LoF': 'Fortuna', 'None': 'Ništa', 'RaptParallel': 'Raptna paralela',
	'Housesystem': 'Sistem kuća', 'HSPlacidus': 'Plasidus', 'HSKoch': 'Koh', 'HSCampanus': 'Kampanus', 'HSEqual': 'Jednake kuće',
	'HSWholeSign': 'Cele kuće', 'HSAxial': 'Aksijalni', 'HSHorizontal': 'Horizontalni', 'HSPagePolich': 'Pejdž-Poliš',
	'HSAlcabitus': 'Alkabitius', 'HSPorphyrius': 'Porfirije', 'Long': 'Dužina', 'Lat': 'Širina', 'E': 'I', 'W': 'Z', 'N': 'S', 'S': 'J',
	'Ascendant': 'Ascendent', 'MediumCoeli': 'MC', 'Transits': 'Tranziti', 'NotAvailable': 'Nije dostupno za karte pre nove ere',
	'CouldnotComputeRevolution': 'Povratak nije mogao da se izračuna!', 'Error': 'Greška', 'CouldnotComputeTransit': 'Tranzit nije mogao da se izračuna!',
	'NoTopicalsCreated': 'Nema napravljenih tematskih almutena!', 'NoSelFixedStars': 'Nijedna fiksna zvezda nije izabrana!',
	'FreeSoft': 'Slobodan softver', 'Description': 'Jednostavan i veoma precizan astrološki program.\nVerzija švajcarskih efemerida: ',
	'User': 'Korisnik', 'Syzygy': 'Sizigija', 'Parallel': 'Paralela', 'ContraParallel': 'Kontraparalela', 'MidPoint': 'Središnja tačka',
	'DinamicKey': 'Dinamički ključ', 'StaticKey': 'Statički ključ', 'DegPDList': 'step', 'MinPDList': 'min', 'SecPDList': 'sek',
	'Antiscion': 'Antiscija', 'Contraantiscion': 'Kontra-antiscija',
	'CheckUser': 'Proverite korisničke tačke (User, User2) u Podešavanja › Primarne direkcije.',
	'SelectColumn': 'Izaberite bar jednu kolonu u Podešavanja › Izgled II.',
	'BusyInfo': 'U zavisnosti od brzine računara i podešavanja primarnih direkcija ovo može da potraje.', 'Calculating': 'Računam',
	'NoPDsWithSettings': 'Nema primarnih direkcija sa ovim podešavanjima!', 'Information': 'Obaveštenje', 'Year': 'Godina',
	'Month': 'Mesec', 'NoSelLots': 'Nijedna tačka nije izabrana!',
}

txtsmenuseldlg = {'MenuSel': 'Izbor stavki menija'}

txtslangdlg = {'Languages': 'Jezik'}

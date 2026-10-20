# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import json
import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import urllib.parse

class Geonames:
    NAME, LON, LAT, COUNTRYCODE, COUNTRYNAME, ALTITUDE, GMTOFFS = list(range(0, 7))
    username = 'morinastro'
    langs = ('en', 'ru', 'fr')

    def __init__(self, city, maxnum, langid):
        self.city = city
        self.maxnum = maxnum
        self.langid = langid
        self.li = None
        return

    def fetch_values_from_page(self, url, params, key):
        url = url % urllib.parse.urlencode(params)
        try:
            page = urllib.request.urlopen(url)
            doc = json.loads(page.read())
            values = doc.get(key, None)
        except Exception as e:
            values = None

        return values

    def get_basic_info(self, city):
        url = 'http://api.geonames.org/searchJSON?%s'
        params = {'username': Geonames.username, 
           'lang': Geonames.langs[self.langid], 
           'q': city, 
           'featureClass': 'P', 
           'maxRows': self.maxnum}
        return self.fetch_values_from_page(url, params, 'geonames')

    def get_gmt_offset(self, longitude, latitude):
        url = 'http://api.geonames.org/timezoneJSON?%s'
        params = {'username': Geonames.username, 
           'lng': longitude, 
           'lat': latitude}
        return self.fetch_values_from_page(url, params, 'rawOffset')

    def get_elevation(self, longitude, latitude):
        url = 'http://api.geonames.org/astergdemJSON?%s'
        params = {'username': Geonames.username, 
           'lng': longitude, 
           'lat': latitude}
        return self.fetch_values_from_page(url, params, 'astergdem')

    def get_location_info(self):
        info = self.get_basic_info(self.city)
        if info == None:
            return False
        else:
            self.li = []
            for it in info:
                longitude = it.get('lng', 0)
                latitude = it.get('lat', 0)
                placename = it.get('name', '')
                country_code = it.get('countryCode', '')
                country_name = it.get('countryName', '')
                gmt_offset = self.get_gmt_offset(longitude, latitude)
                elevation = self.get_elevation(longitude, latitude)
                # the service leaves these out for some places
                if gmt_offset is None:
                    gmt_offset = 0.0
                if elevation is None:
                    elevation = 0
                self.li.append((placename, float(longitude), float(latitude),
                 country_code, country_name, elevation, gmt_offset))

            return True
import re
import pyproj
import requests
from simplejson.scanner import JSONDecodeError

apikey = 'USZWSgrBGpevjABqoXT3mLlUnkiR1Ruf8MWixp//eGc='
twd97 = pyproj.Proj(init='EPSG:3826')
wgs84 = pyproj.Proj(init='EPSG:4326')


class GeoConvert:
    def __init__(self):
        self.__cookies = {}
        self.__pageKey = ""
        self.__baseUrl = 'https://map.tgos.tw'

    def tgos_get_state(self):
        # pagekey 取得途徑: window.sircMessage.sircPAGEKEY = '...';
        r = requests.post(f'{self.__baseUrl}/TGOSCLOUD/Web/Map/TGOSViewer_Map.aspx')
        if r.status_code == 200:
            m = re.search('window\.sircMessage\.sircPAGEKEY\s?=\s?\'([\w\+%]+)\';', r.text)
            if m:
                self.__pageKey = m.group(1)
                for c in r.cookies:
                    self.__cookies[c.name] = c.value

    def tgos_by_spider(self, address: str):
        if not self.__pageKey:
            self.tgos_get_state()

        if self.__pageKey:
            # 取得 TWD 97 (EPSG 3826) 座標
            url = f'{self.__baseUrl}/TGOSCloud/Generic/Project/GHTGOSViewer_Map.ashx'
            params = {
                'pagekey': self.__pageKey,
                'method': 'querymoiaddr',
                'address': address,
                'sid': self.__cookies['ASP.NET_SessionId'],
                'useoddeven': False
            }
            headers = {
                'Origin': self.__baseUrl,
                'Referer': f'{self.__baseUrl}/TGOSCLOUD/Web/Map/TGOSViewer_Map.aspx',
                'X-Requested-With': 'XMLHttpRequest'
            }
            data = {
                'method': 'querymoiaddr',
                'address': address,
                'sid': self.__cookies['ASP.NET_SessionId'],
                'useoddeven': False
            }
            kwargs = {
                'params': params,
                'headers': headers,
                'cookies': self.__cookies,
                'data': data
            }
            r = requests.post(url, **kwargs)
            if r.status_code == 200:
                try:
                    addinfo = r.json()['AddressList']
                    if len(addinfo) > 0:
                        (x, y) = pyproj.transform(twd97, wgs84, addinfo[0]['X'], addinfo[0]['Y'])
                        return str(y), str(x)
                except JSONDecodeError as e:
                    pass
        return None, None

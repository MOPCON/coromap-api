import base64
import csv
import re
from urllib.parse import urlparse

import firebase_admin
import requests
from firebase_admin import credentials
from firebase_admin import db
from urllib.parse import unquote
from bs4 import BeautifulSoup

cred = credentials.Certificate('storage/serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hash-map-default-rtdb.asia-southeast1.firebasedatabase.app'
})

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }


with open('storage/import.csv') as csvfile:
    rows = iter(csv.reader(csvfile))
    next(rows)
    body = {}
    for row in rows:
        origin_url = requests.get(row[1], headers=headers)
        if '@' not in row[1]:
            m = re.search(r'APP_INITIALIZATION_STATE=\[\[\[(.+?)]', origin_url.text)
            _, longitude, latitude = m.group(1).split(',')
            title = BeautifulSoup(origin_url.text, 'html.parser').find('meta', property="og:title")
            shop_name = unquote(title['content'].split('·')[0])
            latitude = str(round(float(latitude), 7))
            longitude = str(round(float(longitude), 7))
        else:
            path = urlparse(origin_url.url).path.split('/')
            latitude = path[4].split(',')[0].split('@')[1]
            longitude = path[4].split(',')[1]
            shop_name = unquote(path[3])
        uid = base64.b64encode((shop_name + latitude + longitude).encode('utf-8'))
        body[uid.decode('ascii')] = {
            'latitude': latitude,
            'longitude': longitude,
            'inside_status': row[9],
            'shop_name': shop_name,
            'prevention_measures': row[9],
            'inside': True if row[3] == '是' else False or '',
            'outside': True if row[4] == '是' else False or '',
            'delivery': True if row[5] == '是' else False or '',
            'open': True if row[2] == '是' else False or '',
            'open_time_change': row[8],
            'discount': row[6],
        }
    ref = db.reference('')
    ref.child('mapData').update(body)

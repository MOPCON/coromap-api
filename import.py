import base64
import csv
from urllib.parse import urlparse

import firebase_admin
import requests
from firebase_admin import credentials
from firebase_admin import db
from urllib.parse import unquote

cred = credentials.Certificate('storage/serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hash-map-default-rtdb.asia-southeast1.firebasedatabase.app'
})

with open('storage/import.csv') as csvfile:
    rows = iter(csv.reader(csvfile))
    next(rows)
    body = {}
    for row in rows:
        origin_url = requests.get(row[1])
        path = urlparse(origin_url.url).path.split('/')
        uid = base64.b64encode((path[3] + path[4]).encode('ascii'))
        latitude = path[4].split(',')[0].split('@')[1]
        longitude = path[4].split(',')[1]
        body[uid.decode('ascii')] = {
            'latitude': latitude,
            'longitude': longitude,
            'inside_status': row[9],
            'shop_name': unquote(path[3]),
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

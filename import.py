import csv

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from common.utils import parse_data

cred = credentials.Certificate('storage/serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hash-map-default-rtdb.asia-southeast1.firebasedatabase.app'
})

with open('storage/import.csv') as csvfile:
    rows = iter(csv.reader(csvfile))
    next(rows)
    body = {}
    for row in rows:
        uid, data = parse_data(row)
        body[uid] = data
    ref = db.reference('')
    ref.child('mapData').update(body)

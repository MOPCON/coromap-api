from fastapi import Request, HTTPException  # pylint: disable=import-error

from fastapi import FastAPI
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

from common.utils import parse_data
from schema.stores import StoreData

app = FastAPI()
cred = credentials.Certificate('storage/serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hash-map-default-rtdb.asia-southeast1.firebasedatabase.app'
})


@app.post('/api/v1/stores', status_code=200)
async def get_stores(request: Request, _: StoreData):
    json_body = await request.json()
    uid, data = parse_data(json_body)
    if uid is None:
        raise HTTPException(status_code=400, detail='Data error')
    ref = db.reference('')
    ref.child('mapData').update({
        uid: data
    })
    return {
        'message': 'success'
    }

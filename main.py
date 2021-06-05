from fastapi import Request, HTTPException  # pylint: disable=import-error

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

from common.geo_convert import GeoConvert
from common.utils import parse_data
from config import Settings
from schema.stores import StoreData

settings = Settings()
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
cred = credentials.Certificate('storage/serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': settings.firebase_url
})
converter = GeoConvert()


@app.post('/api/v1/stores', status_code=200)
async def update_stores(request: Request, _: StoreData):
    json_body = await request.json()
    uid, data = parse_data(converter, json_body)
    if uid is None:
        raise HTTPException(status_code=400, detail='Data error')
    if 'msg' in data:
        raise HTTPException(status_code=400, detail=data['msg'])
    ref = db.reference('')
    ref.child('mapData').update({
        uid: data
    })
    return {
        'message': 'success'
    }


@app.get('/health', status_code=200)
def health():
    return {'health': 'ok'}

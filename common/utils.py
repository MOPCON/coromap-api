from datetime import datetime
import re
from operator import itemgetter
from urllib.parse import unquote, urlparse

import requests
import xxhash
from bs4 import BeautifulSoup

from common.geo_convert import GeoConvert

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


def parse_data(converter: GeoConvert, data):
    if isinstance(data, list):
        last_updated_at = int(datetime.strptime(data[0], '%Y/%m/%d %H:%M:%S').timestamp())
        url = data[1]
        open = data[2]
        inside = data[3]
        outside = data[4]
        delivery = data[5]
        discount = data[6]
        inside_status = data[7]
        open_time_change = data[8]
        prevention_measures = data[9]
    else:
        url, open, inside, outside, delivery, discount, inside_status, open_time_change, \
        prevention_measures = itemgetter('url', 'open', 'inside', 'outside', 'delivery',
                                         'discount', 'inside_status', 'open_time_change',
                                         'prevention_measures')(data)
        if 'last_updated_at' not in data:
            last_updated_at = int(datetime.now().timestamp())
        else:
            last_updated_at = data['last_updated_at']

    white_list = [
        'g.page',
        'goo.gl',
        'www.google.com',
    ]
    if urlparse(url).netloc not in white_list:
        return None, None

    if '@' not in url:
        origin_url = requests.get(url, headers=headers)
        # convert google map to tw language
        url = origin_url.url + '&hl=zh-TW'
    else:
        # convert google map to tw language
        url = url + '?hl=zh-TW'
    origin_url = requests.get(url, headers=headers)
    title = BeautifulSoup(origin_url.text, 'html.parser').find('meta', property="og:title")
    shop_name = unquote(title['content'].split(' · ')[0])
    address = re.search(r'^[0-9]*(.*)', title['content'].split(' · ')[1]).group(1)
    latitude, longitude = converter.tgos_by_spider(address)
    if latitude is None and longitude is None:
        # fall back if tgos can't resolve
        _, longitude, latitude = re.search(
            r'APP_INITIALIZATION_STATE=\[\[\[(.+?)]',
            origin_url.text
        ).group(1).split(',')
    uid = xxhash.xxh64((shop_name + latitude + longitude).encode('utf-8')).hexdigest()

    return uid, {
        'url': origin_url.url,
        'last_updated_at': last_updated_at,
        'latitude': latitude,
        'longitude': longitude,
        'inside_status': inside_status,
        'shop_name': shop_name,
        'prevention_measures': prevention_measures,
        'inside': True if inside == '是' else False or '',
        'outside': True if outside == '是' else False or '',
        'delivery': True if delivery == '是' else False or '',
        'open': True if open == '是' else False or '',
        'open_time_change': open_time_change,
        'discount': discount,
    }

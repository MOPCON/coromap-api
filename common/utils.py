from datetime import datetime
import re
from operator import itemgetter
from urllib.parse import unquote, urlparse

import requests
import xxhash
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


def parse_data(data):
    if isinstance(data, list):
        last_updated_at = int(datetime.strptime(data[0], '%Y/%m/%d %H:%M:%S').timestamp())
        url = data[1]
        open = data[2]
        inside = data[3]
        outside = data[4]
        delivery = data[5]
        discount = data[6]
        seat_change = data[7]
        open_time_change = data[8]
        prevention_measures = data[9]
    else:
        url, open, inside, outside, delivery, discount, seat_change, open_time_change, \
        prevention_measures = itemgetter('url', 'open', 'inside', 'outside', 'delivery',
                                         'discount', 'seat_change', 'open_time_change',
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

    origin_url = requests.get(url, headers=headers)
    if '@' not in url:
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
    uid = xxhash.xxh64((shop_name + latitude + longitude).encode('utf-8')).hexdigest()

    return uid, {
        'last_updated_at': last_updated_at,
        'latitude': latitude,
        'longitude': longitude,
        'inside_status': seat_change,
        'shop_name': shop_name,
        'prevention_measures': prevention_measures,
        'inside': True if inside == '是' else False or '',
        'outside': True if outside == '是' else False or '',
        'delivery': True if delivery == '是' else False or '',
        'open': True if open == '是' else False or '',
        'open_time_change': open_time_change,
        'discount': discount,
    }

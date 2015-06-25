"""Geo Functions
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from urllib.parse import quote_plus as _urlquote

def get_map_link(query: str='', lng: float=None, lat: float=None) -> str:
    url = 'https://www.google.com/maps/place'

    if query:
        url += '/' + _urlquote(query)

    if lat and lng:
        url += '/@' + '%f,%f' % (lat, lng)

    return url

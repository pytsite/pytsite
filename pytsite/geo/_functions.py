"""Geo Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from urllib.parse import quote_plus as _urlquote


def get_map_link(lng: float=None, lat: float=None, query: str=None, zoom: int=15) -> str:
    """Get link to map.
    """
    if lat and lng and query:
        return 'https://www.google.com/maps/search/{}/@{},{},{}z'.format(_urlquote(query), lat, lng, zoom)

    if lat and lng and not query:
        return 'https://www.google.com/maps?q={},{}'.format(lat, lng)

    if (not lat or not lng) and query:
        return 'https://www.google.com/maps/search/{}'.format(_urlquote(query), lat, lng)

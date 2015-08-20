"""Geo Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from urllib.parse import quote_plus as _urlquote


def get_map_link(lng: float, lat: float) -> str:
    """Get link to map.
    """
    return 'https://www.google.com/maps?q={},{}'.format(lng, lat)

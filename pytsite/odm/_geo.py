"""PytSite ODM Geo Helpers
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Point:
    def __init__(self, lng: float, lat: float, min_distance: float = None, max_distance: float = None):
        self._lng = lng
        self._lat = lat
        self._min_distance = min_distance
        self._max_distance = max_distance

    def as_dict(self) -> dict:
        r = {
            '$geometry': {
                'type': 'Point',
                'coordinates': [self._lng, self._lat],
            }
        }

        if self._min_distance:
            r['$minDistance'] = self._min_distance

        if self._max_distance:
            r['$maxDistance'] = self._max_distance

        return r

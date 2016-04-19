class Point:
    def __init__(self, lng: float, lat: float, min_distance: float = 0.0, max_distance: float = 0.0):
        self._lng = lng
        self._lat = lat
        self._min_distance = min_distance
        self._max_distance = max_distance

    def as_dict(self) -> dict:
        r = {
            '$geometry': {
                'type': 'Point',
                'coordinates': [self._lng, self._lat],
            },
            '$minDistance': self._min_distance,
            '$maxDistance': self._max_distance,
        }

        return r

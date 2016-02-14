"""ODM Finder Cache.
"""
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import threading as _threading, logger as _logger, reg as _reg
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__cache = {}


def pool_exists(model: str, pool_id: str) -> bool:
    """Check whether a cache pool exists.
    """
    with _threading.get_r_lock():
        if model not in __cache:
            return False

        if pool_id not in __cache[model]:
            return False

        return True


def create_pool(model: str, pool_id: str, ttl: int=3600):
    """Create a cache pool.
    """
    with _threading.get_r_lock():
        if pool_exists(model, pool_id):
            raise ValueError("Finder cache pool '{}:{}' already exists.".format(model, pool_id), __name__)

        if model not in __cache:
            __cache[model] = {}

        __cache[model][pool_id] = {
            'frozen': False,
            'ts': _datetime.now(),
            'ttl': ttl,
            'entities': [],
        }

        if _reg.get('odm.debug.enabled'):
            _logger.debug("New pool: '{}:{}'.".format(model, pool_id), __name__)


def add_entity(model: str, pool_id: str, entity: _model.Model):
    """Add an entity to the finder cache.
    """
    with _threading.get_r_lock():
        if not pool_exists(model, pool_id):
            raise KeyError("Finder cache pool '{}:{}' doesn't exist.".format(model, pool_id))

        if __cache[model][pool_id]['frozen']:
            raise ValueError("Finder cache pool '{}:{}' is frozen.".format(model, pool_id))

        __cache[model][pool_id]['entities'].append(entity)

        if _reg.get('odm.debug.enabled'):
            _logger.debug("Entity added to the pool '{}:{}': {}.".format(model, pool_id, str(entity.ref)),
                          __name__)


def freeze_pool(model: str, pool_id: str):
    """Freeze finder cache pool.
    """
    with _threading.get_r_lock():
        if not pool_exists(model, pool_id):
            raise KeyError("Finder cache pool '{}:{}' doesn't exist.".format(model, pool_id))

        if __cache[model][pool_id]['frozen']:
            raise ValueError("Finder cache pool '{}:{}' is already frozen.".format(model, pool_id))

        __cache[model][pool_id]['frozen'] = True

        if _reg.get('odm.debug.enabled'):
            _logger.debug("Finder cache pool frozen: '{}:{}'.".format(model, pool_id), __name__)


def get_entities(model: str, pool_id: str) -> tuple:
    """Get entities from the finder cache.
    """
    with _threading.get_r_lock():
        if not pool_exists(model, pool_id):
            raise KeyError("Finder cache pool '{}:{}' doesn't exist.".format(model, pool_id))

        if not __cache[model][pool_id]['frozen']:
            raise ValueError("Finder cache pool '{}:{}' is not frozen.".format(model, pool_id))

        r = tuple(__cache[model][pool_id]['entities'])

        if _reg.get('odm.debug.enabled'):
            _logger.debug("{} entities fetched from pool '{}:{}'.".format(len(r), model, pool_id), __name__)

        return r


def delete_pool(model: str, pool_id: str):
    """Delete pool from finder cache.
    """
    with _threading.get_r_lock():
        if not pool_exists(model, pool_id):
            return

        # We can delete only frozen pools
        if __cache[model][pool_id]['frozen']:
            del __cache[model][pool_id]
            if _reg.get('odm.debug.enabled'):
                _logger.debug("Deleted pool: '{}:{}'.".format(model, pool_id), __name__)


def model_has_opened_pool(model: str) -> bool:
    """Check whether the model has non-frozen pool.
    """
    with _threading.get_r_lock():
        if model not in __cache:
            return False

        for pool_id in __cache[model]:
            if not __cache[model][pool_id]['frozen']:
                return True

        return False


def delete_model(model: str):
    """Delete all cache pools for model.
    """
    with _threading.get_r_lock():
        if model in __cache:
            if model_has_opened_pool(model):
                raise ValueError("Finder cache has non-frozen pool(s) for model {}.".format(model))

            del __cache[model]

            if _reg.get('odm.debug.enabled'):
                _logger.debug("Cleared all pools for model '{}'".format(model), __name__)


def collect_garbage():
    """Remove garbage pools from finder cache.
    """
    with _threading.get_r_lock():
        if _reg.get('odm.debug.enabled'):
            _logger.debug("Garbage collector started.", __name__)

        to_delete = []

        now = _datetime.now()
        for model in __cache:
            for uid in __cache[model]:
                ts = __cache[model][uid]['ts']
                ttl = __cache[model][uid]['ttl']
                if (ts + _timedelta(seconds=ttl)) < now:
                    to_delete.append((model, uid))

        for model, uid in to_delete:
            delete_pool(model, uid)

        if _reg.get('odm.debug.enabled'):
            _logger.debug("Garbage collector finished.", __name__)

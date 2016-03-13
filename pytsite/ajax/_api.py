"""PytSite AJAX API Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__eps = {}


def is_ep_registered(ep_name: str) -> bool:
    """Check if the endpoint is registered.
    """
    return ep_name in __eps


def register_ep(ep_name: str):
    """Register an endpoint.
    """
    if is_ep_registered(ep_name):
        raise Exception("Endpoint '{}' is already registered.".format(ep_name))

    __eps[ep_name] = ep_name

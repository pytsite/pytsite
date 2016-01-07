"""LiveJournal Session.
"""
import pytz as _pytz
from typing import Iterable as _Iterable
from xmlrpc import client as _xmlrpc_client
from datetime import datetime as _datetime
from time import tzname as _tzname
from pytsite import util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Session:
    """LiveJournal Session.
    """
    def __init__(self, user: str, password: str):
        self._user = user
        self._password = _util.md5_hex_digest(password)
        self._proxy = _xmlrpc_client.ServerProxy('http://www.livejournal.com/interface/xmlrpc')

    def _get_request_args(self, args: dict) -> dict:
        challenge = self._proxy.LJ.XMLRPC.getchallenge()['challenge']
        args.update({
            'username': self._user,
            'auth_method': 'challenge',
            'auth_challenge': challenge,
            'auth_response': _util.md5_hex_digest(challenge + self._password),
        })

        return args

    def post_event(self, subject: str, event: str, tags: _Iterable[str]=None, dt: _datetime = None) -> dict:
        if not dt:
            dt = _datetime.now()

        if not dt.tzinfo:
            dt = _pytz.timezone(_tzname[0]).localize(dt)

        return self._proxy.LJ.XMLRPC.postevent(self._get_request_args({
            'subject': subject,
            'event': event,
            'year': dt.year,
            'mon': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'min': dt.minute,
            'props': {
                'taglist': ','.join(tags) if tags else ''
            },
        }))

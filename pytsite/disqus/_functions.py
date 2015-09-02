"""Disqus Functions.
"""
import urllib.request as _urllib_request
import urllib.parse as _urllib_parse
import json as _json
from datetime import datetime as _datetime
from pytsite import odm as _odm, reg as _reg, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_comments_count(thread_url: str) -> int:
    """Get comments count.
    """
    request_url = 'https://disqus.com/api/3.0/forums/listThreads.json?{}'

    api_secret = _reg.get('disqus.api_secret')
    if not api_secret:
        raise ValueError("Configuration parameter 'disqus.api_secret' is not defined.")

    short_name = _reg.get('disqus.short_name')
    if not short_name:
        raise ValueError("Configuration parameter 'disqus.short_name' is not defined.")

    entity = _odm.find('disqus_comment_count').where('thread', '=', thread_url).first()
    if entity:
        time_diff = _datetime.now() - entity.modified
        if time_diff.seconds <= 1800:  # 30 min
            return entity.f_get('count')
    else:
        entity = _odm.dispense('disqus_comment_count').f_set('thread', thread_url)

    data = _urllib_parse.urlencode({
        'api_secret': api_secret,
        'forum': short_name,
        'thread': 'link:' + thread_url
    })

    count = 0
    try:
        request_url = request_url.format(data)
        with _urllib_request.urlopen(request_url) as f:
            response = _json.loads(f.read().decode('utf-8'))

        for thread in response['response']:
            if not thread['isDeleted']:
                count += thread['posts']

        entity.f_set('count', count).save()
    except Exception as e:
        _logger.error(str(e), __name__)

    return count

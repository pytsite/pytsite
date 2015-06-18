__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import metatag as _metatag, lang as _lang, tpl as _tpl


def dashboard(args: dict, inp: dict):
    _metatag.t_set('title', _lang.t('pytsite.admin@dashboard'))
    return _tpl.render('pytsite.admin@html')

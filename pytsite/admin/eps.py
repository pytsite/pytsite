__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import core as _core

def dashboard(args: dict, inp: dict):
    _core.metatag.t_set('title', _core.lang.t('pytsite.admin@dashboard'))
    return _core.tpl.render('pytsite.admin@html')

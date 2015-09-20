from pytsite import metatag as _metatag, tpl as _tpl, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def dashboard(args: dict, inp: dict):
    """Dashboard endpoint.
    """
    _metatag.t_set('title', _lang.t('pytsite.admin@dashboard'))

    return _tpl.render('pytsite.admin@html')

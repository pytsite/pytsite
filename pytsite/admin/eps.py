__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import metatag, tpl
from pytsite.core.lang import t


def dashboard(args: dict, inp: dict):
    metatag.t_set('title', t('pytsite.admin@dashboard'))
    return tpl.render('pytsite.admin@html')

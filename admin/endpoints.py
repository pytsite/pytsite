__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import metatag, lang, tpl


def dashboard(values, request):
    metatag.set_tag('title', lang.t('pytsite.admin@dashboard'))
    return tpl.render('pytsite.admin@html')
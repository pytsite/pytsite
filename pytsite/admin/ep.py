from pytsite import metatag as _metatag, tpl as _tpl, lang as _lang, widget as _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def dashboard(args: dict, inp: dict):
    """Dashboard endpoint.
    """
    _metatag.t_set('title', _lang.t('pytsite.admin@dashboard'))

    app_name = _lang.t('app_name')
    try:
        app_name_short = _lang.t('app_name_short', exceptions=True)
    except _lang.error.TranslationError:
        app_name_short = app_name

    return _tpl.render('pytsite.admin@html', {
        'admin_language_nav': _widget.select.LanguageNav('admin-language-nav', dropdown=True),
        'app_name': app_name,
        'app_name_short': app_name_short,
    })

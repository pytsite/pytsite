"""Content Forms.
"""
from pytsite import form as _form, widget as _widget, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def form_widgets_setup(frm: _form.Form, values: dict):
    i = 10
    for l in _lang.langs():
        frm.add_widget(_widget.input.Text(
            uid='setting_home_title_' + l,
            label=_lang.t('pytsite.content@home_page_title', {'lang_code': l.upper()}, language=l),
            weight=i,
            value=values.get('home_title_' + l),
        ))
        i += 10

        frm.add_widget(_widget.input.Text(
            uid='setting_home_description_' + l,
            label=_lang.t('pytsite.content@home_page_description', {'lang_code': l.upper()}, language=l),
            weight=i,
            value=values.get('home_description_' + l),
        ))
        i += 10

        frm.add_widget(_widget.input.Tokens(
            uid='setting_home_keywords_' + l,
            label=_lang.t('pytsite.content@home_page_keywords', {'lang_code': l.upper()}, language=l),
            weight=i,
            value=values.get('home_keywords_' + l),
        ))
        i += 10

    frm.add_widget(_widget.input.TextArea(
        uid='setting_add_js',
        label=_lang.t('pytsite.content@additional_js_code'),
        rows=10,
        weight=i,
        value=values.get('add_js'),
    ))

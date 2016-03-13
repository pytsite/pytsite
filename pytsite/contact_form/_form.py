"""PytSite Contact Form.
"""
from pytsite import form as _form, widget as _widget, lang as _lang, assetman as _assetman

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_form.Form):
    """Contact Form.
    """
    def __init__(self, uid='pytsite-contact-form', **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._tpl = 'pytsite.contact_form@form'
        self._css += ' pytsite-contact-form'
        _assetman.add('pytsite.contact_form@js/common.js', permanent=True)

    def _setup(self):
        """Hook.
        """
        self.add_widget(_widget.input.Text(
            weight=10,
            uid='contact_name',
            placeholder=_lang.t('pytsite.contact_form@your_name'),
            label_hidden=True,
            required=True,
        ))

        self.add_widget(_widget.input.Email(
            weight=20,
            uid='contact_email',
            placeholder=_lang.t('pytsite.contact_form@your_email'),
            label_hidden=True,
            required=True,
        ))

        self.add_widget(_widget.input.TextArea(
            weight=30,
            uid='contact_message',
            placeholder=_lang.t('pytsite.contact_form@message'),
            label_hidden=True,
            required=True,
        ))

        self.add_widget(_widget.button.Submit(
            form_area='footer',
            weight=10,
            uid='contact_submit',
            value=_lang.t('pytsite.contact_form@send_message'),
        ))

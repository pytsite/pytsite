"""PytSite Contact Form.
"""
from pytsite import form as _form, widget as _widget, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Contact(_form.Base):
    """Contact Form.
    """
    def __init__(self, uid='pytsite-contact-form', **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._tpl = 'pytsite.contact@form'

    def _setup(self):
        """Hook.
        """
        self.add_widget(_widget.input.Text(
            weight=10,
            uid='contact_name',
            placeholder=_lang.t('pytsite.contact@your_name'),
            label_hidden=True,
            required=True,
        ))

        self.add_widget(_widget.input.Email(
            weight=20,
            uid='contact_email',
            placeholder=_lang.t('pytsite.contact@your_email'),
            label_hidden=True,
            required=True,
        ))

        self.add_widget(_widget.input.TextArea(
            weight=30,
            uid='contact_message',
            placeholder=_lang.t('pytsite.contact@message'),
            label_hidden=True,
            required=True,
        ))

        self.add_widget(_widget.button.Submit(
            form_area='footer',
            weight=10,
            uid='contact_submit',
            value=_lang.t('pytsite.contact@send_message'),
        ))

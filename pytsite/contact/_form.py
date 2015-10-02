"""PytSite Contact Form.
"""
from pytsite import form as _form, widget as _widget, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Contact(_form.Base):
    def __init__(self, uid='contact-form', **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._tpl = 'pytsite.contact@form'

    def _setup(self):
        """Hook.
        """
        self.add_widget(_widget.input.Text(
            weight=10,
            uid='contact_sender_name',
            placeholder=_lang.t('pytsite.contact@sender_name'),
        ))

        self.add_widget(_widget.input.Email(
            weight=20,
            uid='contact_sender_email',
            placeholder=_lang.t('pytsite.contact@sender_email'),
        ))

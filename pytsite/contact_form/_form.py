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

        self._css += ' pytsite-contact-form'
        self._prevent_submit = True
        self._area_footer_css += ' text-center'
        _assetman.add('pytsite.contact_form@js/contact-form.js')

    def _setup_widgets(self):
        """Hook.
        """
        name_email_container = _widget.Container(
            uid='name_email',
            weight=10,
            css='row',
            child_sep=None,
        )

        name_email_container.add_widget(_widget.input.Text(
            weight=10,
            uid='contact_name',
            placeholder=_lang.t('pytsite.contact_form@your_name'),
            label_hidden=True,
            required=True,
            css='col-xs-12 col-sm-6',
        ))

        name_email_container.add_widget(_widget.input.Email(
            weight=20,
            uid='contact_email',
            placeholder=_lang.t('pytsite.contact_form@your_email'),
            label_hidden=True,
            required=True,
            css='col-xs-12 col-sm-6',
        ))

        self.add_widget(name_email_container)

        self.add_widget(_widget.input.TextArea(
            weight=20,
            uid='contact_message',
            placeholder=_lang.t('pytsite.contact_form@message'),
            label_hidden=True,
            required=True,
        ))

        submit_btn = self.get_widget('action-submit')
        submit_btn.icon = None
        submit_btn.value = _lang.t('pytsite.contact_form@send_message')

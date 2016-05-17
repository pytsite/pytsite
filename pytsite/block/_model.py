"""PytSite Block Models.
"""
from pytsite import content as _content, odm as _odm, form as _form, widget as _widget, odm_ui as _odm_ui, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Block(_content.model.Base):
    def _setup_fields(self):
        """Hook.
        """
        super()._setup_fields()

        self.define_field(_odm.field.String('uid', nonempty=True))

    def _setup_indexes(self):
        super()._setup_indexes()

        self.define_index([('uid', _odm.I_ASC), ('language', _odm.I_ASC)], True)

    @property
    def uid(self) -> str:
        return self.f_get('uid')

    @classmethod
    def ui_browser_setup(cls, browser: _odm_ui.Browser):
        _content.model.Base.ui_browser_setup(browser)
        browser.data_fields = ('title', 'uid', 'author')

    def ui_browser_get_row(self) -> tuple:
        return self.title, self.uid, self.author.full_name

    def ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        super().ui_m_form_setup_widgets(frm)

        # ID
        frm.add_widget(_widget.input.Text(
            uid='uid',
            weight=50,
            label=self.t('uid'),
            value=self.uid,
            required=True,
        ))

    def ui_m_form_validate(self, frm: _form.Form):
        from . import _api, _error

        block_uid = frm.get_widget('uid').value

        if self.is_new:
            try:
                _api.get_block(block_uid)
                raise _form.error.ValidationError({
                    'uid': _lang.t('pytsite.block@block_already_exists')
                })
            except _error.BlockNotFound:
                pass
        else:
            existing_uid = self.uid
            new_uid = block_uid

            if new_uid != existing_uid:
                try:
                    _api.get_block(new_uid)
                    raise _form.error.ValidationError({
                        'uid': _lang.t('pytsite.block@block_already_exists')
                    })
                except _error.BlockNotFound:
                    pass

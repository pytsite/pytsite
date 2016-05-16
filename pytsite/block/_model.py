"""PytSite Block Models.
"""
from pytsite import content as _content, odm as _odm, form as _form, widget as _widget

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

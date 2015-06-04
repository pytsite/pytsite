"""Content Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.lang import t, t_plural, TranslationError
from pytsite.core.odm.models import ODMModel
from pytsite.core.odm.fields import *
from pytsite.odm_ui.models import ODMUIMixin
from pytsite.core.widgets.input import TextInputWidget
from pytsite.core.widgets.wysiwyg import WYSIWYGWidget
from pytsite.core.validation.rules import NotEmptyRule


class ContentModel(ODMModel, ODMUIMixin):
    """Content Model.
    """

    def _setup(self):
        """_setup() hook.
        """
        self._define_field(StringField('title', not_empty=True))
        self._define_field(StringField('body'))
        self._define_field(StringField('description'))
        self._define_field(RefField('path', model='path', not_empty=True))
        self._define_field(DateTimeField('publish_time', not_empty=True))
        self._define_field(IntegerField('views_count'))
        self._define_field(IntegerField('comments_count'))
        self._define_field(RefsListField('images', model='image'))
        self._define_field(StringListField('video'))
        self._define_field(StringListField('links'))
        self._define_field(StringField('status', default='published', not_empty=True))
        self._define_field(RefsListField('localizations', model=self.model))
        self._define_field(RefField('author', model='user', not_empty=True))
        self._define_field(StringField('language', not_empty=True))
        self._define_field(RefsListField('tags', model='tag'))
        self._define_field(RefField('section', model='section'))
        self._define_field(RefField('location', model='location'))
        self._define_field(BoolField('starred'))

    def _on_f_set(self, field_name: str, orig_value, **kwargs):
        """Hook.
        """
        if field_name == 'path':
            if isinstance(orig_value, str):
                orig_value = orig_value.strip()
                if orig_value:
                    path_obj = None

        return orig_value

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('path'):
            pass

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.browser.ODMUIBrowser
        :return: None
        """
        browser.data_fields = 'title',

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return (
            self.f_get('title'),
        )

    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.forms.BaseForm
        :return: None
        """
        form.add_widget(TextInputWidget(
            uid='title',
            label=self.t('title'),
            value=self.f_get('title'),
        ), 10)
        form.add_widget(WYSIWYGWidget(
            uid='body',
            label=self.t('body'),
            value=self.f_get('body'),
        ), 20)
        form.add_widget(TextInputWidget(
            uid='path',
            label=self.t('path'),
            value=self.f_get('path'),
        ), 80)

        form.add_rule('title', NotEmptyRule())

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        return self.f_get('title')

    def t(self, msg_id: str) -> str:
        """Translate a string.
        """
        try:
            return t(self.package() + '@' + msg_id)
        except TranslationError:
            return t('pytsite.content@' + msg_id)

    def t_plural(self, msg_id: str, num: int=2) -> str:
        """Translate a string into plural form.
        """
        try:
            return t_plural(self.package() + '@' + msg_id, num)
        except TranslationError:
            return t_plural('pytsite.content@' + msg_id, num)

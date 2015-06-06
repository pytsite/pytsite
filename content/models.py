"""Content Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router
from pytsite.core.html import A, Span
from pytsite.core.lang import t, t_plural, TranslationError
from pytsite.core.odm.models import ODMModel
from pytsite.core.odm.fields import *
from pytsite.odm_ui.models import ODMUIMixin
from pytsite.odm_ui.widgets import ODMSelectWidget
from pytsite.core.widgets.input import TextInputWidget, DateTimeInputWidget
from pytsite.core.widgets.selectable import SelectWidget
from pytsite.core.widgets.wysiwyg import WYSIWYGWidget
from pytsite.core.validation.rules import NotEmptyRule, DateTimeRule
from pytsite.auth import auth_manager
from pytsite.route_alias import route_alias_manager
from pytsite.taxonomy.models import AbstractTerm


class SectionModel(AbstractTerm):
    pass


class ContentModel(ODMModel, ODMUIMixin):
    """Content Model.
    """

    def _setup(self):
        """_setup() hook.
        """
        self._define_field(StringField('title', not_empty=True))
        self._define_field(StringField('body'))
        self._define_field(StringField('description'))
        self._define_field(RefField('path', model='route_alias', not_empty=True))
        self._define_field(DateTimeField('publish_time', default=datetime.now(), not_empty=True))
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

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'path':
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    value = self.f_get('title')

                if self.is_new:
                    value = route_alias_manager.create(value).save()
                else:
                    orig_value = self.f_get('path')
                    if orig_value.f_get('alias') != value:
                        orig_value.f_set('alias', value).save()
                    value = orig_value

        return super()._on_f_set(field_name, value, **kwargs)

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('path'):
            self.f_set('path', '')

        if not self.f_get('author'):
            self.f_set('author', auth_manager.get_current_user())

    def _after_save(self):
        """Hook.
        """
        if not self.f_get('path').f_get('target'):
            self.f_get('path').f_set('target', router.endpoint_url('pytsite.content.eps.view', {
                'model': self.model,
                'eid': self.id,
            }, True)).save()

    def _after_delete(self):
        """Hook.
        """
        self.f_get('path').delete()

        for i in self.f_get('images'):
            i.delete()

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.browser.ODMUIBrowser
        :return: None
        """
        browser.data_fields = 'title', 'status', 'publish_time', 'author'

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        title = str(A(self.f_get('title'), href=self.f_get('path').f_get('alias')))

        status = self.f_get('status')
        status_str = self.t('status_' + status)
        status_cls = 'primary'
        if status == 'waiting':
            status_cls = 'warning'
        elif status == 'unpublished':
            status_cls = 'default'

        return (
            title,
            str(Span(status_str, cls='label label-' + status_cls)),
            self.f_get('publish_time', fmt='%d.%m.%Y %H:%M'),
            self.f_get('author').f_get('full_name')
        )

    def setup_m_form(self, form):
        """Modify form setup hook.
        """
        from . import content_manager

        form.add_widget(ODMSelectWidget(
            uid='section',
            model='section',
            caption_field='title',
            label=self.t('section'),
            value=self.f_get('section'),
        ), 10)
        form.add_widget(TextInputWidget(
            uid='title',
            label=self.t('title'),
            value=self.f_get('title'),
        ), 30)
        form.add_widget(WYSIWYGWidget(
            uid='body',
            label=self.t('body'),
            value=self.f_get('body'),
        ), 40)
        form.add_widget(DateTimeInputWidget(
            uid='publish_time',
            label=self.t('publish_time'),
            value=self.f_get('publish_time'),
            h_size='col-sm-4 col-md-3 col-md-2',
        ), 70)
        form.add_widget(SelectWidget(
            uid='status',
            label=self.t('status'),
            value=self.f_get('status'),
            h_size='col-sm-4 col-md-3 col-md-2',
            items=content_manager.get_publish_statuses(),
        ), 80)
        form.add_widget(TextInputWidget(
            uid='path',
            label=self.t('path'),
            value=self.f_get('path').f_get('alias') if self.f_get('path') else '',
        ), 90)

        form.add_rule('title', NotEmptyRule())
        form.add_rules('publish_time', (NotEmptyRule(), DateTimeRule()))

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

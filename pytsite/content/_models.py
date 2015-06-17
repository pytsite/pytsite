"""Content Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime
from pytsite import auth, taxonomy, odm_ui, route_alias, image, geo
from pytsite.core import router, assetman, html, lang, odm, widget, validation


class SectionModel(taxonomy.model.Term):
    pass


class ContentModel(odm.model.ODMModel, odm_ui.model.ODMUIMixin):
    """Content Model.
    """

    def _setup(self):
        """Hook.
        """
        self._define_field(odm.field.String('title', not_empty=True))
        self._define_field(odm.field.String('body'))
        self._define_field(odm.field.String('description'))
        self._define_field(odm.field.Ref('route_alias', model='route_alias', not_empty=True))
        self._define_field(odm.field.DateTime('publish_time', default=datetime.now(), not_empty=True))
        self._define_field(odm.field.Integer('views_count'))
        self._define_field(odm.field.Integer('comments_count'))
        self._define_field(odm.field.RefsUniqueList('images', model='image'))
        self._define_field(odm.field.StringsListField('video'))
        self._define_field(odm.field.StringsListField('links'))
        self._define_field(odm.field.String('status', default='published', not_empty=True))
        self._define_field(odm.field.RefsUniqueList('localizations', model=self.model))
        self._define_field(odm.field.Ref('author', model='user', not_empty=True))
        self._define_field(odm.field.String('language', not_empty=True, default=lang.get_current_lang()))
        self._define_field(odm.field.RefsUniqueList('tags', model='tag',))
        self._define_field(odm.field.Ref('section', model='section', not_empty=True))
        self._define_field(geo.field.GeoLocationField('location'))
        self._define_field(odm.field.Bool('starred'))

        self._define_index([('location.lng_lat', odm.I_GEO2D)])

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'route_alias':
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    value = self.f_get('title')

                if self.is_new:
                    value = route_alias.manager.create(value).save()
                else:
                    orig_value = self.f_get('route_alias')
                    if orig_value.f_get('alias') != value:
                        orig_value.f_set('alias', value).save()
                    value = orig_value

        return super()._on_f_set(field_name, value, **kwargs)

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('author'):
            self.f_set('author', auth.manager.get_current_user())

        if not self.f_get('route_alias'):
            self.f_set('route_alias', '')

    def _after_save(self):
        """Hook.
        """
        if not self.f_get('route_alias').f_get('target'):
            self.f_get('route_alias').f_set('target', router.endpoint_url('pytsite.content.eps.view', {
                'model': self.model,
                'eid': self.id,
            }, True)).save()

    def _after_delete(self):
        """Hook.
        """
        self.f_get('route_alias').delete()

        for i in self.f_get('images'):
            i.delete()

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.ODMUIBrowser
        :return: None
        """
        browser.data_fields = 'title', 'status', 'publish_time', 'author'

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        title = str(html.A(self.f_get('title'), href=self.f_get('route_alias').f_get('alias')))

        status = self.f_get('status')
        status_str = self.t('status_' + status)
        status_cls = 'primary'
        if status == 'waiting':
            status_cls = 'warning'
        elif status == 'unpublished':
            status_cls = 'default'

        return (
            title,
            str(html.Span(status_str, cls='label label-' + status_cls)),
            self.f_get('publish_time', fmt='%d.%m.%Y %H:%M'),
            self.f_get('author').f_get('full_name')
        )

    def setup_m_form(self, form):
        """Hook.

        :type form: pytsite.core.form.Base
        """
        from . import _manager
        assetman.add('pytsite.content@js/content.js')

        if self.has_field('section'):
            form.add_widget(odm_ui.widget.ODMSelect(
                weight=10,
                uid='section',
                model='section',
                caption_field='title',
                label=self.t('section'),
                value=self.f_get('section'),
                h_size='col-sm-6',
            ))
            form.add_rule('section', validation.rule.NotEmpty())

        if self.has_field('title'):
            form.add_widget(widget.input.Text(
                weight=20,
                uid='title',
                label=self.t('title'),
                value=self.f_get('title'),
            ))
            form.add_rule('title', validation.rule.NotEmpty())

        form.add_widget(widget.input.Text(
            weight=30,
            uid='description',
            label=self.t('description'),
            value=self.f_get('description'),
        ))

        form.add_widget(taxonomy.widget.TermTokens(
            weight=40,
            uid='tags',
            model='tag',
            label=self.t('tags'),
            value=self.f_get('tags'),
        ))

        form.add_widget(image.widget.ImagesUploadWidget(
            weight=50,
            uid='images',
            label=self.t('images'),
            value=self.f_get('images'),
        ))

        if self.has_field('body'):
            form.add_widget(widget.wysiwyg.CKEditor(
                weight=60,
                uid='body',
                label=self.t('body'),
                value=self.f_get('body'),
            ))

        # Location
        form.add_widget(geo.widget.SearchAddress(
            weight=70,
            uid='location',
            label=self.t('location'),
            value=self.f_get('location'),
        ))

        if auth.manager.get_current_user().is_admin():
            form.add_widget(widget.select.DateTimeSelect(
                weight=80,
                uid='publish_time',
                label=self.t('publish_time'),
                value=datetime.now() if self.is_new else self.f_get('publish_time'),
                h_size='col-sm-4 col-md-3 col-md-2',
            ))
            form.add_rules('publish_time', (validation.rule.NotEmpty(), validation.rule.DateTime()))

            form.add_widget(widget.select.Select(
                weight=90,
                uid='status',
                label=self.t('status'),
                value=self.f_get('status'),
                h_size='col-sm-4 col-md-3 col-md-2',
                items=_manager.get_publish_statuses(),
            ))

            form.add_widget(widget.select.LanguageSelect(
                weight=100,
                uid='language',
                label=self.t('language'),
                value=self.f_get('language'),
                h_size='col-sm-4 col-md-3 col-md-2',
            ))

            form.add_widget(widget.input.Text(
                weight=110,
                uid='route_alias',
                label=self.t('path'),
                value=self.f_get('route_alias').f_get('alias') if self.f_get('route_alias') else '',
            ))

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        return self.f_get('title')

    def t(self, msg_id: str) -> str:
        """Translate a string.
        """
        try:
            return lang.t(self.package() + '@' + msg_id)
        except lang.error.TranslationError:
            return lang.t('pytsite.content@' + msg_id)

    def t_plural(self, msg_id: str, num: int=2) -> str:
        """Translate a string into plural form.
        """
        try:
            return lang.t_plural(self.package() + '@' + msg_id, num)
        except lang.error.TranslationError:
            return lang.t_plural('pytsite.content@' + msg_id, num)

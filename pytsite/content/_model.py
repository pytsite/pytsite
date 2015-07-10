"""Content Models
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from datetime import datetime as _datetime
from pytsite import auth as _auth, taxonomy as _taxonomy, odm_ui as _odm_ui, route_alias as _route_alias, \
    geo as _geo
from pytsite.core import odm as _odm, widget as _widget, validation as _validation, html as _html, router as _router, \
    lang as _lang, assetman as _assetman, events as _events


class Section(_taxonomy.model.Term):
    """Section Model.
    """
    pass


class Content(_odm.Model, _odm_ui.UIMixin):
    """Content Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('title', not_empty=True))
        self._define_field(_odm.field.String('body'))
        self._define_field(_odm.field.String('description'))
        self._define_field(_odm.field.Ref('route_alias', model='route_alias', not_empty=True))
        self._define_field(_odm.field.DateTime('publish_time', default=_datetime.now(), not_empty=True))
        self._define_field(_odm.field.Integer('views_count'))
        self._define_field(_odm.field.Integer('comments_count'))
        self._define_field(_odm.field.RefsUniqueList('images', model='image'))
        self._define_field(_odm.field.StringList('ext_links'))
        self._define_field(_odm.field.StringList('video_links'))
        self._define_field(_odm.field.String('status', default='published', not_empty=True))
        self._define_field(_odm.field.RefsUniqueList('localizations', model=self.model))
        self._define_field(_odm.field.Ref('author', model='user', not_empty=True))
        self._define_field(_odm.field.String('language', not_empty=True, default=_lang.get_current_lang()))
        self._define_field(_odm.field.RefsUniqueList('tags', model='tag',))
        self._define_field(_odm.field.Ref('section', model='section', not_empty=True))
        self._define_field(_geo.field.Location('location'))
        self._define_field(_odm.field.Bool('starred'))
        self._define_field(_odm.field.Virtual('url'))

        self._define_index([('location.lng_lat', _odm.I_GEO2D)])

    @property
    def title(self) -> str:
        return self.f_get('title')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def body(self) -> str:
        return self.f_get('body')

    @property
    def tags(self):
        """:rtype: list[pytsite.tag._model.Tag]
        """
        return self.f_get('tags')

    @property
    def images(self):
        """:rtype: list[pytsite.image._model.Image]
        """
        return self.f_get('images')

    @property
    def url(self) -> str:
        return self.f_get('url', relative=False)

    @property
    def ext_links(self) -> list:
        return self.f_get('ext_links')

    @property
    def video_links(self) -> list:
        return self.f_get('video_links')

    @property
    def author(self) -> _auth.model.User:
        return self.f_get('author')

    @property
    def section(self) -> Section:
        return self.f_get('section')

    @property
    def publish_time_pretty(self) -> str:
        return self.f_get('publish_time', fmt='pretty_date')

    @property
    def edit_url(self) ->str:
        return _router.endpoint_url('pytsite.odm_ui.eps.get_m_form', {
            'model': self.model,
            'id': self.id
        })

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'route_alias':
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    return

                if self.is_new:
                    value = _route_alias.manager.create(value).save()
                else:
                    orig_value = self.f_get('route_alias')
                    if orig_value.f_get('alias') != value:
                        orig_value.f_set('alias', value).save()
                    value = orig_value

        return super()._on_f_set(field_name, value, **kwargs)

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'url':
            if not self.is_new:
                target = _router.endpoint_url('pytsite.content.eps.view',
                                              {'model': self.model, 'id': str(self.id)},
                                              relative=kwargs.get('relative', True))
                r_alias = _route_alias.manager.find_by_target(target)
                value = r_alias.f_get('alias') if r_alias else target

        return value

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('author'):
            self.f_set('author', _auth.get_current_user())

        section_alias = self.f_get('section').f_get('alias')
        route_alias = self.f_get('route_alias')
        if route_alias:
            # If section has been changed, route alias part also needs to be changed
            route_alias_str = route_alias.f_get('alias')
            new_route_alias_str = _re.sub('^/\w+/', '/' + section_alias + '/', route_alias_str)
            if new_route_alias_str != route_alias_str:
                route_alias.f_set('alias', new_route_alias_str).save()
        else:
            new_route_alias_str = section_alias + '/' + self.f_get('title')
            route_alias = _route_alias.manager.create(new_route_alias_str).save()
            self.f_set('route_alias', route_alias)

        _events.fire('content.entity.pre_save', entity=self)
        _events.fire('content.entity.pre_save.' + self.model, entity=self)

    def _after_save(self):
        """Hook.
        """
        if not self.f_get('route_alias').f_get('target'):
            self.f_get('route_alias').f_set('target', _router.endpoint_url('pytsite.content.eps.view', {
                'model': self.model,
                'id': self.id,
            }, True)).save()

        _events.fire('content.entity.save', entity=self)
        _events.fire('content.entity.save.' + self.model, entity=self)

    def _after_delete(self):
        """Hook.
        """
        self.f_get('route_alias').delete()

        for i in self.f_get('images'):
            i.delete()

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        :return: None
        """
        browser.data_fields = 'title', 'section', 'status', 'publish_time', 'author'

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        title = str(_html.A(self.f_get('title'), href=self.f_get('route_alias').f_get('alias')))

        status = self.f_get('status')
        status_str = self.t('status_' + status)
        status_cls = 'primary'
        if status == 'waiting':
            status_cls = 'warning'
        elif status == 'unpublished':
            status_cls = 'default'

        return (
            title,
            self.f_get('section').f_get('title'),
            str(_html.Span(status_str, cls='label label-' + status_cls)),
            self.f_get('publish_time', fmt='%d.%m.%Y %H:%M'),
            self.f_get('author').f_get('full_name')
        )

    def browser_search(self, finder: _odm.Finder, query: str):
        """Hook.
        """
        finder.or_where('title', 'regex_i', query)

    def setup_m_form(self, form, stage: str):
        """Hook.
        :type form: pytsite.core.form.Base
        """
        from . import _functions
        _assetman.add('content@js/content.js')

        # Section
        form.add_widget(_odm_ui.widget.ODMSelect(
            weight=10,
            uid='section',
            model='section',
            caption_field='title',
            label=self.t('section'),
            value=self.f_get('section'),
            h_size='col-sm-6',
        ))
        form.add_rule('section', _validation.rule.NotEmpty())

        # Title
        form.add_widget(_widget.input.Text(
            weight=20,
            uid='title',
            label=self.t('title'),
            value=self.title,
        ))
        form.add_rule('title', _validation.rule.NotEmpty())

        # Description
        form.add_widget(_widget.input.Text(
            weight=30,
            uid='description',
            label=self.t('description'),
            value=self.description,
        ))

        # Tags
        form.add_widget(_taxonomy.widget.TokensInput(
            weight=40,
            uid='tags',
            model='tag',
            label=self.t('tags'),
            value=self.tags,
        ))

        # Images
        if self.has_field('images'):
            from pytsite import image
            form.add_widget(image.widget.ImagesUploadWidget(
                weight=50,
                uid='images',
                label=self.t('images'),
                value=self.f_get('images'),
                max_files=10
            ))

        # Body
        form.add_widget(_widget.input.CKEditor(
            weight=60,
            uid='body',
            label=self.t('body'),
            value=self.body,
        ))

        # Links
        if self.has_field('ext_links'):
            form.add_widget(_widget.input.StringList(
                weight=70,
                uid='ext_links',
                label=self.t('external_links'),
                add_btn_label=self.t('add_link'),
                value=self.ext_links
            ))
            form.add_rule('ext_links', _validation.rule.Url())

        # Links
        if self.has_field('video_links'):
            form.add_widget(_widget.input.StringList(
                weight=80,
                uid='video_links',
                label=self.t('video'),
                add_btn_label=self.t('add_link'),
                value=self.video_links
            ))
            form.add_rule('video_links', _validation.rule.VideoHostingUrl())

        # Location
        form.add_widget(_geo.widget.SearchAddress(
            weight=90,
            uid='location',
            label=self.t('location'),
            value=self.f_get('location'),
        ))

        # Visible only for admins
        if _auth.get_current_user().is_admin:
            # Publish time
            form.add_widget(_widget.select.DateTime(
                weight=100,
                uid='publish_time',
                label=self.t('publish_time'),
                value=_datetime.now() if self.is_new else self.f_get('publish_time'),
                h_size='col-sm-4 col-md-3 col-md-2',
            ))
            form.add_rules('publish_time', (_validation.rule.NotEmpty(), _validation.rule.DateTime()))

            # Status
            form.add_widget(_widget.select.Select(
                weight=110,
                uid='status',
                label=self.t('status'),
                value=self.f_get('status'),
                h_size='col-sm-4 col-md-3 col-md-2',
                items=_functions.get_publish_statuses(),
            ))

            # Language
            form.add_widget(_widget.select.Language(
                weight=120,
                uid='language',
                label=self.t('language'),
                value=self.f_get('language'),
                h_size='col-sm-4 col-md-3 col-md-2',
            ))

            # Route alias
            form.add_widget(_widget.input.Text(
                weight=130,
                uid='route_alias',
                label=self.t('path'),
                value=self.f_get('route_alias').f_get('alias') if self.f_get('route_alias') else '',
            ))

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        return self.f_get('title')

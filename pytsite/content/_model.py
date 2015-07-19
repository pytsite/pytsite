"""Content Models
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import auth as _auth, taxonomy as _taxonomy, odm_ui as _odm_ui, route_alias as _route_alias, \
    geo as _geo, image as _image, ckeditor as _ckeditor
from pytsite.core import odm as _odm, widget as _widget, validation as _validation, html as _html, router as _router, \
    lang as _lang, assetman as _assetman, events as _events, mail as _mail, tpl as _tpl


class Section(_taxonomy.model.Term):
    """Section Model.
    """
    def _pre_delete(self):
        from . import _functions
        for m in _functions.get_models():
            r_entity = _functions.find(m, None, False).where('section', '=', self).first()
            if r_entity:
                error_args = {'model': r_entity.model, 'title': r_entity.f_get('title')}
                raise _odm.error.ForbidEntityDelete(_lang.t('pytsite.content@referenced_entity_exists', error_args))

        tag = _taxonomy.find('tag').where('section', '=', self).first()
        if tag:
            error_args = {'model': tag.model, 'title': tag.f_get('title')}
            raise _odm.error.ForbidEntityDelete(_lang.t('pytsite,content@referenced_entity_exists', error_args))


class Tag(_taxonomy.model.Term):
    """Tag Model.
    """
    def _setup(self):
        """Hook.
        """
        super()._setup()
        self._define_field(_odm.field.RefsUniqueList('sections', model='section'))

    def setup_browser(self, browser):
        super().setup_browser(browser)
        browser.default_sort_field = 'weight'
        browser.default_sort_order = _odm.I_DESC


class Content(_odm.Model, _odm_ui.UIMixin):
    """Content Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('title', not_empty=True))
        self._define_field(_odm.field.String('description'))
        self._define_field(_odm.field.String('body'))
        self._define_field(_odm.field.Ref('route_alias', model='route_alias', not_empty=True))
        self._define_field(_odm.field.DateTime('publish_time', default=_datetime.now(), not_empty=True))
        self._define_field(_odm.field.Integer('views_count'))
        self._define_field(_odm.field.Integer('comments_count'))
        self._define_field(_odm.field.RefsUniqueList('images', model='image'))
        self._define_field(_odm.field.String('status', not_empty=True))
        self._define_field(_odm.field.RefsUniqueList('localizations', model=self.model))
        self._define_field(_odm.field.Ref('author', model='user', not_empty=True))
        self._define_field(_odm.field.String('language', not_empty=True, default=_lang.get_current_lang()))
        self._define_field(_odm.field.RefsUniqueList('tags', model='tag',))
        self._define_field(_odm.field.StringList('video_links'))
        self._define_field(_odm.field.Virtual('url'))
        self._define_field(_odm.field.Virtual('edit_url'))

    @property
    def title(self) -> str:
        return self.f_get('title')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def body(self) -> str:
        return self.f_get('body', process_tags=True)

    @property
    def tags(self):
        """:rtype: list[pytsite.content._model.Tag]
        """
        return self.f_get('tags', sort_by='weight', sort_reverse=True)

    @property
    def images(self):
        """:rtype: list[pytsite.image._model.Image]
        """
        return self.f_get('images')

    @property
    def url(self) -> str:
        return self.f_get('url', relative=False)

    @property
    def edit_url(self) -> str:
        return self.f_get('edit_url')

    @property
    def author(self) -> _auth.model.User:
        return self.f_get('author')

    @property
    def publish_time(self) -> _datetime:
        return self.f_get('publish_time')

    @property
    def publish_time_pretty(self) -> str:
        return self.f_get('publish_time', fmt='pretty_date')

    @property
    def route_alias(self) -> _route_alias.model.RouteAlias:
        return self.f_get('route_alias')

    @property
    def views_count(self) -> int:
        return self.f_get('views_count')

    @property
    def comments_count(self) -> int:
        return self.f_get('comments_count')

    @property
    def video_links(self) -> list:
        return self.f_get('video_links')

    @property
    def status(self) -> str:
        return self.f_get('status')

    @property
    def searchable_fields(self) -> tuple:
        return 'title',

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'route_alias':
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    value = self.title

                if self.is_new:
                    # Create new route alias
                    value = _route_alias.create(value, 'NONE').save()
                else:
                    orig_value = self.f_get('route_alias')
                    if orig_value.f_get('alias') != value:
                        orig_value.f_set('alias', value).save()
                    value = orig_value

        if field_name == 'status':
            from ._functions import get_publish_statuses
            if value not in [v[0] for v in get_publish_statuses()]:
                raise Exception("Invalid publish status: '{}'.".format(value))

        return super()._on_f_set(field_name, value, **kwargs)

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'url' and not self.is_new:
            target_path = _router.endpoint_path('pytsite.content.eps.view', {'model': self.model, 'id': str(self.id)})
            r_alias = _route_alias.find_one_by_target(target_path)
            value = r_alias.f_get('alias') if r_alias else target_path

            # Transform path to absolute URL
            if not kwargs.get('relative', False):
                value = _router.url(value)

        if field_name == 'edit_url' and self.id:
            value = _router.endpoint_url('pytsite.odm_ui.eps.get_m_form', {
                'model': self.model,
                'id': self.id
            })

        if field_name == 'body' and kwargs.get('process_tags'):
            value = self._process_body_tags(value)

        if field_name == 'tags':
            if kwargs.get('as_string'):
                value = ','.join([tag.title for tag in self.f_get('tags')])

        return value

    def _pre_save(self):
        """Hook.
        """
        super()._pre_save()

        current_user = _auth.get_current_user()

        # Author is required
        if not self.author and current_user:
            self.f_set('author', current_user)

        # Route alias is required
        if not self.route_alias:
            self.f_set('route_alias', self.title)

        # Extract inline images from the body
        body, images = self._extract_body_images()
        self.f_set('body', body).f_set('images', images)

        # Changing status if necessary
        if not self.status:
            if current_user and current_user.has_permission('pytsite.content.bypass_moderation.' + self.model):
                self.f_set('status', 'published')
            else:
                self.f_set('status', 'waiting')

        _events.fire('content.entity.pre_save', entity=self)
        _events.fire('content.entity.pre_save.' + self.model, entity=self)

    def _after_save(self):
        """Hook.
        """
        if self.is_new:
            # Update route alias target which has been created in self._pre_save()
            if self.f_get('route_alias').f_get('target') == 'NONE':
                target = _router.endpoint_path('pytsite.content.eps.view', {'model': self.model, 'id': self.id})
                self.f_get('route_alias').f_set('target', target).save()

            # Clean up not fully filled route aliases
            f = _route_alias.find()
            f.where('target', '=', 'NONE').where('_created', '<', _datetime.now() - _timedelta(1))
            for ra in f.get():
                ra.delete()

            # Notify content moderators about waiting content
            if self.is_new and self.status == 'waiting':
                self._send_waiting_status_notification()
                if _router.session:
                    _router.session.add_info(_lang.t('pytsite.content@content_will_be_published_after_moderation'))

            # Recalculate tags weights
            from . import _functions
            for tag in self.tags:
                weight = 0
                for model in _functions.get_models().keys():
                    weight += _functions.find(model).where('tags', 'in', [tag]).count()
                tag.f_set('weight', weight).save()

        # Creating back links in images
        for img in self.images:
            if not img.f_get('attached_to'):
                img.f_set('attached_to', self).f_set('owner', self.author).save()

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
        browser.data_fields = 'title', 'status', 'publish_time', 'author'
        browser.default_sort_field = 'publish_time'

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
        _assetman.add('pytsite.content@js/content.js')

        # Title
        form.add_widget(_widget.input.Text(
            weight=100,
            uid='title',
            label=self.t('title'),
            value=self.title,
        ))
        form.add_rule('title', _validation.rule.NotEmpty())

        # Description
        form.add_widget(_widget.input.Text(
            weight=200,
            uid='description',
            label=self.t('description'),
            value=self.description,
        ))

        # Tags
        form.add_widget(_taxonomy.widget.TokensInput(
            weight=300,
            uid='tags',
            model='tag',
            label=self.t('tags'),
            value=self.tags,
        ))

        # Images
        if self.has_field('images'):
            from pytsite import image
            form.add_widget(image.widget.ImagesUploadWidget(
                weight=400,
                uid='images',
                label=self.t('images'),
                value=self.f_get('images'),
                max_files=10
            ))

        # Video links
        if self.has_field('video_links'):
            form.add_widget(_widget.input.StringList(
                weight=500,
                uid='video_links',
                label=self.t('video'),
                add_btn_label=self.t('add_link'),
                value=self.video_links
            ))
            form.add_rule('video_links', _validation.rule.VideoHostingUrl())

        # Body
        form.add_widget(_ckeditor.widget.CKEditor(
            weight=600,
            uid='body',
            label=self.t('body'),
            value=self.f_get('body', process_tags=False),
        ))
        form.add_rule('body', _validation.rule.NotEmpty())

        # Status
        current_user = _auth.get_current_user()
        if current_user and current_user.has_permission('pytsite.content.bypass_moderation.' + self.model):
            form.add_widget(_widget.select.Select(
                weight=700,
                uid='status',
                label=self.t('status'),
                value=self.status if self.status else 'published',
                h_size='col-sm-4 col-md-3 col-lg-2',
                items=_functions.get_publish_statuses(),
            ))
            form.add_rule('status', _validation.rule.NotEmpty())

        # Visible only for admins
        if _auth.get_current_user().is_admin:
            # Publish time
            form.add_widget(_widget.select.DateTime(
                weight=800,
                uid='publish_time',
                label=self.t('publish_time'),
                value=_datetime.now() if self.is_new else self.f_get('publish_time'),
                h_size='col-sm-4 col-md-3 col-lg-2',
            ))
            form.add_rules('publish_time', (_validation.rule.NotEmpty(), _validation.rule.DateTime()))

            # Language
            form.add_widget(_widget.select.Language(
                weight=900,
                uid='language',
                label=self.t('language'),
                value=self.f_get('language'),
                h_size='col-sm-4 col-md-3 col-lg-2',
            ))

            # Route alias
            form.add_widget(_widget.input.Text(
                weight=1000,
                uid='route_alias',
                label=self.t('path'),
                value=self.f_get('route_alias').f_get('alias') if self.f_get('route_alias') else '',
            ))

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        return self.f_get('title')

    def _process_body_tags(self, inp: str) -> str:
        def process_img_tag(match):
            img_index = int(match.group(1))
            if len(self.images) < img_index:
                return ''
            img = self.images[img_index - 1]
            return '<img class="img-responsive" src="{}" data-path="{}">'.format(img.url, img.path)

        def process_vid_tag(match):
            vid_index = int(match.group(1))
            if len(self.video_links) < vid_index:
                return ''
            return str(_widget.static.VideoPlayer(value=self.video_links[vid_index - 1]))

        inp = _re.sub('\[img:(\d+)\]', process_img_tag, inp)
        inp = _re.sub('\[vid:(\d+)\]', process_vid_tag, inp)

        return inp

    def _extract_body_images(self) -> tuple:
        """Transforms inline <img> tags into [img] tags
        """
        images = self.images
        img_index = len(images)

        def replace_func(match):
            nonlocal img_index, images
            img_index += 1
            images.append(_image.create(match.group(1)))
            return '[img:{}]'.format(img_index)

        body = _re.sub('<img.*src\s*=["\']([^"\']+)["\'][^>]*>', replace_func, self.f_get('body'))

        return body, images

    def _send_waiting_status_notification(self):
        for u in _auth.find_users().get():
            if u.has_permission('pytsite.odm_ui.modify.' + self.model):
                m_to = '{} <{}>'.format(u.f_get('full_name'), u.f_get('email'))
                m_subject = _lang.t('pytsite.content@content_waiting_mail_subject', {'app_name': _lang.t('app_name')})
                m_body = _tpl.render('pytsite.content@mail/propose-' + _lang.get_current_lang(), {
                    'user': u,
                    'entity': self,
                })
                _mail.Message(m_to, m_subject, m_body).send()


class Page(Content):
    """Page Model.
    """
    pass


class Article(Content):
    """Article Model.
    """
    @property
    def section(self) -> Section:
        return self.f_get('section')

    @property
    def ext_links(self) -> list:
        return self.f_get('ext_links')

    @property
    def starred(self) -> bool:
        return self.f_get('starred')

    @property
    def location(self) -> list:
        return self.f_get('location')

    def _setup(self):
        super()._setup()
        self._define_field(_odm.field.Ref('section', model='section', not_empty=True))
        self._define_field(_odm.field.StringList('ext_links'))
        self._define_field(_odm.field.Bool('starred'))
        self._define_field(_geo.field.Location('location'))

        self._define_index([('location.lng_lat', _odm.I_GEO2D)])

    def setup_m_form(self, form, stage: str):
        super().setup_m_form(form, stage)

        # Starred
        if _auth.get_current_user().is_admin:
            form.add_widget(_widget.select.Checkbox(
                weight=30,
                uid='starred',
                label=self.t('starred'),
                value=self.starred,
            ))

        # Section
        form.add_widget(_odm_ui.widget.EntitySelect(
            weight=60,
            uid='section',
            model='section',
            caption_field='title',
            label=self.t('section'),
            value=self.section,
            h_size='col-sm-6',
        ))
        form.add_rule('section', _validation.rule.NotEmpty())

        # External links
        if self.has_field('ext_links'):
            form.add_widget(_widget.input.StringList(
                weight=630,
                uid='ext_links',
                label=self.t('external_links'),
                add_btn_label=self.t('add_link'),
                value=self.ext_links
            ))
            form.add_rule('ext_links', _validation.rule.Url())

        # Location
        form.add_widget(_geo.widget.SearchAddress(
            weight=660,
            uid='location',
            label=self.t('location'),
            value=self.location,
        ))

    def _pre_save(self):
        # Create route alias
        if not self.route_alias:
            route_alias_str = self.title
            if self.section:
                route_alias_str = self.section.alias + '/' + route_alias_str
            route_alias = _route_alias.create(route_alias_str, 'NONE').save()
            self.f_set('route_alias', route_alias)

        super()._pre_save()


class ContentSubscriber(_odm.Model):
    def _setup(self):
        self._define_field(_odm.field.String('email', not_empty=True))
        self._define_field(_odm.field.Bool('enabled', default=True))
        self._define_index([('email', _odm.I_ASC)])

"""Content Models
"""
import re as _re
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import auth as _auth, taxonomy as _taxonomy, odm_ui as _odm_ui, route_alias as _route_alias, \
    geo as _geo, image as _image, ckeditor as _ckeditor, odm as _odm, widget as _widget, validation as _validation, \
    html as _html, router as _router, lang as _lang, assetman as _assetman, events as _events, mail as _mail, \
    tpl as _tpl, auth_ui as _auth_ui, reg as _reg, util as _util, comments as _comments

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Section(_taxonomy.model.Term):
    """Section Model.
    """
    def _pre_delete(self, **kwargs):
        from . import _api
        for m in _api.get_models():
            f = _api.find(m, status=None, check_publish_time=False)
            if not f.mock.has_field('section'):
                continue
            r_entity = f.where('section', '=', self).first()
            if r_entity:
                error_args = {'model': r_entity.model, 'title': r_entity.f_get('title')}
                raise _odm.error.ForbidEntityDelete(_lang.t('pytsite.content@referenced_entity_exists', error_args))

        f = _taxonomy.find('tag')
        if f.mock.has_field('sections'):
            tag = f.where('sections', 'in', [self]).first()
            if tag:
                error_args = {'model': tag.model, 'title': tag.f_get('title')}
                raise _odm.error.ForbidEntityDelete(_lang.t('pytsite.content@referenced_entity_exists', error_args))


class Tag(_taxonomy.model.Term):
    """Tag Model.
    """
    def _setup(self):
        """Hook.
        """
        super()._setup()
        self.define_field(_odm.field.RefsUniqueList('sections', model='section'))

    @classmethod
    def ui_browser_setup(cls, browser):
        """Hook.

        :type browser: pytsite.odm_ui._browser.Browser
        """
        super().ui_browser_setup(browser)
        browser.default_sort_field = 'weight'
        browser.default_sort_order = _odm.I_DESC


class Content(_odm_ui.UIModel):
    """Base Content Model.
    """
    def _setup(self):
        """Hook.
        """
        self.define_field(_odm.field.String('title', nonempty=True))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.String('body'))
        self.define_field(_odm.field.Ref('route_alias', model='route_alias', nonempty=True))
        self.define_field(_odm.field.DateTime('publish_time', default=_datetime.now(), nonempty=True))
        self.define_field(_odm.field.Integer('views_count'))
        self.define_field(_odm.field.Integer('comments_count'))
        self.define_field(_odm.field.RefsUniqueList('images', model='image'))
        self.define_field(_odm.field.String('status', nonempty=True))
        self.define_field(_odm.field.Ref('author', model='user', nonempty=True))
        self.define_field(_odm.field.String('language', nonempty=True, default=_lang.get_current()))
        self.define_field(_odm.field.String('language_db', nonempty=True))
        self.define_field(_odm.field.RefsUniqueList('tags', model='tag', ))
        self.define_field(_odm.field.Virtual('url'))
        self.define_field(_odm.field.Virtual('edit_url'))
        self.define_field(_odm.field.Dict('options'))

        for lng in _lang.langs():
            self.define_field(_odm.field.Ref('localization_' + lng, model=self.model))

        self.define_index([('publish_time', _odm.I_DESC)])
        self.define_index([('title', _odm.I_TEXT), ('body', _odm.I_TEXT)])

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
        return self.f_get('publish_time', fmt='pretty_date_time')

    @property
    def publish_date_pretty(self) -> str:
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
    def options(self) -> dict:
        return self.f_get('options')

    @property
    def language(self) -> str:
        return self.f_get('language')

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'route_alias' and (isinstance(value, str) or value is None):
            # Generate route alias string via hook method
            if value is None:
                value = ''
            route_alias_str = self._alter_route_alias_str(value.strip())

            # No route alias is attached, so we need to create a new one
            if not self.route_alias:
                value = _route_alias.create(route_alias_str, 'NONE', self.language).save()

            # Existing route alias is attached and its value needs to be changed
            elif self.route_alias and self.route_alias.alias != route_alias_str:
                self.route_alias.delete()
                value = _route_alias.create(route_alias_str, 'NONE', self.language).save()

            # Keep old route alias
            else:
                value = self.route_alias

        elif field_name == 'status':
            from ._api import get_publish_statuses
            if value not in [v[0] for v in get_publish_statuses()]:
                raise Exception("Invalid publish status: '{}'.".format(value))

        elif field_name == 'language':
            if value not in _lang.langs():
                raise ValueError("Language '{}' is not supported.".format(value))

            if value == 'en':
                self.f_set('language_db', 'english')
            elif value == 'ru':
                self.f_set('language_db', 'russian')
            else:
                self.f_set('language_db', 'none')

        return super()._on_f_set(field_name, value, **kwargs)

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'url' and not self.is_new:
            target_path = _router.ep_path('pytsite.content.ep.view', {'model': self.model, 'id': str(self.id)}, True)
            r_alias = _route_alias.find_by_target(target_path, self.language)
            value = r_alias.alias if r_alias else target_path

            # Transform path to absolute URL
            value = _router.url(value, self.language, relative=kwargs.get('relative', False))

        if field_name == 'edit_url' and self.id:
            value = _router.ep_url('pytsite.odm_ui.ep.get_m_form', {
                'model': self.model,
                'id': self.id
            })

        if field_name == 'body' and kwargs.get('process_tags'):
            value = self._process_body_tags(value, kwargs.get('responsive', True), kwargs.get('width'))

        if field_name == 'tags':
            if kwargs.get('as_string'):
                value = ','.join([tag.title for tag in self.f_get('tags')])

        return value

    def _pre_save(self):
        """Hook.
        """
        super()._pre_save()

        current_user = _auth.get_current_user()

        # Language is required
        if not self.language or not self.f_get('language_db'):
            self.f_set('language', _lang.get_current())

        # Author is required
        if not self.author and not current_user.is_anonymous:
            self.f_set('author', current_user)

        # Route alias is required
        if not self.route_alias:
            self.f_set('route_alias', None)

        # Extract inline images from the body
        body, images = self._extract_body_images()
        self.f_set('body', body).f_set('images', images)

        # Changing status if necessary
        if self.is_new and _reg.get('env.type') != 'console':
            if not current_user.has_permission('pytsite.content.bypass_moderation.' + self.model):
                self.f_set('status', 'waiting')
            elif not self.status:
                self.f_set('status', 'published')

        _events.fire('pytsite.content.entity.pre_save', entity=self)
        _events.fire('pytsite.content.entity.{}.pre_save.'.format(self.model), entity=self)

    def _after_save(self):
        """Hook.
        """
        # Update route alias target which has been created in self._pre_save()
        if self.route_alias.target == 'NONE':
            target = _router.ep_path('pytsite.content.ep.view', {'model': self.model, 'id': self.id}, True)
            self.route_alias.f_set('target', target).save()

        if self.is_new:
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
        from . import _api
        for tag in self.tags:
            weight = 0
            for model in _api.get_models().keys():
                weight += _api.find(model, language=self.language).where('tags', 'in', [tag]).count()
            tag.f_set('weight', weight).save()

        # Creating back links in images
        for img in self.images:
            if not img.f_get('attached_to'):
                img.f_set('attached_to', self).f_set('owner', self.author).save()

        # Updating localization entities references
        for lng in _lang.langs(False):
            localization = self.f_get('localization_' + lng)
            if isinstance(localization, Content):
                if localization.f_get('localization_' + self.language) != self:
                    localization.f_set('localization_' + self.language, self).save()
            elif localization is None:
                f = _api.find(self.model, language=lng).where('localization_' + self.language, '=', self)
                for referenced in f.get():
                    referenced.f_set('localization_' + self.language, None).save()

        _events.fire('pytsite.content.entity.save', entity=self)
        _events.fire('pytsite.content.entity.{}.save'.format(self.model), entity=self)

    def _after_delete(self):
        """Hook.
        """
        self.f_get('route_alias').delete()

        for i in self.f_get('images'):
            i.delete()

    @classmethod
    def ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = 'title', 'status', 'images', 'publish_time', 'author'
        browser.default_sort_field = 'publish_time'

        def finder_adjust(finder: _odm.Finder):
            finder.where('language', '=', _lang.get_current())
        browser.finder_adjust = finder_adjust

    def ui_browser_get_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        title = str(_html.A(self.f_get('title'), href=self.url))

        status = self.f_get('status')
        status_str = self.t('status_' + status)
        status_cls = 'primary'
        if status == 'waiting':
            status_cls = 'warning'
        elif status == 'unpublished':
            status_cls = 'default'

        images_cls = 'default' if not len(self.images) else 'primary'

        return (
            title,
            str(_html.Span(status_str, cls='label label-' + status_cls)),
            '<span class="label label-{}">{}</span>'.format(images_cls, len(self.images)),
            self.f_get('publish_time', fmt='%d.%m.%Y %H:%M'),
            self.f_get('author').full_name
        )

    def ui_m_form_setup(self, form, stage: str):
        """Hook.
        :type form: pytsite.form.Form
        """
        from . import _api
        _assetman.add('pytsite.content@js/content.js')

        current_user = _auth.get_current_user()

        # Title
        form.add_widget(_widget.input.Text(
            uid='title',
            weight=100,
            label=self.t('title'),
            value=self.title,
            required=True,
        ))

        # Description
        form.add_widget(_widget.input.Text(
            uid='description',
            weight=200,
            label=self.t('description'),
            value=self.description,
        ))

        # Tags
        form.add_widget(_taxonomy.widget.TokensInput(
            uid='tags',
            weight=300,
            model='tag',
            label=self.t('tags'),
            value=self.tags,
        ))

        # Images
        if self.has_field('images'):
            from pytsite import image
            form.add_widget(image.widget.ImagesUpload(
                uid='images',
                weight=400,
                label=self.t('images'),
                value=self.f_get('images'),
                max_files=10,
                max_file_size=5,
            ))

        # Video links
        if self.has_field('video_links'):
            form.add_widget(_widget.input.StringList(
                uid='video_links',
                weight=500,
                label=self.t('video'),
                add_btn_label=self.t('add_link'),
                value=self.video_links
            ))
            form.add_rule('video_links', _validation.rule.VideoHostingUrl())

        # Body
        form.add_widget(_ckeditor.widget.CKEditor(
            uid='body',
            weight=600,
            label=self.t('body'),
            value=self.f_get('body', process_tags=False),
        ))
        form.add_rule('body', _validation.rule.NonEmpty())

        # Status
        if current_user.has_permission('pytsite.content.bypass_moderation.' + self.model):
            form.add_widget(_widget.select.Select(
                uid='status',
                weight=700,
                label=self.t('status'),
                value=self.status if self.status else 'published',
                h_size='col-sm-4 col-md-3 col-lg-2',
                items=_api.get_publish_statuses(),
                required=True,
            ))

        # Publish time
        if current_user.has_permission('pytsite.content.set_publish_time.' + self.model):
            form.add_widget(_widget.select.DateTime(
                uid='publish_time',
                weight=800,
                label=self.t('publish_time'),
                value=_datetime.now() if self.is_new else self.publish_time,
                h_size='col-sm-4 col-md-3 col-lg-2',
                required=True,
            ))

        # Language settings
        if current_user.has_permission('pytsite.content.set_localization.' + self.model):
            # Language
            if self.is_new:
                lang_title = _lang.t('lang_title_' + _lang.get_current())
            else:
                lang_title = _lang.t('lang_title_' + self.language)
            form.add_widget(_widget.static.Text(
                uid='language',
                weight=900,
                label=self.t('language'),
                title=lang_title,
                value=_lang.get_current() if self.is_new else self.language,
                hidden=False if len(_lang.langs()) > 1 else True,
            ))

            # Localization selects
            from ._widget import EntitySelect
            for i, lng in enumerate(_lang.langs(False)):
                form.add_widget(EntitySelect(
                    uid='localization_' + lng,
                    weight=1000 + i,
                    label=self.t('localization', {'lang': _lang.lang_title(lng)}),
                    model=self.model,
                    language=lng,
                    value=self.f_get('localization_' + lng)
                ))

        # Visible only for admins
        if _auth.get_current_user().is_admin:
            form.add_widget(_widget.input.Text(
                uid='route_alias',
                weight=1100,
                label=self.t('path'),
                value=self.route_alias.alias if self.route_alias else '',
            ))

            form.add_widget(_auth_ui.widget.UserSelect(
                uid='author',
                weight=1200,
                label=self.t('author'),
                value=_auth.get_current_user() if self.is_new else self.author,
                h_size='col-sm-4',
                required=True,
            ))

    def ui_mass_action_get_entity_description(self) -> str:
        """Get delete form description.
        """
        return self.title

    def _process_body_tags(self, inp: str, responsive: bool, width: int=None) -> str:
        def process_img_tag(match):
            img_index = int(match.group(1))
            if len(self.images) < img_index:
                return ''
            img = self.images[img_index - 1]
            r = img.get_responsive_html(self.title) if responsive else img.get_html(self.title, width=width)
            if match.group(2):
                r = '<a target="_blank" href="{}" title="{}">{}</a>'.format(img.url, _util.escape_html(self.title), r)
            return r

        def process_vid_tag(match):
            vid_index = int(match.group(1))
            if len(self.video_links) < vid_index:
                return ''
            return str(_widget.static.VideoPlayer('content-video-' + str(vid_index),
                                                  value=self.video_links[vid_index - 1]))

        inp = _re.sub('\[img:(\d+)(:link_orig)?\]', process_img_tag, inp)
        inp = _re.sub('\[vid:(\d+)\]', process_vid_tag, inp)

        return inp

    def _extract_body_images(self) -> tuple:
        """Transforms inline <img> tags into [img] tags
        """
        images = list(self.images)
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
                m_to = '{} <{}>'.format(u.full_name, u.email)
                m_subject = _lang.t('pytsite.content@content_waiting_mail_subject', {'app_name': _lang.t('app_name')})
                m_body = _tpl.render('pytsite.content@mail/propose-' + _lang.get_current(), {
                    'user': u,
                    'entity': self,
                })
                _mail.Message(m_to, m_subject, m_body).send()

    def _alter_route_alias_str(self, orig_str: str) -> str:
        """Alter route alias string.
        """
        # Checking original string
        if not orig_str:
            if self.title:
                return self.title
            else:
                raise ValueError('Cannot generate route alias because title is empty.')

        return orig_str


class Page(Content):
    """Page Model.
    """
    pass


class Article(Content):
    """Article Model.
    """
    def _setup(self):
        super()._setup()

        self.define_field(_odm.field.Ref('section', model='section'))
        self.define_field(_odm.field.Bool('starred'))
        self.define_field(_odm.field.StringList('video_links'))
        self.define_field(_odm.field.StringList('ext_links'))

        self.define_field(_geo.field.Location('location'))
        self.define_index([('location.lng_lat', _odm.I_GEO2D)])

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
    def location(self) -> dict:
        return self.f_get('location')

    @classmethod
    def ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        """
        super().ui_browser_setup(browser)
        browser.data_fields = 'title', 'section', 'status', 'images', 'publish_time', 'author'

    def ui_browser_get_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        r = list(super().ui_browser_get_row())
        if self.section:
            r.insert(1, self.section.title)
        else:
            r.insert(1, '')

        return tuple(r)

    def ui_m_form_setup(self, form, stage: str):
        """Hook.
        :type form: pytsite.form.Form
        """
        super().ui_m_form_setup(form, stage)

        # At least one image required
        form.get_widget('images').add_rule(_validation.rule.NonEmpty(msg_id='pytsite.content@image_required'))

        # Starred
        if self.has_field('starred') and _auth.get_current_user().is_admin:
            form.add_widget(_widget.select.Checkbox(
                uid='starred',
                weight=30,
                label=self.t('starred'),
                value=self.starred,
            ))

        # Section
        if self.has_field('section'):
            form.add_widget(_taxonomy.widget.TermSelect(
                uid='section',
                weight=60,
                model='section',
                caption_field='title',
                label=self.t('section'),
                value=self.section,
                h_size='col-sm-6',
                required=True,
            ))

        # External links
        if self.has_field('ext_links'):
            form.add_widget(_widget.input.StringList(
                uid='ext_links',
                weight=630,
                label=self.t('external_links'),
                add_btn_label=self.t('add_link'),
                value=self.ext_links
            ))
            form.add_rule('ext_links', _validation.rule.Url())

        # Location
        if self.has_field('location'):
            form.add_widget(_geo.widget.SearchAddress(
                uid='location',
                weight=660,
                label=self.t('location'),
                value=self.location
            ))

    def _pre_save(self):
        """Hook.
        """
        if self.is_new and self.has_field('section') and self.section and self.tags:
            # Attach section to tags
            for tag in self.tags:
                tag.f_add('sections', self.section).save()

        super()._pre_save()

    def _alter_route_alias_str(self, orig_str: str) -> str:
        """Alter route alias string.
        """
        orig_str = super()._alter_route_alias_str(orig_str)

        # Prefix given article title with section title if it exists.
        # Do this work ONLY if title doesn't look like correct path alias string.
        if self.section and not _re.search('^/?[a-z0-9\-]+/[a-z0-9\-]+', orig_str, _re.IGNORECASE):
            return '{}/{}'.format(self.section.alias, orig_str)

        return orig_str


class ContentSubscriber(_odm.Model):
    """content_subscriber ODM Model.
    """
    def _setup(self):
        """Hook.
        """
        self.define_field(_odm.field.String('email', nonempty=True))
        self.define_field(_odm.field.Bool('enabled', default=True))
        self.define_field(_odm.field.String('language', nonempty=True))

        self.define_index([('email', _odm.I_ASC), ('language', _odm.I_ASC)], unique=True)

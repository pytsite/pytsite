"""Content Models
"""
import re as _re
from typing import Tuple as _Tuple, Union as _Union
from datetime import datetime as _datetime, timedelta as _timedelta
from frozendict import frozendict as _frozendict
from pytsite import auth as _auth, taxonomy as _taxonomy, odm_ui as _odm_ui, route_alias as _route_alias, \
    file as _file, ckeditor as _ckeditor, odm as _odm, widget as _widget, validation as _validation, \
    html as _html, router as _router, lang as _lang, assetman as _assetman, events as _events, mail as _mail, \
    tpl as _tpl, util as _util, form as _form, reg as _reg, comments as _comments, errors as _errors, \
    auth_storage_odm as _auth_storage_odm, file_storage_odm as _file_storage_odm


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_localization_enabled = _reg.get('content.localization', True)
_body_img_tag_re = _re.compile('\[img:(\d+)([^\]]*)\]')
_body_vid_tag_re = _re.compile('\[vid:(\d+)\]')
_html_img_tag_re = _re.compile('<img.*?src\s*=["\']([^"\']+)["\'][^>]*>')
_html_video_youtube_re = _re.compile(
    '<iframe.*?src=["\']?https?://www\.youtube\.com/embed/([a-zA-Z0-9_-]{11})[^"\']*["\']?.+?</iframe>'
)
_html_video_facebook_re = _re.compile(
    '<iframe.*?src=["\']?https?://www\.facebook\.com/plugins/video\.php\?href=([^"\']+)["\']?.+?</iframe>'
)


def _process_tags(entity, inp: str) -> str:
    """Converts body tags like [img] into HTML tags.

    :type entity: _Union[Block, Content]
    """
    entity_images = entity.images if entity.has_field('images') else ()
    entity_images_count = len(entity_images)

    def process_img_tag(match):
        """Converts single body [img] tag into HTML <img> tag.
        """
        # Image index
        img_index = int(match.group(1))

        # Does image exist?
        if entity_images_count < img_index:
            return ''

        img = entity_images[img_index - 1]

        # Additional parameters defaults
        link_orig = False
        link_target = '_blank'
        link_class = ''
        img_css = ''
        enlarge = True
        alt = entity.title if entity.has_field('title') else ''
        width = 0
        height = 0
        responsive = True

        for arg in match.group(2).split(':'):  # type: str
            arg = arg.strip()
            if arg in ('link_orig', 'link'):
                link_orig = True
            elif arg.startswith('link_target='):
                link_target = arg.split('=')[1]
            elif arg.startswith('link_class='):
                link_class = arg.split('=')[1]
            elif arg in ('skip_enlarge', 'no_enlarge'):
                enlarge = False
            elif arg.startswith('class='):
                img_css = arg.split('=')[1]
            elif arg.startswith('alt='):
                alt = arg.split('=')[1]
            elif arg.startswith('width='):
                responsive = False
                try:
                    width = int(arg.split('=')[1])
                except ValueError:
                    width = 0
            elif arg.startswith('height='):
                responsive = False
                try:
                    height = int(arg.split('=')[1])
                except ValueError:
                    height = 0

        # HTML code
        if responsive:
            r = img.get_responsive_html(alt, enlarge=enlarge, css=_util.escape_html(img_css))
        else:
            r = img.get_html(alt, width=width, height=height, enlarge=enlarge, css=_util.escape_html(img_css))

        # Link to original file
        if link_orig:
            link = _html.A(r, href=img.url, target=link_target, title=_util.escape_html(alt))
            if link_class:
                link.set_attr('cls', _util.escape_html(link_class))

            r = str(link)

        return r

    def process_vid_tag(match):
        """Converts single body [vid] tag into video player HTML code.
        """
        vid_index = int(match.group(1))
        if len(entity.video_links) < vid_index:
            return ''

        return str(_widget.misc.VideoPlayer('content-video-' + str(vid_index), value=entity.video_links[vid_index - 1]))

    inp = _body_img_tag_re.sub(process_img_tag, inp)
    inp = _body_vid_tag_re.sub(process_vid_tag, inp)

    return inp


def _extract_images(entity) -> tuple:
    """Transforms inline HTML <img> tags into [img] tags.

    :type entity: Base
    """
    if not entity.author:
        raise RuntimeError('Entity author must be set before ')

    # Existing images count
    img_index = len(entity.images)

    # Extracted images
    images = []

    def replace_func(match):
        nonlocal img_index, images
        img_index += 1
        images.append(_file.create(match.group(1)))

        return '[img:{}]'.format(img_index)

    body = _html_img_tag_re.sub(replace_func, entity.body)

    return body, images


def _extract_video_links(entity) -> tuple:
    """Transforms embedded video players code into [vid] tags.

    :type entity: Base
    """
    # Existing video links count
    vid_index = len(entity.video_links)

    vid_links = []

    def replace_func(match):
        nonlocal vid_index, vid_links
        vid_index += 1

        if 'youtube' in match.group(0):
            vid_links.append('https://youtu.be/' + match.group(1))
        elif 'facebook' in match.group(0):
            link = _re.sub('&.+$', '', _util.url_unquote(match.group(1)))
            vid_links.append(link)

        return '[vid:{}]'.format(vid_index)

    body = entity.f_get('body', process_tags=False)
    body = _html_video_youtube_re.sub(replace_func, body)
    body = _html_video_facebook_re.sub(replace_func, body)

    return body, vid_links


def _remove_tags(s: str) -> str:
    s = _body_img_tag_re.sub('', s)
    s = _body_vid_tag_re.sub('', s)
    return s


class Section(_taxonomy.model.Term):
    """Section Model.
    """

    def _pre_delete(self, **kwargs):
        from . import _api

        # Search for content entities which use this section
        for content_model in _api.get_models():
            f = _api.find(content_model, status=None, check_publish_time=False)
            if not f.mock.has_field('section'):
                continue
            r_entity = f.eq('section', self).first()
            if r_entity:
                error_args = {'model': r_entity.model, 'title': r_entity.f_get('title')}
                raise _errors.ForbidDeletion(_lang.t('pytsite.content@referenced_entity_exists', error_args))

        # Search for tags which use this section
        f = _taxonomy.find('tag')
        if f.mock.has_field('sections'):
            tag = f.inc('sections', [self]).first()
            if tag:
                error_args = {'model': tag.model, 'title': tag.f_get('title')}
                raise _errors.ForbidDeletion(_lang.t('pytsite.content@referenced_entity_exists', error_args))


class Tag(_taxonomy.model.Term):
    """Tag Model.
    """

    def _setup_fields(self):
        """Hook.
        """
        super()._setup_fields()
        self.define_field(_odm.field.RefsUniqueList('sections', model='section'))

    @classmethod
    def odm_ui_browser_setup(cls, browser: _odm_ui.Browser):
        """Hook.
        """
        super().odm_ui_browser_setup(browser)
        browser.default_sort_field = 'weight'
        browser.default_sort_order = _odm.I_DESC


class Base(_odm_ui.model.UIEntity):
    """Base Content Model.

    Just minimum amount of fields.
    """

    @classmethod
    def odm_auth_permissions_group(cls) -> str:
        return 'content'

    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('title', required=True, strip_html=True))
        self.define_field(_odm.field.String('body', tidyfy_html=True))
        self.define_field(_file_storage_odm.field.Images('images'))
        self.define_field(_odm.field.StringList('video_links', unique=True))
        self.define_field(_odm.field.String('language', required=True, default=_lang.get_primary()))
        self.define_field(_odm.field.String('language_db', required=True))
        self.define_field(_auth_storage_odm.field.User('author', required=True))
        self.define_field(_odm.field.Dict('options'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('_created', _odm.I_DESC)])
        self.define_index([('_modified', _odm.I_DESC)])
        self.define_index([('title', _odm.I_ASC)])

        if self.has_field('author'):
            self.define_index([('author', _odm.I_ASC)])

        if self.has_field('video_links'):
            self.define_index([('video_links', _odm.I_ASC)])

    @property
    def title(self) -> str:
        """Title getter.
        """
        return self.f_get('title')

    @property
    def body(self) -> str:
        """Body getter.
        """
        return self.f_get('body', process_tags=True)

    @property
    def images(self) -> _Tuple[_file.model.AbstractImage]:
        """Images getter.
        """
        return self.f_get('images')

    @property
    def video_links(self) -> tuple:
        """Video links getter.
        """
        return self.f_get('video_links')

    @property
    def language(self) -> str:
        """Language getter.
        """
        return self.f_get('language')

    @property
    def author(self) -> _auth.model.AbstractUser:
        """Author getter.
        """
        return self.f_get('author')

    @property
    def options(self) -> _frozendict:
        """Options getter.
        """
        return self.f_get('options')

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'body':
            if kwargs.get('process_tags'):
                value = _process_tags(self, value)
            elif kwargs.get('remove_tags'):
                value = _remove_tags(value)

            return value

        return value

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'language':
            if value not in _lang.langs():
                raise ValueError("Language '{}' is not supported.".format(value))

            if value == 'en':
                self.f_set('language_db', 'english')
            elif value == 'ru':
                self.f_set('language_db', 'russian')
            else:
                self.f_set('language_db', 'none')

        return super()._on_f_set(field_name, value, **kwargs)

    def _pre_save(self, **kwargs):
        """Hook.
        """
        super()._pre_save(**kwargs)

        current_user = _auth.get_current_user()

        # Language is required
        if not self.language or not self.f_get('language_db'):
            self.f_set('language', _lang.get_current())

        # If author is required
        if self.has_field('author') and self.get_field('author').required and not self.author:
            if not current_user.is_anonymous:
                self.f_set('author', current_user)
            else:
                raise RuntimeError('Cannot assign author, because current user is anonymous.')

        # Extract inline images from the body
        if self.has_field('body') and self.has_field('images'):
            body, images = _extract_images(self)

            # If new images has been extracted
            if images:
                self.f_set('body', body)
                self.f_set('images', list(self.images) + images)

        # Extract inline videos from the body
        if self.has_field('body') and self.has_field('video_links'):
            body, video_links = _extract_video_links(self)

            # If new video links has been extracted
            if video_links:
                self.f_set('body', body)
                self.f_set('video_links', list(self.video_links) + video_links)

        _events.fire('pytsite.content.entity.pre_save', entity=self)
        _events.fire('pytsite.content.entity.{}.pre_save.'.format(self.model), entity=self)

    def _after_save(self, first_save: bool = False, **kwargs):
        """Hook.
        """
        _events.fire('pytsite.content.entity.save', entity=self)
        _events.fire('pytsite.content.entity.{}.save'.format(self.model), entity=self)

    def _after_delete(self, **kwargs):
        """Hook.
        """
        # Delete all attached images
        if self.has_field('images'):
            for img in self.images:
                img.delete()

    @classmethod
    def odm_ui_browser_setup(cls, browser: _odm_ui.Browser):
        """Setup ODM UI browser hook.
        """
        # Filter by language
        if _localization_enabled:
            browser.finder_adjust = lambda f: f.eq('language', _lang.get_current())

        browser.default_sort_field = '_modified'
        browser.insert_data_field('title', 'pytsite.content@title')

    def odm_ui_browser_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return self.title,

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        # Title
        frm.add_widget(_widget.input.Text(
            uid='title',
            weight=200,
            label=self.t('title'),
            value=self.title,
            required=True,
        ))

        # Images
        if self.has_field('images'):
            frm.add_widget(_file.widget.ImagesUpload(
                uid='images',
                weight=400,
                label=self.t('images'),
                value=self.f_get('images'),
                max_file_size=5,
                max_files=50,
            ))
            if self.get_field('images').required:
                frm.add_rule('images', _validation.rule.NonEmpty())

        # Video links
        if self.has_field('video_links'):
            frm.add_widget(_widget.input.StringList(
                uid='video_links',
                weight=600,
                label=self.t('video'),
                add_btn_label=self.t('add_link'),
                value=self.video_links,
                unique=True,
            ))
            frm.add_rule('video_links', _validation.rule.VideoHostingUrl())

        # Body
        if self.has_field('body'):
            frm.add_widget(_ckeditor.widget.CKEditor(
                uid='body',
                weight=800,
                label=self.t('body'),
                value=self.f_get('body', process_tags=False),
            ))
            if self.get_field('body').required:
                frm.add_rule('body', _validation.rule.NonEmpty())

        # Visible only for admins
        if _auth.get_current_user().is_admin:
            # Author
            if self.has_field('author'):
                frm.add_widget(_auth.widget.UserSelect(
                    uid='author',
                    weight=1000,
                    label=self.t('author'),
                    value=_auth.get_current_user() if self.is_new else self.author,
                    h_size='col-sm-4',
                    required=True,
                ))

    def odm_ui_mass_action_entity_description(self) -> str:
        """Get delete form description.
        """
        return self.title

    def as_jsonable(self, **kwargs) -> dict:
        r = super().as_jsonable()

        r.update({
            'title': self.title,
            'language': self.language,
            'options': dict(self.options),
        })

        if self.has_field('images'):
            img_jsonable_args = {
                'thumb_width': kwargs.get('images_thumb_width', 450),
                'thumb_height': kwargs.get('images_thumb_height', 450),
            }
            r['images'] = [img.as_jsonable(**img_jsonable_args) for img in self.images]

        if self.has_field('video_links'):
            r['video_links'] = self.video_links

        if self.has_field('body'):
            r['body'] = self.body

        if self.has_field('author'):
            r['author'] = self.author.as_jsonable()

        return r


class Content(Base):
    """Content Model.
    """

    def _setup_fields(self):
        """Hook.
        """
        super()._setup_fields()

        self.define_field(_odm.field.Ref('route_alias', model='route_alias', required=True))
        self.define_field(_odm.field.String('status', required=True, default='waiting'))
        self.define_field(_odm.field.String('description', strip_html=True))
        self.define_field(_odm.field.DateTime('publish_time', default=_datetime.now()))
        self.define_field(_odm.field.RefsUniqueList('tags', model='tag'))
        self.define_field(_odm.field.Ref('section', model='section'))
        self.define_field(_odm.field.Bool('starred'))
        self.define_field(_odm.field.Integer('views_count'))
        self.define_field(_odm.field.Integer('comments_count'))
        self.define_field(_odm.field.StringList('ext_links', unique=True))

        for lng in _lang.langs():
            self.define_field(_odm.field.Ref('localization_' + lng, model=self.model))

    def _setup_indexes(self):
        """Hook.
        """
        super()._setup_indexes()

        if self.has_field('ext_links'):
            self.define_index([('ext_links', _odm.I_ASC)])

        if self.has_field('publish_time'):
            self.define_index([('publish_time', _odm.I_DESC)])

        # Text index
        if self.has_field('description') and self.has_field('body'):
            self.define_index([('title', _odm.I_TEXT), ('description', _odm.I_TEXT), ('body', _odm.I_TEXT)])
        elif self.has_field('description'):
            self.define_index([('title', _odm.I_TEXT), ('description', _odm.I_TEXT)])
        elif self.has_field('body'):
            self.define_index([('title', _odm.I_TEXT), ('body', _odm.I_TEXT)])

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def tags(self) -> _Tuple[Tag]:
        return self.f_get('tags', sort_by='weight', sort_reverse=True)

    def odm_ui_m_form_url(self, args: dict = None) -> str:
        return _router.ep_url('pytsite.content@modify', {
            'model': self.model,
            'id': '0' if self.is_new else str(self.id),
            '__redirect': 'ENTITY_VIEW',
        })

    def odm_ui_view_url(self) -> str:
        if self.is_new:
            raise RuntimeError("Cannot generate view URL for non-saved entity of model '{}'.".format(self.model))

        target_path = _router.ep_path('pytsite.content@view', {'model': self.model, 'id': str(self.id)})
        r_alias = _route_alias.get_by_target(target_path, self.language)
        value = r_alias.alias if r_alias else target_path

        return _router.url(value, lang=self.language)

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
    def status(self) -> str:
        return self.f_get('status')

    @property
    def publish_time(self) -> _datetime:
        return self.f_get('publish_time')

    @property
    def publish_date_time_pretty(self) -> str:
        return self.f_get('publish_time', fmt='pretty_date_time')

    @property
    def publish_date_pretty(self) -> str:
        return self.f_get('publish_time', fmt='pretty_date')

    @property
    def publish_time_ago(self) -> str:
        return self.f_get('publish_time', fmt='ago')

    @property
    def starred(self) -> bool:
        return self.f_get('starred')

    @property
    def section(self) -> Section:
        return self.f_get('section')

    @property
    def ext_links(self) -> _Tuple[str]:
        return self.f_get('ext_links')

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'route_alias' and (isinstance(value, str) or value is None):
            if value is None:
                value = ''

            # Delegate string generation to dedicated hook
            route_alias_str = self._alter_route_alias_str(value.strip())

            # No route alias is attached, so we need to create a new one
            if not self.route_alias:
                value = _route_alias.create(route_alias_str, 'NONE', self.language).save()

            # Existing route alias is attached and its value needs to be changed
            elif self.route_alias and self.route_alias.alias != route_alias_str:
                with self.route_alias:
                    self.route_alias.delete()
                value = _route_alias.create(route_alias_str, 'NONE', self.language).save()

            # Keep old route alias
            else:
                value = self.route_alias

        elif field_name == 'status':
            from ._api import get_statuses
            if value not in [v[0] for v in get_statuses()]:
                raise RuntimeError("Invalid publish status: '{}'.".format(value))

        return super()._on_f_set(field_name, value, **kwargs)

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'tags' and kwargs.get('as_string'):
            return ','.join([tag.title for tag in self.f_get('tags')])
        else:
            return super()._on_f_get(field_name, value, **kwargs)

    def _pre_save(self, **kwargs):
        """Hook.
        """
        super()._pre_save(**kwargs)

        # Route alias is required
        if not self.route_alias:
            # Setting None leads to route alias auto-generation
            self.f_set('route_alias', None)

        if self.is_new:
            # Attach section to tags
            if self.has_field('section') and self.section and self.tags:
                for tag in self.tags:
                    with tag:
                        _auth.switch_user_to_system()
                        tag.f_add('sections', self.section).save()
                        _auth.restore_user()

    def _after_save(self, first_save: bool = False, **kwargs):
        """Hook.
        """
        super()._after_save(first_save, **kwargs)

        # Update route alias target which has been created in self._pre_save()
        if self.route_alias.target == 'NONE':
            with self.route_alias:
                target = _router.ep_path('pytsite.content@view', {'model': self.model, 'id': self.id})
                self.route_alias.f_set('target', target).save()

        if first_save:
            # Clean up not fully filled route aliases
            f = _route_alias.find()
            f.eq('target', 'NONE').lt('_created', _datetime.now() - _timedelta(1))
            for ra in f.get():
                with ra:
                    ra.delete()

            # Notify content moderators about waiting content
            if self.status == 'waiting' and _reg.get('content.send_waiting_notifications', True):
                self._send_waiting_status_notification()

            # Recalculate tags weights
            from . import _api
            if self.has_field('tags'):
                for tag in self.tags:
                    with tag:
                        weight = 0
                        for model in _api.get_models().keys():
                            weight += _api.find(model, language=self.language).inc('tags', [tag]).count()

                        _auth.switch_user_to_system()
                        tag.f_set('weight', weight).save()
                        _auth.restore_user()

        # Updating localization entities references.
        # For each language except current one
        from . import _api
        for lng in _lang.langs(False):
            # Get localization ref for lng
            localization = self.f_get('localization_' + lng)

            # If localization is set
            if isinstance(localization, Content):
                # If localized entity hasn't reference to this entity, set it
                if localization.f_get('localization_' + self.language) != self:
                    with localization:
                        localization.f_set('localization_' + self.language, self).save()

            # If localization is not set
            elif localization is None:
                # Clear references from localized entities
                f = _api.find(self.model, language=lng).eq('localization_' + self.language, self)
                for referenced in f.get():
                    with referenced:
                        referenced.f_set('localization_' + self.language, None).save()

    def _after_delete(self, **kwargs):
        """Hook.
        """
        super()._after_delete()

        # Disable permissions check
        _auth.switch_user_to_system()

        # Delete comments
        try:
            _comments.delete_thread(self.route_alias.alias)
        except NotImplementedError:
            pass

        # Enable permissions check
        _auth.restore_user()

        # Delete linked route alias
        with self.route_alias:
            self.route_alias.delete()

    @classmethod
    def odm_ui_browser_setup(cls, browser: _odm_ui.Browser):
        """Setup ODM UI browser hook.
        """
        super().odm_ui_browser_setup(browser)

        mock = _odm.dispense(browser.model)

        # Sort field
        if mock.has_field('publish_time'):
            browser.default_sort_field = 'publish_time'
            browser.default_sort_order = 'desc'

        # Section
        if mock.has_field('section'):
            browser.insert_data_field('section', 'pytsite.content@section')

        # Starred
        if mock.has_field('starred'):
            browser.insert_data_field('starred', 'pytsite.content@starred')

        # Status
        if mock.has_field('status'):
            browser.insert_data_field('status', 'pytsite.content@status')

        # Images
        if mock.has_field('images'):
            browser.insert_data_field('images', 'pytsite.content@images')

        # Publish time
        if mock.has_field('publish_time'):
            browser.insert_data_field('publish_time', 'pytsite.content@publish_time')

        # Author
        if mock.has_field('author'):
            browser.insert_data_field('author', 'pytsite.content@author')

    def odm_ui_browser_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        # Title
        r = [str(_html.A(self.title, href=self.url))]

        # Section
        if self.has_field('section'):
            r.append(self.section.title if self.section else '&nbsp;')

        # Starred
        if self.has_field('starred'):
            # 'Starred' flag
            if self.starred:
                starred = '<span class="label label-primary">{}</span>'.format(_lang.t('pytsite.content@word_yes'))
            else:
                starred = '&nbsp;'
            r.append(starred)

        # Status
        if self.has_field('status'):
            status = self.status
            status_str = self.t('status_' + status)
            status_cls = 'primary'
            if status == 'waiting':
                status_cls = 'warning'
            elif status == 'unpublished':
                status_cls = 'default'
            status = str(_html.Span(status_str, cls='label label-' + status_cls))
            r.append(status)

        # Images counter
        if self.has_field('images'):
            images_cls = 'default' if not len(self.images) else 'primary'
            images_count = '<span class="label label-{}">{}</span>'.format(images_cls, len(self.images))
            r.append(images_count)

        # Publish time
        if self.has_field('publish_time'):
            r.append(self.f_get('publish_time', fmt='%d.%m.%Y %H:%M'))

        # Author
        if self.has_field('author'):
            r.append(self.author.full_name if self.author else '&nbsp;')

        return tuple(r)

    def odm_ui_m_form_setup(self, frm: _form.Form):
        """Hook.
        """
        _assetman.add('pytsite.content@js/content.js')

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        super().odm_ui_m_form_setup_widgets(frm)

        current_user = _auth.get_current_user()

        # Starred
        if self.has_field('starred') and current_user.has_permission('pytsite.content.set_starred.' + self.model):
            frm.add_widget(_widget.select.Checkbox(
                uid='starred',
                weight=100,
                label=self.t('starred'),
                value=self.starred,
            ))

        # Section
        if self.has_field('section'):
            from ._widget import SectionSelect
            frm.add_widget(SectionSelect(
                uid='section',
                weight=150,
                label=self.t('section'),
                value=self.section,
                h_size='col-sm-6',
                required=True,
            ))

        # Description
        if self.has_field('description'):
            frm.add_widget(_widget.input.Text(
                uid='description',
                weight=300,
                label=self.t('description'),
                value=self.description,
            ))

        # Tags
        if self.has_field('tags'):
            frm.add_widget(_taxonomy.widget.TokensInput(
                uid='tags',
                weight=350,
                model='tag',
                label=self.t('tags'),
                value=self.tags,
            ))

        # External links
        if self.has_field('ext_links'):
            frm.add_widget(_widget.input.StringList(
                uid='ext_links',
                weight=900,
                label=self.t('external_links'),
                add_btn_label=self.t('add_link'),
                value=self.ext_links,
                unique=True,
            ))
            frm.add_rule('ext_links', _validation.rule.Url())

        # Status
        if self.has_field('status') and current_user.has_permission('pytsite.content.bypass_moderation.' + self.model):
            from ._widget import StatusSelect
            frm.add_widget(StatusSelect(
                uid='status',
                weight=950,
                label=self.t('status'),
                value='published' if self.is_new else self.status,
                h_size='col-sm-4 col-md-3 col-lg-2',
                required=True,
            ))

        # Publish time
        if self.has_field('publish_time'):
            if current_user.has_permission('pytsite.content.set_publish_time.' + self.model):
                frm.add_widget(_widget.select.DateTime(
                    uid='publish_time',
                    weight=975,
                    label=self.t('publish_time'),
                    value=_datetime.now() if self.is_new else self.publish_time,
                    h_size='col-sm-4 col-md-3 col-lg-2',
                    required=True,
                ))

        # Language settings
        if _localization_enabled and current_user.has_permission('pytsite.content.set_localization.' + self.model):
            # Current language
            if self.is_new:
                lang_title = _lang.t('lang_title_' + _lang.get_current())
            else:
                lang_title = _lang.t('lang_title_' + self.language)
            frm.add_widget(_widget.static.Text(
                uid='language',
                weight=1200,
                label=self.t('language'),
                title=lang_title,
                value=_lang.get_current() if self.is_new else self.language,
                hidden=False if len(_lang.langs()) > 1 else True,
            ))

            # Localization selects
            from ._widget import EntitySelect
            for i, lng in enumerate(_lang.langs(False)):
                frm.add_widget(EntitySelect(
                    uid='localization_' + lng,
                    weight=1200 + i,
                    label=self.t('localization', {'lang': _lang.lang_title(lng)}),
                    model=self.model,
                    language=lng,
                    value=self.f_get('localization_' + lng)
                ))

        # Visible only for admins
        if _auth.get_current_user().is_admin:
            # Route alias
            frm.add_widget(_widget.input.Text(
                uid='route_alias',
                weight=1400,
                label=self.t('path'),
                value=self.route_alias.alias if self.route_alias else '',
                enabled=not self.comments_count,
            ))

    def _send_waiting_status_notification(self):
        for u in _auth.get_users():
            if u.has_permission('pytsite.odm_perm.modify.' + self.model):
                m_subject = _lang.t('pytsite.content@content_waiting_mail_subject', {'app_name': _lang.t('app_name')})
                m_body = _tpl.render('pytsite.content@mail/{}/propose'.format(_lang.get_current()), {
                    'user': u,
                    'entity': self,
                })
                _mail.Message(u.email, m_subject, m_body).send()

    def _alter_route_alias_str(self, orig_str: str) -> str:
        """Alter route alias string.
        """
        # Checking original string
        if not orig_str:
            # Route alias string generation is possible only if entity's title is not empty
            if self.title:
                orig_str = self.title
                if self.has_field('section') and self.section:
                    # If 'section' field exists and section is selected, use its alias
                    orig_str = '{}/{}'.format(self.section.alias, orig_str)
                else:
                    # Otherwise use model name
                    orig_str = '{}/{}'.format(self.model, orig_str)
            else:
                # Without entity's title we cannot construct route alias string
                raise RuntimeError('Cannot generate route alias because title is empty.')

        return orig_str

    def as_jsonable(self, **kwargs):
        r = super().as_jsonable(**kwargs)

        r['route_alias'] = self.route_alias.as_jsonable()

        if self.has_field('starred'):
            r['starred'] = self.starred
        if self.has_field('section'):
            r['section'] = self.section.as_jsonable()
        if self.has_field('description'):
            r['description'] = self.description
        if self.has_field('tags'):
            r['tags'] = [tag.as_jsonable() for tag in self.tags]
        if self.has_field('ext_links'):
            r['ext_links'] = self.ext_links
        if self.has_field('status'):
            r['status'] = self.status
        if self.has_field('publish_time'):
            r['publish_time'] = {
                'w3c': _util.w3c_datetime_str(self.publish_time),
                'pretty_date': self.publish_date_pretty,
                'pretty_date_time': self.publish_date_time_pretty,
                'ago': self.publish_time_ago,
            }
        if self.has_field('views_count'):
            r['views_count'] = self.views_count
        if self.has_field('comments_count'):
            r['comments_count'] = self.comments_count

        if _localization_enabled:
            for lng in _lang.langs():
                if self.has_field('localization_' + lng):
                    ref = self.f_get('localization_' + lng)
                    if ref:
                        r['localization_' + lng] = ref.as_jsonable(**kwargs)

        return r


class Page(Content):
    """Page Model.
    """

    def _setup_fields(self):
        """Hook.
        """
        super()._setup_fields()

        self.get_field('body').required = True

        self.remove_field('section')
        self.remove_field('starred')


class Article(Content):
    """Article Model.
    """

    def _setup_fields(self):
        super()._setup_fields()

        self.get_field('images').required = True
        self.get_field('body').required = True


class ContentSubscriber(_odm.model.Entity):
    """content_subscriber ODM Model.
    """

    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('email', required=True))
        self.define_field(_odm.field.Bool('enabled', default=True))
        self.define_field(_odm.field.String('language', required=True))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('email', _odm.I_ASC), ('language', _odm.I_ASC)], unique=True)

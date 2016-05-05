"""LiveJournal content_export's Driver.
"""
from frozendict import frozendict as _frozendict
from pytsite import content_export as _content_export, widget as _widget, html as _html, lang as _lang, \
    assetman as _assetman, util as _util, logger as _logger
from ._session import Session as _Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _SettingsWidget(_widget.Base):
    """LiveJournal content_export Settings Widget.
     """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._css += ' widget-content-export-lj-settings'
        self._username = kwargs.get('username', '')
        self._password = kwargs.get('password', '')
        self._lj_like = kwargs.get('lj_like', 'fb,tw,go,vk,lj')

        _assetman.add('pytsite.lj@js/content-export-settings.js')

    def get_html_em(self, **kwargs) -> _html.Element:
        """Get HTML element of the widget.
        :param **kwargs:
        """
        wrapper = _widget.Container(uid=self._uid)

        wrapper.add_widget(_widget.input.Text(
            weight=10,
            uid='{}[username]'.format(self._uid),
            label=_lang.t('pytsite.lj@username'),
            required=True,
            value=self._username,
        ))

        wrapper.add_widget(_widget.input.Password(
            uid='{}[password]'.format(self._uid),
            weight=20,
            label=_lang.t('pytsite.lj@password'),
            required=True,
            value=self._password,
        ))

        wrapper.add_widget(_widget.input.Text(
            uid='{}[lj_like]'.format(self._uid),
            weight=30,
            label=_lang.t('pytsite.lj@lj_like_buttons'),
            help=_lang.t('pytsite.lj@lj_like_buttons_help'),
            value=self._lj_like,
        ))

        wrapper.add_widget(_widget.input.Hidden(
            weight=40,
            uid='title',
            name='{}[title]'.format(self._uid),
            required=True,
            value=self._title,
        ))

        return self._group_wrap(wrapper)


class Driver(_content_export.AbstractDriver):
    """LiveJournal content_export Driver.
    """
    def get_name(self) -> str:
        """Get system name of the driver.
        """
        return 'lj'

    def get_description(self) -> str:
        """Get human readable description of the driver.
        """
        return 'pytsite.lj@livejournal'

    def get_options_description(self, driver_options: _frozendict) -> str:
        """Get human readable driver options.
        """
        return driver_options.get('username')

    def get_settings_widget(self, driver_opts: _frozendict) -> _widget.Base:
        """Add widgets to the settings form of the driver.
        """
        return _SettingsWidget(
            uid='driver_opts',
            username=driver_opts.get('username'),
            password=driver_opts.get('password'),
            lj_like=driver_opts.get('lj_like', 'fb,tw,go,vk,lj'),
        )

    def export(self, entity, exporter):
        """Performs export.

        :type entity: pytsite.content._model.Content
        :type exporter: pytsite.content_export._model.ContentExport
        """
        try:
            _logger.info("Export started. '{}'".format(entity.title), __name__)

            tags = exporter.add_tags + tuple([tag.title for tag in entity.tags])
            opts = exporter.driver_opts

            msg = ''
            if entity.has_field('images') and entity.images:
                img_url = entity.images[0].get_url(1024)
                msg += '<p><a href="{}"><img src="{}" title="{}"></a></p>'.format(entity.url, img_url, entity.title)

            msg += '<p>{}: <a href="{}">{}</a></p>'.format(
                    _lang.t('pytsite.lj@source', language=entity.language), entity.url, entity.url)
            if entity.description:
                msg += '<p>{}</p>'.format(entity.description)
            msg += '<lj-cut>'
            msg += _util.trim_str(entity.f_get('body', process_tags=True, responsive=False), 64000, True)
            msg += '</lj-cut>'
            if opts['lj_like']:
                msg += '<lj-like buttons="{}">'.format(opts['lj_like'])

            s = _Session(opts['username'], opts['password'])
            r = s.post_event(entity.title[:255], msg, tags, entity.publish_time)

            _logger.info("Export finished. '{}'. LJ response: {}".format(entity.title, r), __name__)

        except Exception as e:
            raise _content_export.error.ExportError(e)

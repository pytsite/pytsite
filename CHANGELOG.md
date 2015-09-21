# PytSite Changelog

## 0.18.2 (2015-09-21)
### Fixed
- Quotes escaping in `image.model.Image.get_html()` and `browser`'s `responsive` lib.


## 0.18.1 (2015-09-21)
### Added
- `css` argument in `image.model.Image.get_html()`.


## 0.18 (2015-09-21)
### Added
- `responsive` library in `browser`.
- `image.model.Image.get_html()` method.


## 0.17 (2015-09-20)
### Added
- Jinja blocks markup in `auth_ui.widget.Profile`'s base template and its rework.
- `col_image_css` and `col_content_css` arguments in `auth_ui.widget.Profile`.
- `followers` and `follows` fields in `auth.model.User`.
- `weight` and `forever` arguments in `assetman.add()`.s
- `forever` argument in `browser.include()`.
- New widget: `ath_ui.widget.Follow`.
- Safety checking before deletion of `auth.model.User` and `auth.model.Role`.

### Changed
- `admin.eps` renamed to `admin.ep`.
- `auth_ui.eps` renamed to `auth_ui.ep`.
- `image.widget.ImagesUploadWidget` renamed to `image.widget.ImagesUpload`.

### Fixed
- Error while generating `content`'s RSS and Atom feeds.


## 0.16 (2015-09-17)
### Added
- `enabled` and `errors` fields in `content_export.model.ContentExport`.
- Erroneously content exporters automatically will be automatically disabled.


## 0.15.3 (2015-09-17)
### Added
- `exc_info` argument in `logger.error()`.

## 0.15.2 (2015-09-17)
### Fixed
- Exception handling in `twitter`'s content export driver.


## 0.15.1 (2015-09-17)
### Fixed
- Exception handling in `twitter`'s content export driver.


## 0.15 (2015-09-17)
### Added
- New properties `can_be_modified` and `can_be_deleted` in `odm_ui.Model`.
- New method `odm_ui.Model.get_delete_url()`

### Changed
- `author` argument of the `content:generate` console command is now optional.

### Fixed
- Exception handling from drivers of the `content_export`.


## 0.14.4 (2015-09-15)
### Added
- New argument `wrap` in `taxonomy.widget.Cloud`.

### Fixed
- Erroneous second call to final endpoints in `browser`.


## 0.14.3 (2015-09-14)
### Fixed
- Incorrect usage of `css` argument in some forms.


## 0.14.2 (2015-09-14)
### Fixed
- Small fix in `admin` and related packages.


## 0.14.1 (2015-09-14)
### Fixed
- Errors in JS initialization of `widget.input.TypeaheadText`.


## 0.14 (2015-09-12)
### Added
- Set `nickname` field's value of the `auth.model.User` in `auth.driver.ulogin` 

### Fixed
- Errors in `db`'s console commands.
- Error in `auth`'s `setup` event handler.

### Changed
- `auth.allow_signup` configuration parameter renamed to `auth.signup.enabled`.
- `auth.signup_roles` configuration parameter renamed to `auth.signup.roles`.
- `widget.Base.cls` renamed to `widget.Base.css`.
- `widget.Base.group_cls` removed in favour of `widget.Base.css`.
- `file.widget.File.slot_cls` renamed to `file.widget.File.slot_css`.
- `taxonomy.widget.Cloud.terms` now returns  list instead of iterator.
- `taxonomy.widget.Cloud.title_pattern` renamed to `taxonomy.widget.Cloud.term_title_pattern`.
- `content.widget.SearchInput` renamed to `content.widget.Search`.
- `auth_ui.widget.Profile` improved.
- `content.widget.Search` improved.


## 0.13 (2015-09-10)
### Added
- `description` and `nickname` fields in `auth.model.User`.
- `validation.rule.Regex` rule.

### Changed
- Some changes in layout of the `auth_ui.widget.Profile`.

### Fixed
- Various validations in `auth_ui.model.UserUI`.


## 0.12.1 (2015-09-09)
### Added
- `flag.widget` initialization via JS API. 

### Changed
- Bilinear algorithm is now the default while resizing images in `image.ep.resize()`. 

## 0.12 (2015-09-09)
### Added
- Passing `_name` and `_call` arguments to routes.
- New event: `pytsite.auth.user.create`.

### Changed
- `login` and `email` arguments of the `auth.crate_user()` function have been swapped out


## 0.11.5 (2015-09-07)
### Added
- Ability to specify modules to autoload in application config file.

### Changed
- `auth.eps` renamed to `auth.ep`.


## 0.11.4 (2015-09-07)
### Added
- New widget: `geo.widget.LatLng`.
- `--short` argument  in `content:generate` console command.
- Support for `maxlength` attribute in `html.Input` and `html.TextArea`.
- Support for `max_length` attribute in `widget.input.Text`, `widget.input.TextArea` and descendants.
- New function: `content.get_tag()`.

### Changed
- `content.eps` renamed to `content.ep`.
- `router.endpoint_url()` renamed to `router.ep_url()`.
- `router.endpoint_path()` renamed to `router.ep_path()`.

### Fixed
- Various errors in `currency.widget.Currency`.
- Invalid longitude and latitude order in `geo.widget.*`.


## 0.11.3 (2015-09-05)
### Fixed
- Error while setting value of the `geo.widget.SearchAddress`.


## 0.11.2 (2015-09-05)
### Added
- Users' registration date in users browser.

### Changed
- `db.ssl` configuration parameter is `true` by default.

### Fixed
- Package search error in `lang.register_package()`.


## 0.11.1 (2015-09-04)
### Added
- Now is possible to specify allowed members types, min and max lengths in `odm.field.List`.
- New ODM field `odm.field.FloatList`. 
- New event `pytsite.content.console.generate`.
- New function `content.get_tags()`.
- `--no-html` argument  in `content:generate` console command.

### Fixed
- Incorrect arguments order in `geo` widgets.

### Changed
- Some `odm.field.*` fields rework.
- `geo.odm_field.Position` renamed to `geo.odm_field.LngLat`.


## 0.11 (2015-09-03)
### Added
- `auth_log` package.
- New events: `pytsite.auth.login` and `pytsite.auth.logout`.

### Changed
- Frequency of `cleanup` decreased to 1 hour.


## 0.10.1 (2015-09-03)
### Changed
- `auth.find_users()` now sorts by `login_count`, descending.

### Fixed
- Invalid reference to `geo.odm_field` in `content.model.Article` setup.


## 0.10 (2015-09-03)
### Added
- `geo_ip` package.
- ODM field `Position` in `geo` package.

### Changed
- Automatic type conversion in setters of `odm.field.Integer` and `odm.field.Float`. 


## 0.9 (2015-09-02)
### Added
- `sitemap` package.
- Session and temporary data cleanup is now maintained by `cron` instead of console commands.

### Fixed
- Too late start timestamp set bug in `cron`.
- Non working events '30min' and 'hourly' in `cron`.


## 0.8.7 (2015-09-01)
### Added
- Missed functions in public API of the `content`.
- `warn` function in `logger`.

### Changed
- `logger` functions now accept message's prefix.
- Logging level of `cron`'s message 'Cron is still working' lowered to 'warning'.

### Fixed
- `cleanup` package initialization while application start.


## 0.8.6 (2015-08-31)
### Changed
- 1 export in 1 minute limit in `content_export`.


## 0.8.5 (2015-08-29)
### Fixed
- Missed cron initialization.


## 0.8.4 (2015-08-29)
### Changed
- 5 exports in 5 minutes limit in `content_export`.


## 0.8.3 (2015-08-29)
### Fixed
- Removed forgotten debug messages.
- Incorrect language ODM UI form field setup in `taxonomy.model.Term`.  


## 0.8.2 (2015-08-28)
### Fixed
- Removed `module_name` extra argument from `logger`.


## 0.8.1 (2015-08-28)
### Fixed
- `VERSION.txt` included into `setup.py`.


## 0.8 (2015-08-28)
### Changed
- `core` refactored into separate modules.
- `update` module rewritten. 

### Fixed
- Value set error in `currency.odm.CurrencyField`.
- Language issues while working with `content` and `taxonomy` models.


## 0.7.2 (2015-08-25)
### Changed
- 10 exports in 15 minutes limit in `content_export`.

## 0.7.1 (2015-08-25)
### Added
- `pytsite.core.cron.(1,5,15)min` events.
- `core.threading` module.

### Fixed
- Thread safety in `content_export`.

### Changed
- No limit in `content_export`.

## 0.7 (2015-08-24)
### Added
- Text indexes and search in `core.odm`.
- `replace_widget()` method in `core.form.Base`.

### Changed
- 10 exports in 15 minutes limit in `content_export`.


## 0.6.1 (2015-08-20)
### Fixed
- Incorrect CSS class name in `geo.widget.SearchAddress`.


## 0.6 (2015-08-20)
### Added
- `geo.widget.Location` widget.
- `autodetect` property in `geo.widget.SearchAddress`.
- `core.validation.rule.Float` rule.
- Support for children in `core.html.TagLessElement`.
- `<script>` is now allowed in `ckeditor.widget.CKEditor`.
- `hide()` method in `core.widget.Base`.
- Support for `hidden` attribute in `core.html` elements.
- Field `publish_date_pretty` in `content.model.Content`.

### Changed
- `auth.get_logout_url()` renamed to `auth.logout_url()`.
- `core.validation.rule.GreaterThan` renamed to `core.validation.rule.FloatGreaterThan`.
- `core.widget.static.Text` now separates value and title.

### Fixed
- Error in `auth.logout_url`.
- Field existence check in `content.model.Article.setup_m_form()`.
- Error in template `flag@widget`.
- Incorrect behaviour in `core.validation.rule.DictPartsNotEmpty`.
- Error in `geo.rule.AddressNotEmpty`.
- Incorrect russian plurals for numbers between 11 and 19.
- CSS asset appending in `flag.widget.Flag`.


## 0.5.4 (2015-08-16)
### Added
- `reply_to` argument in `core.mail.Message`.

### Fixed
- Incorrect argument passing to `mongodump` executable in `core.console.command.DbDump`.


## 0.5.3 (2015-08-11)
### Fixed
- TZ-aware dates manipulation.


## 0.5.2 (2015-08-11)
### Changed
- RSS and Atom feeds store path in `content`. 


## 0.5.1 (2015-08-11)
### Fixed
- TZ-aware dates manipulation errors in `content` and `disqus`.


## 0.5 (2015-08-11)
### Added
- `feed` plugin.
- RSS and Atom feeds generation in `content`. 

### Changed
- More informative users browser layout in `auth_ui`.
- `core.odm.field.DateTime` is TZ aware now.


## 0.4 (2015-08-10)
### Added
- `sitemap` plugin.
- Cron sitemap generation in `content`.


## 0.3.5 (2015-08-10)
### Changed
- Template of `auth_ui.widget.profile`.


## 0.3.4 (2015-08-08)
### Fixed
- Localized URLs error in `core.router.current_url()`.


## 0.3.3 (2015-08-07)
### Fixed
- Localization related content and taxonomy ODM UI form's widgets options.


## 0.3.2 (2015-08-06)
### Added
- Ukrainian translations.

### Fixed
- Localized routes processing errors and other localization issues.


## 0.3.1 (2015-08-04)
### Added
- `auth`:
    - New fields in `model.User`:  `last_activity` and `is_online`. 


## 0.3 (2015-08-03)
### Added
- `core`:
    - `date` filter in `tpl`.
    - New arguments in `odm.Model.save()`: `skip_hooks` and `update_timestamp`.
- `auth`:
    - New field `urls` in `model.User`.
- `auth_ui`
    - New field `profile_view_url` in `auth_ui.model.userUI`.
    - Profile widget.
    - Profile view endpoint: `auth_ui.eps.profile_view()`.
    - Base profile view template.
- `content`:
    - 'Additional JS code' field on the settings form.
    - New widget `SearchInput`.
    - Content index view by author.
    - `content:generate` console command.
- `settings`:
    - `settings` global in `core.tpl`.

### Changed
- Template in `admin`.
- Code cleanup in `core.odm.Model`.

### Fixed
- Large amounts deletion error in `odm_ui._browser`.
- Removed unnecessary thread locks in `core.odm.Model`.
- Incorrect behaviour of `content.eps.index()` in case of `term_field` argument usage.
- Arguments cleanup while processing login form in `auth`.
- Strings strip in `core.validation.rule.NotEmpty`.
- Improved regexp in `core.validation.rule.Email`.
- Input arguments pass-through to called endpoint in `core.eps.index()`.  


## 0.2.13 (2015-07-27)
### Added
- Thread safety in `core.odm`.
- Thread safety in `content_export`.
- Own Cron. No more OS's cron!

### Fixed
- Exception handling in `cron:start` console command.
- Unnecessary user login count in `auth.get_current_user()`.
- YouTube links detection in `core.widget.static.VideoPlayer`. 


## 0.2.12 (2015-07-25)
### Changed
- Threading removed from `content_export`.


## 0.2.11 (2015-07-24)
### Changed
- Program logic in `content_export`.


## 0.2.10 (2015-07-24)
### Added
- `[img:N:link_orig]` tag support in `content.model.Content` models.


## 0.2.9 (2015-07-24)
### Added
- Twitter content cross posting. 

### Changed
- `poster` moved to `export` and refactored.
- `oauth` removed.

### Fixed
- Handling lost connections in `core.db`.
- Route alias generation in `content.model.Article`.


## 0.2.8 (2015-07-22)
### Fixed
- YouTube links validation in `core.validation.rule.VideoHostingUrl` 


## 0.2.7 (2015-07-22)
### Fixed
- Catch exceptions in `core.mail.Message.send()`.
- YouTube links detection in `core.widget.static.VideoPlayer`.


## 0.2.6 (2015-07-22)
### Added
- Permissions support in `settings`.

### Changed
- `core.assetman` refactored.
- `core.client` improved and renamed to `core.browser`.
- `content.model.Content` publish time widget is now visible for non admins.
- `core.mail`: asynchronous messages delivery. 


## 0.2.4 (2015-07-21)
### Fixed
- Incorrect value of `og:url` in `content.eps.view`. 


## 0.2.3 (2015-07-21)
### Added
- Support for 'author' and 'og:url' in `core.metatag`.


## 0.2.2 (2015-07-21)
### Added
- `core`:
    - Support for 'article:author' and 'article:publisher' in `metatag`.

### Fixed
- setup.py
- Host and port usage in `db:*` console commands.
- Permissions check in `admin.sidebar`.
- Permissions check in `odm_ui`.


## 0.2.1 (2015-07-21)
### Fixed
- setup.py


## 0.2 (2015-07-21)
### Added
- New plugins: `oauth`, `twitter`, `poster`, `page`, `add_this`.
- Some english and ukrainian translations.
- `core`:
    - SSL and authorization basic support in `core.db`.
    - New events:
        - `odm.entity.pre_save`;
        - `odm.entity.save`.
    - New validation rules:
        - `core.validation.rule.ListListItemNotEmpty`;
        - `core.validation.rule.ListListItemUrl`;
        - `core.validation.rule.VideoHostingUrl`.
    - New `args` argument in `core.odm.Model.t()`.
    - New widgets: 
        - `core.widget.static.Pager`;
        - `core.widget.input.StringList`;
        - `core.widget.static.VideoPlayer`.
    - New functions:
        - `core.util.list_cleanup()`;
        - `core.util.dict_cleanup()`;
        - `core.util.nav_link()`.
    - New `core.tpl` globals: `url()`, `current_url()`, `base_url()` , `endpoint_url()`, `nav_link()`.
    - Sorting ability in `odm.field.RefList.get_val()`.
    - New console commands:
        - `db:dump`
        - `db:restore`
    - Support for some OpenGraph and Twitter properties in `core.metatag`.
- `auth`:
    - New ODM `auth.model.User` properties: `full_name`.
- `content`:
    - New public package method: `content.create()`
    - `content.model.Content` model:
        - Processing `[img]` and `[vid]` body tags.
        - New field properties.
        - New events `content.entity.pre_save`, `content.entity.save`.
    - "Propose content" form.
    - Weekly email digest subscription.
    - SEO settings form for home page.
    - Support for OpenGraph and Twitter meta tags.
    - Simple content search.
- `ckeditor`:
    - Images upload.
- `file`:
    - New ODM `file.model.File` properties: `url`, `path`, `abs_path`.
    - New field: `attached_to`.
- `odm_ui`:
    - New `stage` argument in `odm_ui.UIMixin.setup_m_form()` hook.
- `route_alias`:
    - New `route_alias.model.RouteAlias` properties: `alias`, `target`, `language`.
- `taxonomy`:
    - New ODM `taxonomy.model.Term` properties: `title`, `alias`, `language`, `weight`, `order`.

### Changed
- `core.widget` plugin:
    - New argument in `geo.widget.SearchAddress`: `autodetect`. 
- `geo` plugin:
    - New `autodetect` argument in `geo.widget.SearchAddress`.
- `auth`
    - Config parameter changed `auth.auto_signup` -> `auth.allow_signup`.
- `admin` plugin templates improvements.
- `core.validation.rule.Url` now can work with lists and dicts.
- `core.widget.input.CKEditor` moved to `ckeditor.widget.CKEditor`.
- `tag` joined with `content`.

### Fixed
- Empty configuration files read error.
- Incorrect usage of 'server_name' configuration value in `core.router`.
- Check for app assets directory existence during `lang:build` console command.
- Exceptions handling during `odm_ui`'s form submit.
- Router's `current_url` incorrect behaviour in some situations.
- Incorrect entity caption field get in `odm_ui.widget.ODMSelect`.
- Incorrect method call in `admin@tpl/header.jinja2`.
- Issue with `core.odm.Model.t()` in inheritance cases.
- Incorrect return value of `core.http.request.values_dict` in case of list input.
- Non-working JS for `core.widget.select.DateTime()`.
- Open files leak in `file.create()`.


## 0.1 (2015-07-01)
First release.

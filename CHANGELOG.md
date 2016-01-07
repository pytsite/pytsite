# PytSite Changelog

## 0.42 (2016-01-07)
### Added
- New function: `util.strip_html_tags()`.
- More detailed error output in `fb.Session.paginated_request()`.

### Changed
- `fb`'s content_export driver now uses entity body instead of description as export message body and trims it to 600 
  characters. 

### Fixed
- Error in `content_export`'s form rendering.
- Checking for '__form_location' widget existence in `form.Form.render()`.


## 0.41.18 (2016-01-05)
### Added
- New `tpl`'s global: `metatag_get`

### Fixed
- Improper metatag usages in `admin`'s and `auth_ui`'s templates.


## 0.41.17 (2016-01-05)
### Added
- New `tpl`'s globals: `browser_include()`, `assetman_add()`, `assetman_css()`, `assetman_js()`, `assetman_inline()`, 
  `metatag()`, `metatag_all()`, `reg_get()`, `get_current_lang()`.
- New event 'pytsite.tpl.render';

### Changed
- `auth_get_current_user()` tpl global renamed to `get_current_user()`. 
- `auth_get_login_form()` tpl global renamed to `get_login_form()`.
- `auth_get_logout_url()` tpl global renamed to `get_logout_url()`.

### Removed
- `tpl`'s globals: `browser`, `assetman`, `metatag`, `reg`, `lang`.


## 0.41.16 (2016-01-04)
### Added
- New `tpl`'s globals: `auth_get_current_user()`, `auth_get_login_form()`, `auth_get_logout_url()`, `current_path()`.
- 'mode' keyword argument in widgets' `set_val()` calls.
- New methods in `odm_ui.model.UIModel`: `ui_m_form_get_url()` and `ui_d_form_get_url()`.
- New method `router.remove_path_alias()`.
- New ODM field: `wallet.field.Money`.
- New widget: `wallet.widget.MoneyInput`.

### Changed
- 'prefix_symbol' and 'suffix_symbol' replaced with 'symbol' in `currency`.
- `widget.input.Float` is `widget.input.Decimal` now.
- `validation.rule.Float` is `validation.rule.Decimal` now.
- Widgets validation logic.
- `widget.Base.remove_rules()` reamed to `widget.Base.clear_rules()`.

### Fixed
- Invalid widget types in `auth_ui.model.UserUI`.
- Route alias string sanitization in `content.model.Content`.
- Errors in `Number`-based validation rules.

### Removed
- `tpl`'s globals: `auth`, `content`, `disqus`, `flag`.


## 0.41.15 (2015-12-29)
### Added
- New fields in `auth.model.User`: `geo_ip`, `country`, `city`.
- More convenient `auth_ui`'s endpoints overriding.
- `currency_fmt` added to `tpl`'s globals.
- 'currency' field for `auth.model.user` added by `currency`.
- 'system' currencies in `currency`.

### Changed
- `odm.Model.define_field()`, `odm.Model.remove_field()` and `odm.Model.define_index()` are public.
- `odm.field.Dict.get_val()` is returning `frozendict`.
- `wallet` has been refactored.

### Removed
- `form.Form.redirect` property.
- `auth_ui` global from `tpl`'s globals.
- `currency` global from `tpl`'s globals.


## 0.41.14 (2015-12-25)
### Added
- New function `tpl.is_global_registered()`.
- New `router`'s event 'pytsite.router.exception'.
- `call_once` argument in `events.listen()`.

### Changed
- `form`'s and `contact`'s JS assets made permanent. 

### Removed
- `url` global from `tpl`.

## 0.41.13 (2015-12-24)
### Fixed
- Admin templates inheritance in `odm_ui`.


## 0.41.12 (2015-12-24)
### Added
- New function `admin.render()`.


## 0.41.11 (2015-12-24)
### Added
- New function `router.is_ep_callable()`.
- Support for custom exceptions handler in `router`.

### Changed
- `tpl`'s 'widget' global removed.


## 0.41.10 (2015-12-23)
### Added
- Text field for entering description in `wallet.model.Transaction`.

### Changed
- `wallet.model.Account.description` field is required now.


## 0.41.9 (2015-12-23)
### Changed
- `odm.field.FloatList` refactored to `odm.field.DecimalList`.


## 0.41.8 (2015-12-23)
### Fixed
- Date localization check in `util`'s time formatting functions.
- Incorrect date format `sitemap`.


## 0.41.7 (2015-12-23)
### Fixed
- Incorrect operations with `odm.field.Dict`. 


## 0.41.6 (2015-12-23)
### Changed
- `odm.field.Dict.get_val()` returns immutable dictionary now.
- `odm.field.Decimal` refactored.


## 0.41.5 (2015-12-23)
### Changed
- `validation`'s rules refactored.


## 0.41.4 (2015-12-23)
### Fixed
- Error in while `feed`'s RSS generation.


## 0.41.3 (2015-12-22)
### Changed
- `router.url()` refactored.
- `util.nav_link()` refactored.


## 0.41.2 (2015-12-21)
### Fixed
- Error in `odm_ui.check_permissions`


## 0.41.1 (2015-12-19)
### Fixed
- Error in `fb.widget.Auth`.
- Error in `widget.input.Integer`.


## 0.41 (2015-12-19)
### Added
- New methods in `odm.Finder`: `remove_where()` as `remove_or_where()`.
- `currency` is ready for work.
- New method `odm.Model.reload()`
- `wallet` is ready to work. 

### Changed
- `odm_ui` refactored a lot.
- `browser.bootstrap-table` updated to version 1.9.1.
- `form.Base` renamed to `form.Form`.
- `currency` rates precision changed to 8 digits after floating point.
- `widget.static.Wrapper` renamed to `widget.static.HTMLWrap`.

### Fixed
- Little fixes of `auth_log`.
- Incorrect check in `validation.rule.NonEmpty` rule.
- Error in `fb.widget.Auth`.
- Missing entity state update in `odm.field.List.sub_val()`. 


## 0.40.4 (2015-12-14)
### Changed
- Default maximum image file size for `content.model.Content.images` field's upload widget increased to 5 MB.


## 0.40.3 (2015-12-13)
### Fixed
- Input arguments processing in `util.w3c_datetime()` and `util.rfc822_datetime()`.


## 0.40.2 (2015-12-13)
### Fixed
- Times format in `sitemap`.


## 0.40.1 (2015-12-13)
### Added
- New function `util.w3c_datetime()`.


## 0.40 (2015-12-13)
### Added
- Base functions in `wallet`.

### Changed
- Some refactoring of `currency`, `auth` and `odm`.

### Fixed
- Bugs in `sitemap`.


## 0.39.3 (2015-12-12)
### Fixed
- Missing package in setup.py.


## 0.39.2 (2015-12-12)
### Added
- New registry variable: 'env.type'.

### Fixed
- Missing mail template for english language in `content`.


## 0.39.1 (2015-12-08)
### Fixed
- Improper models status set in `content` while saving entities.


## 0.39 (2015-12-08)
### Added
- New ODM field: `odm.field.Decimal`.
- New permission definitions in `content`: 'pytsite.content.set_publish_time.*' and 
  'pytsite.content.set_localization.*'.


## 0.38.4 (2015-12-02)
### Fixed
- 'yandex:full-text' iframes incomplete cleanup. 


## 0.38.3 (2015-12-02)
### Added
- Automatic application root path detection.
- Tests for `odm` API functions and for some `odm.Model` methods.


## 0.38.2 (2015-12-02)
### Added
- Images and iframes cleanup in `feed.yandex_news.Item.full_text`.

## 0.38.1 (2015-12-02)
### Added
- `feed.yandex_news.PdaLink` element.

### Fixed
- Type error in `auth_ui.widget.Profile`.
- Incorrect placement of 'yandex:logo' tag in `feed.yandex_news.Generator`.


## 0.38 (2015-12-01)
### Added
- `feed` completely rewritten.


## 0.37.9 (2015-11-30)
### Fixed
- Missing widgets UIDs in `tumblr`'s auth widget.


## 0.37.8 (2015-11-30)
### Fixed
- Improper tuple concatenation error in `tumblr`'s content export driver.


## 0.37.7 (2015-11-29)
### Fixed
- Error in `file.widget.FilesUpload`.


## 0.37.6 (2015-11-28)
### Added
- All translations in `browser.select2` and `ckeditor`.
- `browser.select2` updated to version 4.0.1.

### Fixed
- Error while parsing image tags in `content.model` body field.
- Error in `pytsite.lang.t` JS function.


## 0.37.5 (2015-11-28)
### Added
- 'pl', 'it' translations in `browser.select2` library.


## 0.37.4 (2015-11-28)
### Fixed
- Error in `auth_ui` template.


## 0.37.3 (2015-11-28)
### Fixed
- Video embedding error in `content.model.Content`.


## 0.37.2 (2015-11-28)
### Fixed
- Improper input value checking in `file.widget.FilesUpload`.
- Typo in `flag.widget.Flag`.


## 0.37.1 (2015-11-28)
### Fixed
- Improper `widget.static.Pager` initialization in `content`.


## 0.37 (2015-11-28)
### Added
- New validation rule: `validation.rule.Number`.
- New validation rules: `validation.rule.Greater`, `validation.rule.Less`.
- New validation rules: `validation.rule.GreaterOrEqual`, `validation.rule.LessOrEqual`.

### Changed
- `odm.field.List` and descendants now return `tuple` by `get_val()` instead of `list`.
- `widget.Base.get_value()` renamed to `widget.Base.get_val()`.
- `widget.Base.set_value()` renamed to `widget.Base.set_val()`.
- `uid` argument of `widget.Base` is mandatory now.

### Fixed
- Title and CSS settings in `auth.get_login_form()`.
- Non-strings processing in `util.list_cleanup()` and `util.dict_cleanup()`.
- Improper tags processing in `content_export`'s driver of `fb` package.


## 0.36 (2015-11-16)
### Added
- New widget: `taxonomy.widget.TermSelect`.

### Fixed
- Translation errors in `odm.Model.t()`.
- `TypeError` catch in `validation.rule.Float`.


## 0.35.6 (2015-11-15)
### Fixed
- Form validation in `settings`.


## 0.35.5 (2015-11-15)
### Fixed
- 'postal_code' field type in `geo_ip` ODM model.


## 0.35.4 (2015-11-15)
### Fixed
- Link to homepage in `widget.select.LanguageNav`.


## 0.35.3 (2015-11-14)
### Fixed
- Typo in `content`.


## 0.35.2 (2015-11-14)
### Fixed
- Multilingual digest subscriptions in `content`.


## 0.35.1 (2015-11-14)
### Fixed
- Support for 'pytsite.content.ep.subscribe' endpoint in `browser`.


## 0.35 (2015-11-14)
### Added
- `browser`'s JS endpoints now must be registered before usage.
- Multilingual mail digests in `content`.


## 0.34.1 (2015-11-12)
### Fixed
- Improper email validation in `content.ep.subscribe()` endpoint. 
- Support for fallback language in JS `lang`.


## 0.34 (2015-11-12)
### Added
- Support for fallback language in `lang`.

### Changed
- Switched to [ip-api.com](http://ip-api.com) in `geo_ip`.


## 0.33.6 (2015-11-11)
### Added
- `cleanup` argument in `odm.field.List` constructor. 


## 0.33.5 (2015-11-11)
### Fixed
- Improper paginated result checking in `fb`'s session.


## 0.33.4 (2015-11-11)
### Added
- Support for [Telize](http://www.telize.com/)-1.04's `organization` field in `geo_ip`.
- `add_tags` in `content_export`'s driver.


## 0.33.3 (2015-11-09)
### Added
- `fb`: export from behalf of a page.

### Fixed
- Incorrect building of the redirect URL in the `ulogin` auth driver. 


## 0.33.2 (2015-11-06)
### Changed
- `fb.Session.feed_link()` removed in favour of `fb.Session.feed_message()`.


## 0.33.1 (2015-11-05)
### Fixed
- Children separator output in widgets.


## 0.33 (2015-11-05)
### Added
- New package: `reddit` (partly completed).
- New package: `fb` (partly completed).
- New `auth` driver: `password`.


## 0.32.4 (2015-10-28)
### Changed
- Default value of the config parameter `content_export.delay_errors` increased to 2 hours.

### Fixed
- Incomplete driver options title in `tumblr`'s auth widget.


## 0.32.3 (2015-10-27)
### Fixed
- Incorrect loop logic in `content_export`.


## 0.32.2 (2015-10-27)
### Added
- New event `pytsite.auth.login_error`.
- Support for severity by `auth_log`'s model.
- `auth_log` ODM UI improvements.

### Changed
- `pytsite.auth.error.LoginIncorrect` renamed to `pytsite.auth.error.LoginError`.

### Fixed
- Error while resolving non-private IP addresses in `geo_ip.resolve()`. 


## 0.32.1 (2015-10-26)
### Fixed
- Unused import in `router` which leads to crash at startup.


## 0.32 (2015-10-26)
### Added
- ODM UI implementation for `auth_log`.
- Timed pausing `content_export`'s exporters in case of errors. 
- New fields `paused_till` and `last_error` in `content_export.model.ContentExport`.

### Fixed
- Error in `content.widget.ModelSelect`.


## 0.31 (2015-10-25)
### Added
- `bootstrap` argument in `widget.select.LanguageNav`.
- New widget `widget.select Select2`.
- New `browser`'s library: `select2`.
- `include_current` argument in `lang.langs()`.
- Localization select on `content`'s entities forms.
- hreflangs support by `content` entities.

### Fixed
- Incomplete items list in `widget.select.LanguageNav`.
- Incorrect language detection in JavaScript `t()` function.


## 0.30.1 (2015-10-23)
### Fixed
- Error in `content`'s propose form.


## 0.30 (2015-10-22)
### Added
- New package: `tumblr`.


## 0.29 (2015-10-20)
### Added
- Font Awesome updated to version 4.4.0.


## 0.28.1 (2015-10-20)
### Fixed
- `content_export`'s driver initialization error in `vk`.


## 0.28 (2015-10-20)
### Added
- New package: `vk`.
- New fields in `content_export`'s model: `only_with_images` and `max_age`.


## 0.27.2 (2015-10-14)
### Fixed
- `browser`: added missed images for slippry.


## 0.27.1 (2015-10-13)
### Fixed
- Excluded language part from `content`'s feeds file names if defined languages count equals 1.


## 0.27 (2015-10-13)
### Changed
- `content`'s feeds generation moved to separate function `content.generate_feeds()`.


## 0.26 (2015-10-13)
### Added
- Support for `mousewheel`,`smoothscroll`, `enllax`, `scrollto`, `waypoints`, `slippry`, libraries in `browser`.


## 0.25 (2015-10-12)
### Added
- Support for `animate` and `wow` libraries in `browser`.


## 0.24 (2015-10-12)
### Added
- New function `lang.is_translation_defined()`.

### Changed
- Automatic ODM collections reindexing on `console`'s 'update' command is now disabled.

### Fixed
- Cascading translations in `content`'s models.


## 0.23.7 (2015-10-11)
### Added
- CKeditor updated to 4.5.4.

### Fixed
- CKEditor JS file corruption after unnecessary minifying.


## 0.23.6 (2015-10-11)
### Added
- Languages support while sitemap generation in `content`.

### Fixed
- Error while URLs validation in `sitemap`.
- Error while URLs validation in `feed`.


## 0.23.5 (2015-10-10)
### Fixed
- Non working inline JS code injection on internal pages in `content`.


## 0.23.4 (2015-10-08)
### Changed
- 'images' field is now required in `content.model.Article`.

### Fixed
- Error in arguments order while constructing `Url()` in `validation.rule.ListListItemUrl()'.
- Error in setting validator's value in `file.widget.FilesUpload`. 

## 0.23.3 (2015-10-08)
### Added
- 'section' column in `content`'s articles browser UI.

### Fixed
- Changing content path's aliases error.
- Showing empty header area in forms. 

## 0.23.2 (2015-10-07)
### Added
- favicon support in `metatag`.

## 0.23.1 (2015-10-06)
### Added
- `twitter:site` support in `metatag`.

## 0.23 (2015-10-06)
### Added
- New widget `widget.select.LanguageNav`.
- Basic support for `hreflang` in router.
- Basic support for adding inline code in `assetman`.

### Changed
- `lang.define_languages()` renamed to `lang.define()`.
- `lang.set_current_lang()` renamed to `lang.set_current()`.
- `lang.get_current_lang()` renamed to `lang.get_current()`.
- `lang.get_langs()` renamed to `lang.langs()`.
- `lang.get_lang_title()` renamed to `lang.lang_title()` and improved.

### Fixed
- 'Unsupported language' exception in case of specifying it in the URL path.


## 0.22.1 (2015-10-05)
### Changed
- `rjsmin` requirement replaced with `jsmin`.
- `cssutils` requirement replaced with `cssmin`.

## 0.22 (2015-10-03)
### Added
- New package `contact`.
- `form.Base.get_widgets()` method.
- `widget.Base.form_area` property.
- `util.weight_sort()` now supports objects.
- `widget.input.Email` widget.
- New attributes in `widget.Base`: `label_hidden` and `label_disabled`.
- New shortcut method `form.Base.render_widget()`.

### Changes
- `form.add_widget()`'s `area` argument removed in favour of the `widget.Base.form_area` property.
- Output generation of forms is fully template based now.

### Fixed
- `form` and `validation` was partly refactored.
- Underscore recognition in domain part of URL in `validation.Rule.Url`.


## 0.21.4 (2015-09-28)
### Added
- `images` column in admin content view browser. 


## 0.21.3 (2015-09-28)
### Fixed
- Entity description emptiness check while generating RSS and Atom feeds in content.


## 0.21.2 (2015-09-28)
### Added
- Store user's profile URL by `auth.driver.ulogin` while logging in.

### Fixed
- Layout errors in `auth_ui.widget.Profile`.
- User's nickname composing in `auth.driver.ulogin`.


## 0.21.1 (2015-09-27)
### Added
- English translations in `content`, `admin`, `lang`, `taxonomy`, `router`, `auth_ui`, `settings`, `odm_ui`.
- New argument `strip_lang` in `router.ep_path()`.
- New arguments passed to endpoints via `router.call_ep()`: `_call_orig` and `_name_orig`.

### Fixed
- Incorrect path alias resolving in `content.model.Content.url`.


## 0.21 (2015-09-26)
### Added
- New events `pytsite.odm.entity.delete` and `pytsite.odm.entity.%model%.delete`.

### Changed
- `flag`'s API functions now accept `odm.Model` instead of string as input argument.
- `flag`'s API functions now accept author of the flag(s) as optional argument.
- `core.odm@register_model` event renamed to `pytsite.odm.register_model`.
- `content.entity.pre_save` event renamed to `pytsite.content.entity.pre_save`.
- `content.entity.pre_save.%model%` event renamed to `pytsite.content.entity.%model%.pre_save`.
- `content.entity.save` event renamed to `pytsite.content.entity.save`.
- `content.entity.save.%model%` event renamed to `pytsite.content.entity.%model%.save`.
- `odm.entity.pre_save` event renamed to `pytsite.odm.entity.pre_save`.
- `odm.entity.pre_save.%model%` event renamed to `pytsite.odm.entity.%model%.pre_save`.
- `odm.entity.pre_delete` event renamed to `pytsite.odm.entity.pre_delete`.
- `odm.entity.pre_delete.%model%` event renamed to `pytsite.odm.entity.%model%.pre_delete`.
- `setup` event renamed to `pytsite.setup`.

### Fixed
- `flag` total rework.


## 0.20.1 (2015-09-25)
### Added
- `data-alias` and `data-path` properties in `taxonomy.widget.Cloud`'s default template;

## 0.20 (2015-09-25)
### Added
- New configuration parameters: `auth_ui.model.user` and `auth_ui.model.role`.
- New method `odm.Model.f_sub()`.
- New method `route_alias.find_by_alias()`.

### Changed
- `route_alias.find_one_by_target()` renamed to `route_alias.find_by_target()`.

### Fixed
- Erroneous options overwriting of `auth.model.model.User` in `auth.driver.ulogin`. 
- Little rewrite of `odm.field`


## 0.19 (2015-09-21)
### Added
- New widget `auth_ui.widget.UserSelect()`.
- User select widget on the `content.model.Content`'s form.


## 0.18.4 (2015-09-21)
### Fixed
- Duplicates ignoring error in `assetman.add()`.


## 0.18.3 (2015-09-21)
### Added
- `aspect_ratio` argument in `image.model.Image.get_html()`.
- `data-aspect-ratio` property support by `browser`'s `responsive` library.


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
- New method `odm_ui.Model.ui_get_delete_url()`

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
- Error in `auth.logout_url()`.
- Field existence check in `content.model.Article.ui_m_form_setup()`.
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
- Strings strip in `core.validation.rule.NonEmpty`.
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
    - New `stage` argument in `odm_ui.UIMixin.ui_m_form_setup()` hook.
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

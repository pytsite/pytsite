# PytSite Changelog


## 0.98.82 (2017-03-11)
### Added
- `form`: support of non-cached forms.


## 0.98.81 (2017-03-08)
### Fixed
- `odm`: geo point distance object default values.


## 0.98.80 (2017-03-07)
### Fixed
- `core`: application's root path detection.


## 0.98.79 (2017-03-03)
### Added
- `plugman`: missing plugin automatic installation in `start()`. 

### Fixed
- `routing`: rule path's slashes cleanup.


## 0.98.78 (2017-03-03)
### Added
- `routing`: support for new rule formatters: **float**, **alpha**, **alnum**, **choice**.

### Changed
- `router`:
    - API function `add_rule()` renamed to `handle()`;
    - `handle()`'s **name** argument is generated as random string by default now.
    - `handle()`'s **method** argument renamed to **methods** and now accepts multiple values.
- `routing`: refactored.


## 0.98.77 (2017-03-02)
### Fixed
- `router`: work of `current_path()` in non web environment. 


## 0.98.76 (2017-03-02)
### Changed
- `admin`: `admin_url` tpl's global renamed to `admin_base_path`.

### Fixed
- `router`: current language autodetection in `url()`. 


## 0.98.75 (2017-02-28)
### Fixed
- `odm`: exception description.
- `odm_ui`: route method.


## 0.98.74 (2017-02-28)
### Fixed
- `auth`: incorrect template names.


## 0.98.73 (2017-02-27)
### Fixed
- `plugman`: missed colon.


## 0.98.72 (2017-02-27)
### Fixed
- `plugman`: app start fail on plugins API host.


## 0.98.71 (2017-02-25)
### Fixed
- `router`: language related issues.


## 0.98.70 (2017-02-25)
### Added
- `theme`: new tpl's global: `theme_logo_url()`.

### Fixed
- `http_api`: missed localization header in JS requests.
- `router`: calls to named routes.
- `theme`: assets compilation order on setting form submit.


## 0.98.69 (2017-02-22)
### Added
- `auth`:
    - storage driver registration;
    - new methods in `model.AbstractRole`: `add_permission()`, `remove_permission()`.

### Changed
- `router`: routing moved from Werkzeug's to own `routing` package.

### Fixed
- `auth`: missing **GET auth/is_anonymous** HTTP API endpoint.
- `reload`: HTTP API handler.


## 0.98.68 (2017-02-18)
### Fixed
- `http_api`: incorrect URL building in JS function.


## 0.98.67 (2017-02-17)
### Fixed
- `file_storage_odm`: model JSON formatting. 


## 0.98.66 (2017-02-17)
### Added
- New package: `unittest`.
- `auth`:
    - some tests;
    - new methods in `model.AbstractUser`: `add_role()`, `remove_role()`.
- `auth_password`: some tests.
- `file`: some tests.
- `util`: new API function: `parse_w3c_datetime_str`.

### Changed
- `auth`: return values of 'follow' HTTP endpoints.
- `file`: HTTP API endpoint names and authentication.

### Fixed
- `auth`: missed exception handling in HTTP API endpoint.



## 0.98.65 (2017-02-15)
### Added
- `auth_storage_odm`: support for anonymous and system user in `field.User`.

### Fixed
- `auth_storage_odm`: description translation in `model.ODMRole`.


## 0.98.64 (2017-02-14)
### Added
- `http_api`: events.
- `lang`: new API function: `is_defined()`.

### Fixed
- `auth`: HTTP API issues.


## 0.98.63 (2017-02-12)
### Added
- `router`: events API shortcuts.

### Fixed
- `metatag`: multithreading issue in `reset()`.


## 0.98.62 (2017-02-12)
### Added
- New package: `stats`.
- `cron`: events API shortcuts.
- `events`: value return in `fire()`.
- `odm`: entities cache cleanup.

### Changed
- `form`: default form's cache TTL increased to 6 hours.

### Fixed
- `metatag`: multithreading issue in `reset()`.


## 0.98.61 (2017-02-11)
### Changed
- `auth`: HTTP API endpoints signature.

### Updated
- Documentation of `http_api`, `odm_http_api`, `file`, `auth`.


## 0.98.60 (2017-02-10)
### Changed
- `auth`: access token authentication code moved to `http_api`.

### Fixed
- `metatag`: HTTP exceptions handling.


## 0.98.59 (2017-02-08)
### Fixed
- `odm_auth`: permissions checking error.  


## 0.98.58 (2017-02-07)
### Fixed
- `theme`: settings form.


## 0.98.57 (2017-02-07)
### Fixed
- `admin`: 'app@app_name' message ID usage.


## 0.98.56 (2017-02-07)
### Added
- `http_api`: new argument **includeUA** in `pytsite.httpApi.request()` function.

### Fixed
- 'app@app_name' message ID usage in several places.


## 0.98.55 (2017-02-07)
### Added
- `core`: late theme initialization.
- `lang`: neutral language support.
- `odm_ui`: `odm_*_allowed` methods in `model.UIEntity`.

### Changed
- `odm_auth`: checking permissions concept.
- `util`: support for table styles by default in `tidyfy_html()`.

### Fixed
- `ckeditor`: images uploading.

### Removed
- `theme`: on the fly theme switching. 


## 0.98.54 (2017-02-02)
### Fixed
- `plugman`: dependencies management while upgrading plugins. 


## 0.98.53 (2017-02-02)
### Added
- `metatag`: new API function: `rm()`.
- `theme`: support for favicon and logo upload.

### Fixed
- `plugman`: HTTP API calls from JS code.
- `theme`: settings load.


## 0.98.52 (2017-02-02)
### Fixed
- `form`: error while retrieving widgets in multi-step forms.


## 0.98.51 (2017-01-27)
### Fixed
- `auth_storage_odm`: outdated access token usage.


## 0.98.50 (2017-01-26)
### Changed
- `http_api`: totally reworked.


## 0.98.49 (2017-01-22)
### Fixed
- `auth_storage_odm`: non-existent field usage.


## 0.98.48 (2017-01-21)
### Added
- `http`: processing of 'list in dict' input from client side.
- `widget`: new widget: `MultiRow`.

### Changed
- `widget`: base class hook names.

### Fixed
- `form`: HTML escaping of error messages.

### Removed
- `settings`: processing all input values, not only widget-related.


## 0.98.47 (2017-01-16)
### Fixed
- `auth`: error while getting access token in **router.dispatch** event handler. 


## 0.98.46 (2017-01-16)
### Fixed
- `auth`: initialization order in `pytsite` package init.

### Changed
- `auth`: work with access tokens refactored.


## 0.98.45 (2017-01-15)
### Changed
- `form`: JS event names.


## 0.98.44 (2017-01-15)
### Changed
- `form`: JS event names and targets.

### Fixed
- `mail`: default 'From' header encoding.


## 0.98.43 (2017-01-14)
### Fixed
- `settings`: invalid form constructors signature's calls.


## 0.98.42 (2017-01-14)
### Fixed
- `odm_ui`: invalid form constructors signature's calls.


## 0.98.41 (2017-01-13)
### Fixed
- `auth`: exception in `get_sign_in_form()`.


## 0.98.40 (2017-01-13)
### Fixed
- `auth`: form names and UIDs usage.
- `form`: form's name usage.


## 0.98.39 (2017-01-13)
### Changed
- `form`: base form's class constructor's signature changed.


## 0.98.38 (2017-01-12)
### Fixed
- `theme`: theme's settings form submit.


## 0.98.37 (2017-01-12)
### Fixed
- `theme`: theme's settings loading via AJAX request.


## 0.98.36 (2017-01-12)
### Changed
- `form`: refactored.
- `widget`: refactored.

## 0.98.35 (2017-01-08)
### Added
- `assetman`: new argument **console_notify** in **pytsite.assetman.build** events.
- `console`: logging of console messages.

### Fixed
- `plugman`: console notification and logging.


## 0.98.34 (2017-01-08)
### Fixed
- `router`: endpoint callable resolving. 


## 0.98.33 (2017-01-08)
### Added
- `github`: support for paginated requests.


## 0.98.32 (2017-01-08)
### Added
- `plugman`: remembering erroneous plugins.
- `odm`: new hook method `model.Entity.on_register()`.

### Changed
- `odm_auth`: 'odm_perm_' permissions names changed to 'odm_auth'.
- `odm`: event name **pytsite.odm.register_model** changed to **pytsite.odm.register**.

### Removed
- `taxonomy`: moved to separate [plugin](https://github.com/pytsite/plugin-taxonomy).
- `content`: moved to separate [plugin](https://github.com/pytsite/plugin-content).
- `comments`: moved to separate [plugin](https://github.com/pytsite/plugin-comments).
- `comments_native`: moved to separate [plugin](https://github.com/pytsite/plugin-comments_native).


## 0.98.31 (2017-01-06)
### Fixed
- `plugman`: 'Permission denied' error while installing pip packages.


## 0.98.30 (2017-01-06)
### Added
- `plugman`:
    - new registry parameters: **plugman.license**, **plugman.plugins**;
    - automatic install of required plugins at application boot.


## 0.98.29 (2017-01-06)
### Removed
- `flag`: moved to separate [plugin](https://github.com/pytsite/plugin-flag).


## 0.98.28 (2017-01-04)
### Fixed
- `settings`: processing form's values.


## 0.98.27 (2017-01-04)
### Fixed
- `plugman`: absent plugin.json exception handling.

### Removed
- `lang`: support of {::callback} syntax.


## 0.98.26 (2017-01-04)
### Removed
- `currency`: moved to separate [plugin](https://github.com/pytsite/plugin-currency).
- `wallet`: moved to separate [plugin](https://github.com/pytsite/plugin-wallet).


## 0.98.25 (2016-12-25)
### Added
- `lang`: processing message IDs as globals.

### Changed
- `core`: 'config', 'log', 'static', 'storage', 'tmp' directories moved from the 'app' root.


## 0.98.24 (2016-12-25)
### Fixed
- `theme`: settings widgets values set. 


## 0.98.23 (2016-12-25)
### Added
- `assetman`: new API function: `register_global`.
- `theme`: support for settings in themes.
- `widget`: new widget `ColorPicker`.

### Changed
- `browser`: **inputmask** library updated from 3.1.64 to 3.3.4.


## 0.98.22 (2016-12-22)
### Fixed
- `browser`: Bootstrap CSS add-ons.
- `http_api`: verbose log messages while processing HTTP exceptions.

### Removed
- `assetman`: **add_asset** tpl global.
- `browser`: **add_lib** tpl global.
- `plugman`: support for automatic plugin installation during application boot.


## 0.98.21 (2016-12-21)
### Added
- `widget`: new argument in `select.LanguageNav`: **dropup**.

### Fixed
- `content`: processing exception in case of no comments driver registered.
- `semver`: processing `IndexError` in `latest()` function.


## 0.98.20 (2016-12-21)
### Added
- `plugman`: hostname sending in requests to plugin API. 

### Fixed
- `plugman`: license checking period.
- `router`: HTTP errors log message details.


## 0.98.19 (2016-12-21)
### Fixed
- `odm`: collections reindexing on 'pytsite.update' event. 


## 0.98.18 (2016-12-21)
### Added
- `odm_ui`: new argument `translate_captions` in `widget.EntityCheckboxes`.

### Changed
- `odm_ui`: captions is not translated by default now in `widget.EntityCheckboxes`.

### Fixed
- `widget`: form group class name in base widget.


## 0.98.17 (2016-12-20)
### Fixed
- `plugman`: plugin API request errors handling.


## 0.98.16 (2016-12-20)
### Added
- `form`: new hook method: 'Form.'
- `odm`: automatic collections reindexing on `pytsite.update` event.
- `widget`: new properties in base widget: `has_success`, 'has_warning' and `has_error`.

### Changed
- `plugman`: refactored to use new plugin API.


## 0.98.15 (2016-12-19)
### Added
- `github`: new `Session`'s method: `repo_contents()`.


## 0.98.14 (2016-12-18)
### Fixed
- `content`, `settings`, `taxonomy`: `admin`'s section permissions definition.


## 0.98.13 (2016-12-18)
### Fixed
- `admin`: permissions specification checking in `sidebar.add_menu()`. 
- `currency`: `admin`'s sidebar menu permissions.


## 0.98.12 (2016-12-18)
### Added
- Automatic necessary files and directories creation while core initialization.

### Removed
- `tpl`: **output.base_tpl** variable.


## 0.98.11 (2016-12-18)
### Added
- `router`: logging HTTP exceptions.
- `theme`: automatic resource directories creation.

### Fixed
- `assetman`: `errors` revealed for public usage.
- `metatag`: checking for `assetman`'s package registration while setting favicon.
- `router`: processing non existent endpoints via HTTP exception.
- `theme`: checks while theme registration and paths detection.

### Removed
- `mp`: removed completely.


## 0.98.10 (2016-12-16)
### Added
- `widget`: new constructor's argument **language_titles** in `select.LanguageNav`.


## 0.98.9 (2016-12-11)
### Added
- `content`: new widget: `ModelCheckboxes`.

### Fixed
- `theme`: invalid setting name.


## 0.98.8 (2016-12-09)
### Added
- `form`: new event: **pytsite.form.setup_widgets.FORM_UID**.

### Fixed
- `mail`: default sender name.

### Removed
- `content`: digest mail moved to separate [plugin](https://github.com/pytsite/plugin-content_digest).


## 0.98.7 (2016-12-03)
### Added
- `assetman`: new `build()`'s option: **cache** and corresponding console command argument.

### Changed
- `content`, `taxonomy`: processing **language** argument in find-related API functions.


## 0.98.6 (2016-12-03)
### Changed
- `assetman`: **assetman** console command renamed to **assetman:build**.

### Added
- `assetman`: new argument in **assetman:build** console command: **--package**.


## 0.98.5 (2016-12-02)
### Fixed
- `content`, `route_alias`, `taxonomy`: language related issues. 


## 0.98.4 (2016-12-01)
### Added
- `content`: new API function: `paginate()`.

### Changed
- `content`: response format of `ep.index()`. 
- `tpl`: signature of 'pytsite.tpl.render' event.

### Fixed
- `theme`: HTTP response handling. 


## 0.98.3 (2016-11-29)
### Fixed
- `taxonomy`: language widget default title and value on ODM model form.


## 0.98.2 (2016-11-29)
### Fixed
- `taxonomy`: language widget title on ODM model form.


## 0.98.1 (2016-11-29)
### Fixed
- `assetman`: incorrect absolute asset paths in some cases. 


## 0.98 (2016-11-29)
### Added
- `assetman`: new API function: `is_package_registered()`.
- `github`: new configuration parameter: `github.access_token`. 

### Changed
- `plugman`: partly refactored.

### Removed
- `auth_google`: moved to separate [plugin](https://github.com/pytsite/plugin-auth_google).
- `auth_log`: moved to separate [plugin](https://github.com/pytsite/plugin-auth_log).
- `block`: moved to separate [plugin](https://github.com/pytsite/plugin-content_block).
- `contact_form`: moved to separate [plugin](https://github.com/pytsite/plugin-contact_form).
- `content_export`: moved to separate [plugin](https://github.com/pytsite/plugin-content_export).
- `google`: removed totally.


## 0.97 (2016-11-27)
### Removed
- `content_import`: moved to separate [plugin](https://github.com/pytsite/plugin-content_import).

### Fixed
- `assetman`: check for static assets path existence. 


## 0.96 (2016-11-26)
### Added
- `plugman`: conformation dialogs.

### Changed
- `admin`: AdminLTE theme files updated: 2.3.2 -> 2.3.7.
- `auth`: 'password' driver loads by default now.
- `browser`:
    - Twitter Bootstrap updated: 3.3.4 -> 3.3.7;
    - Font Awesome updated: 4.6.3 -> 4.7.0.

### Fixed
- `auth_password`: translations and form button icon.
- `odm`: entity caching error handling.
- `plugman`: incorrect upgradable version number display.


## 0.95.3 (2016-11-25)
### Fixed
- `content_export`: error messages formatting.
- `theme`: error in `get_current()` API function.


## 0.95.2 (2016-11-24)
### Fixed
- `util`: callable name checking in `get_callable()`.


## 0.95.1 (2016-11-24)
### Fixed
- `auth_ulogin`: profile URLs overwriting while login.
- `comments`: check for registered comment drivers.
- `content`: translation error.
- `metatag`: favicon early URL building.
- `theme`: directory structure checking while searching for installed themes.


## 0.95 (2016-11-24)
### Added
- New package: `theme`.
- `assetman`:
    - new `tpl`'s global: `add_asset()`;
    - support for package aliases;
    - asset's build cache;
    - support for `$theme` placeholder in location specification.
- `browser`: new `tpl`'s global: `add_lib()`.
- `http`: new methods in `Session`: `get_message()`, `get_info_message()`, `get_success_message()`, 
  `get_warning_message()`, `get_error_message()`.
- `lang`: 
    - support for registering and using global variables in translation strings;
    - support for `$theme` placeholder in message id specification.
- `plugman`: support for remote `plugin.json` spec files.
- `settings`: new API function: `form_url()`.

### Fixed
- `router`: exception handling when theme's `exception` template is not accessible.
- `console`: checking environment type in `print_` functions.
- `http`: incorrect session's behaviour in some cases.

### Changed
- `assetman`: assets building console command moved to API function `build()`.
- `plugman`: plugins storage moved outside `app` directory.
- `theme`: themes storage moved outside `app` directory.
- `tpl`: `$theme` is default package name now in location specification without it.

### Removed
- Package `fb` moved to separate [plugin](https://github.com/pytsite/plugin-facebook).
- Package `lj` moved to separate [plugin](https://github.com/pytsite/plugin-livejournal).
- Package `tumblr` moved to separate [plugin](https://github.com/pytsite/plugin-tumblr).
- Package `twitter` moved to separate [plugin](https://github.com/pytsite/plugin-twitter).
- Package `vk` moved to separate [plugin](https://github.com/pytsite/plugin-vkontakte).


## 0.94 (2016-11-09)
### Added
- `admin`: new argument in `add_section()`: `sort_items_by`.
- `lang`: new argument in `register_package()`: `alias`.
- `plugman`: automatic plugins installation while application init.
- `tpl`: new argument in `register_package()`: `alias`.

### Fixed
- `content`: empty checkboxes on settings form in case when no models defined.
- `plugman`: disabling buttons on settings form while working with plugin.
- `validation`: regexp in `rule.Email`.

### Removed
- Package `disqus` moved to separate [plugin](https://github.com/pytsite/plugin-disqus).
- Package `google_analytics` moved to separate [plugin](https://github.com/pytsite/plugin-google_analytics).


## 0.93.3 (2016-11-05)
### Fixed
- `http`: error in `Session.has_message()`.


## 0.93.2 (2016-11-03)
### Fixed
- `file_storage_odm`: error while performing setup on fresh installs.


## 0.93.1 (2016-11-02)
### Fixed
- `odm`: unnecessary exception in `model.Entity.__eq__()`. 
- `util`: incorrect default HTML arguments list in `tidyfy_html()`.


## 0.93 (2016-11-02)
### Added
- New packages: `github`, `semver`, `odm_http_api`.
- `http`: new `Session()`'s methods: `flash_clear()` and `has_message()`.
- `http_api`: shortcut API functions: `get()`, `post()`, `patch()`, `delete()`.
- `reload`:
    - HTTP API support;
    - new API functions: `set_flag()`, `get_flag()`.
- `plugman`: installing, uninstalling plugins from GitHub.
- `router`:
    - new API function: `get_session_store()`;
    - automatic cleanup of old flash messages.
- `settings`: new API function: `is_defined()`.
- `tpl`: new API function: `is_package_registered()`.

### Changed
- `http`: flash messages related function names.
- `http_api`:
    - API function `register_package()` renamed to `register_handler()`;
    - API function `call_ep()` renamed to `call_endpoint()`;
    - signature of endpoint handlers.

### Fixed
- `widget`: processing table parts in `static.Table`.

### Removed
- Package `addthis` moved to separate [plugin](https://github.com/pytsite/plugin-addthis).


## 0.92.8 (2016-10-24)
### Fixed
- `auth_ulogin`: processing incorrect birth date from uLogin response.
- `currency`: error while updating `auth`'s HTTP API response. 


## 0.92.7 (2016-10-24)
### Removed
- `util`: non-necessary whitespaces cleaning while processing HTML code by related functions.


## 0.92.6 (2016-10-20)
### Fixed
- `auth`: checking user's status. 


## 0.92.5 (2016-10-19)
### Added
- `plugman`: first steps.
- `content`: new arguments for `f_get('body')`: `responsive_images`, `images_width`.
- `widget`: new widget: `static.Table`.

### Fixed
- `file_storage_odm`: non-necessary static images deletion while updating to version 0.90.
- `lj`: ugly line breaks while exporting content. 


## 0.92.4 (2016-10-16)
### Fixed
- `content`: comments counter recalculation.
- `file`: documentation.
- `file_storage_odm`: configuration parameters and documentation.


## 0.92.3 (2016-10-16)
### Fixed
- `browser`: `responsive` library is loading synchronously now. 
- `update`: automatic start of second stage.


## 0.92.2 (2016-10-15)
### Fixed
- `auth_storage_odm`: getting non-assigned user in `field.User`.
- `file_storage_odm`: support for dictionary argument in `field`'s classes.
- `http_api`: HTTP exceptions traceback logging.

### Removed
- `odm`: collection reindexing after each update.


## 0.92.1 (2016-10-15)
### Fixed
- `file_storage_odm`, `odm_auth`: more descriptive exception message.
- `http_api`: HTTP exceptions traceback logging.


## 0.92 (2016-10-14)
### Added
- New packages: `google_analytics`, `reload`.
- `auth`: `__eq()__` support in `model.AbstractUser`.
- `auth_storage_odm`: new ODM field: `Users`.
- `file`: authentication is necessary now while performing file uploads.

### Fixed
- `auth`: following/unfollowing HTTP API errors.
- `auth_storage_odm`: error while getting non-existent user's picture.
- `console`: error message localization.
- `contact_form`: missing translations.
- `file`: missing data in `model.AbstractFile.as_jsonable()`.
- `wallet`: improper `owner` field's type in `model.Account`. 


## 0.91.8 (2016-10-11)
### Fixed
- `auth_storage_odm`: switching user context while updating missing user's picture.


## 0.91.7 (2016-10-10)
### Fixed
- `auth`: switching user context while performing `sign_out()` call.
- `auth_storage_odm`: skipping unnecessary user status checking in `field.User`.
- `lj`: HTML escaping of image titles in `content_export`'s driver.


## 0.91.6 (2016-10-10)
### Fixed
- `lj`: error while getting image's URL in `content_export`'s driver.


## 0.91.5 (2016-10-09)
### Fixed
- `fb`: invalid setting of metatag 'fb:app_id'.
- `tumblr`: error while getting image's URL in `content_export`'s driver.


## 0.91.4 (2016-10-09)
### Fixed
- `disqus`: comments number calculating.
- `file_storage_odm`: processing of invalid entity IDs by driver's `get()` method.


## 0.91.3 (2016-10-07)
### Fixed
- `auth_storage_odm`: default user picture acquiring.
- `odm`: 
    - processing `ObjectId` arguments in `Query`;
    - casting of `$nin` operator's arguments.


## 0.91.2 (2016-10-07)
### Added
- `admin`: new `tpl`'s global: `admin_url()`.
- `content`: entity view endpoint's argument: `entity_tag_cloud`.
- `router`: CSS classes and ID in exception's template.

### Fixed
- `browser`: Twitter Bootstrap's add-ons.
- `content`: user context while content generation.
- `file_storage_odm`: missed `field.AnyFile._on_set()` return value.
- `odm`:
    - `__eq__`'s misbehaviour in `model.Entity`;
    - empty query checking in `Query.remove_criteria()`.
- `util`: improper processing of whitespaces by some regular expressions.
- `validation`: improper processing of whitespaces by some regular expressions.


## 0.91.1 (2016-09-30)
### Fixed
- `util`: newlines not deleted anymore while processing HTML code by related functions. 


## 0.91 (2016-09-30)
### Added
- New package: `errors`.
- `content`: searching for authored content entities while user deletion.
- `http_api`: support for '$theme' shortcut while package registration.

### Changed
- `assetman`: `tpl`'s globals renamed:
    - `assetman_url()` to `asset_url()`;
    - `assetman_css()` to `css_links()`;
    - `assetman_js()` to `js_links()`;
    - `assetman_inline()` to `inline_js()`.
- `metatag`: `tpl`'s global `metatag_all()` renamed to `metatags()`.
- `odm_ui`: all methods in `model.UIEntity` got prefix 'odm_'.

### Fixed
- `assetman`: error while adding non-permanent assets outside router's context.
- `auth_storage_odm`: issuing events.
- `browser`: `pytsite.responsive()` behavior.
- `taxonomy`: incorrect language setting while modifying term via UI.


## 0.90.9 (2016-09-26)
### Fixed
- `fb`: error while getting image URL in `content_export`'s driver.


## 0.90.8 (2016-09-26)
### Fixed
- `content_export`: error in finder query argument.


## 0.90.7 (2016-09-26)
### Fixed
- `auth_storage_odm`: authentication error of non-admin users.


## 0.90.6 (2016-09-26)
### Added
- `file`: `local_path` property to abstract models.

### Changed
- `fb`: settings moved from `reg` to `settings` module.
- `vk`: settings moved from `reg` to `settings` module.

### Fixed
- `content_export`: `owner`'s field type in `model.ContentExport`;
- `content_import`: processing errors while saving entities.
- `feed`: processing XML elements parsing errors.


## 0.90.5 (2016-09-25)
### Fixed
- `odm`: missed return value in `field.RefsList.sanitize_finder_arg()`.


## 0.90.4 (2016-09-24)
### Fixed
- `file_storage_odm`: values set hook errors in `field`'s classes.


## 0.90.3 (2016-09-23)
### Added
- `content`: Facebook's embedded videos extracting.
- `feed`: ability to skip unknown elements without exception in `rss.Parser`.
- `file`: 'real' user agent string while downloading remote files.
- `validation`: support for Facebook's video links in `rule.VideoHostingUrl`. 
- `widget`: support for Facebook's in `misc.VideoPlayer`.

### Fixed
- `auth_storage_odm`:
    - empty response from `get_users()`;
    - automatic `field.User`'s value in case of user deletion.
    - error while user deletion via admin ODM UI.
- `content_import`: exception handling.
- `feed`: error while URLs validation.
- `file_storage_odm`: automatic skipping non-existent files in `field` models.


## 0.90.2 (2016-09-22)
### Added
- `setup`: automatic updates applying after setup.

### Fixed
- `file_storage_odm`: stuck while updating process.


## 0.90.1 (2016-09-21)
### Added
- `auth`: `url` shortcut property in `model.AbstractUser`.
- `file`: `url` and `thumb_url` shortcut properties in `model.AbstractFile`.

### Fixed
- `admin`: active links on the sidebar.
- `auth`:
    - creating admin user while application's setup;
    - user picture size in `widget.Profile`.
- `auth_storage_odm`: entity locking issues.
- `content`: setting up roles while application's setup.


## 0.90 (2016-09-21)
### Added
- `odm`: new finder shortcut operators.

### Changed
- `auth`: totally refactored.
- `content_import`: event order.
- `file`: totally refactored.
- `permission` renamed to `permissions`.
- `odm`: `nonempty` argument of fields renamed to `required`.
- `odm_ui`: renamed some hook methods.

### Fixed
- `content`: parsing YouTube embedded videos.

### Removed
- `image`: removed completely in favour of `file` and `file_storage_odm`.


## 0.89.1 (2016-09-11)
### Fixed
- `content`: processing YouTube embedded videos.


## 0.89 (2016-09-11)
### Added
- `contact_form`: settings form.

### Changed
- Configuration parameter `app.autoload` renamed to `autoload`.
- Configuration parameter `server.name` renamed to `server_name`.

### Fixed
- `content`: settings form.
- `widget`: icon definition in buttons.
- `validation`: missed translations.

### Removed
- `pylibmc` dependency.
- `contact_form`: configuration parameter `contact_form.recipients`.


## 0.88.1 (2016-09-10)
### Added
- `content`: converting HTML YouTube's iframes ino `[vid]` tags.

### Changed
- Logo.
- `widget`: `static.VideoPlayer` moved to `misc.VideoPlayer`.

### Fixed
- `content`: first image tag deletion while saving entities.
- `form`: forward and backward icons on multi-step forms.
- `settings`: form cancel icon.


## 0.88 (2016-09-08)
### Added
- `auth`: new functions: `switch_user_to_system()`, `switch_user_to_anonymous()`, `restore_user()`.
- `comments`: new function: `delete_thread()`.
- `content`:
    - new configuration option `content.localization` and related behaviour;
    - comments deletion on content entity deletion.
- `lang`: new function: `get_primary()`.
- `odm`: new methods in `Finder`: `eq()`, `or_eq()`.
- `route_alias`: new configuration option `route_alias.localization` and related behaviour;
- `taxonomy`: new configuration option `taxonomy.localization` and related behaviour;

### Changed
- `comments`: format of `model.AbstractComment.as_jsonable()` response.
- `content`: format of `model.Content.as_jsonable()` response.
- `disqus`: thread IDs now is relative path by default.

### Fixed
- `admin`: processing sidebar URLs.
- `form`: default submit button icon.
- `odm_ui`: default cancel button icon.

### Removed
- `odm_auth`: functions `disable_perm_check`, `enable_perm_check`, `is_perm_check_enabled`.
- `json`: package removed.


## 0.87 (2016-09-04)
### Added
- `browser`: Font Awesome upgraded from 4.4.0 to 4.6.3.
- `content`: new field `author.picture` in `model.Base.as_jsonable()` return value.

### Changed
- `content`: format of `publish_time` field in `model.Content.as_jsonable()` return value. 


## 0.86.4 (2016-09-04)
### Changed
- `odm_auth`: argument renamed in `delete_entity()` HTTP API endpoint.
- `wallet`: currency title format in `widget.MoneyInput`. 

### Fixed
- `odm`: return `self` in `Aggregator.group()`.
- `odm_ui`: required input argument checking in `widget.EntitySelect`. 


## 0.86.3 (2016-09-02)
### Added
- `browser`:
    - Bootstrap's columns add-ons;
    - `costo.browser.parseLocation()` fields of returned value.


## 0.86.2 (2016-09-01)
### Changed
- Configuration parameter `lang.languages` shortcuted to `languages`. 
- Configuration parameter `currency.currencies` renamed to `currency.list`. 

### Fixed
- `currency`: unregistered HTTP API handler. 


## 0.86.1 (2016-08-30)
### Changed
- `odm_auth`: format of the response of the `POST odm_auth/entity` HTTP API endpoint.


## 0.86 (2016-08-30)
### Added
- `odm_auth`: 
    - new function: `dispense()`;
    - new HTTP API endpoint: `PATCH odm_auth/entity`.

### Changed
- `http_api`: explicit package registration is necessary now.

### Fixed
- `content`: stripping HTML in `model.Base.title` field.


## 0.85.3 (2016-08-29)
### Fixed
- `wallet`: JSONable value building in `field.Money`. 


## 0.85.2 (2016-08-25)
### Fixed
- `odm`: processing empty list/tuple values in `field.Ref()`.


## 0.85.1 (2016-08-25)
### Added
- `disqus`: support of renamed Disqus block with inline buttons. 


## 0.85 (2016-08-24)
### Changed
- `disqus`: settings moved from registry to UI settings form.
- `widget`: `static.tabs` moved to `select.tabs`.

### Fixed
- `addthis`: typo.
- `auth_storage_odm`: displaying empty permissions tab on the role administration page.


## 0.84.2 (2016-08-23)
### Added
- `content`: index for `video_links` in `model.Base`.
- `widget`: required arguments checking in `select.pager`.


## 0.84.1 (2016-08-23)
### Fixed
- `widget`: calculations in `select.pager`.


## 0.84 (2016-08-23)
### Changed
- `widget`: `static.pager` moved to `select.pager`.

### Added
- `widget`: support for AJAX requests in `select.pager`.


## 0.83.3 (2016-08-22)
### Fixed
- `validation`: processing of empty string in `rule.Regex`.


## 0.83.2 (2016-08-22)
### Fixed
- `util`: processing `remove_tags` argument in `tidyfy_html()`.


## 0.83.1 (2016-08-22)
### Added
- `widget`: new argument `unique` in `select.Checkboxes`.
- `util`: default value of argument `anchor` in `nav_link()`. 

### Fixed
- `widget`:
    - `base.Abstract`: check for `None` in `set_val()` instead of emptiness.
    - `select.Checkboxes` filtering empty values.


## 0.83 (2016-08-19)
### Added
- `addthis`: settings form.
- `admin`: store of collapsed state of sidebar. 
- `browser`: new JS library: `js-cookie`.
- `content`: part of the reg-settings moved to settings form.
- `mail`: settings form.
- `util`: new argument in `cleanup_list`: `uniquize`.
- `widget`: new constructor's argument and property in `input.StringList`: `unique`. 

### Changed
- `settings`: refactored.
- `lang`: syntax of sub-translation placeholders from `{term}` to `{:term}`.
- `reg`: method names.

### Fixed
- `auth_log`: missed translations.
- `validation`: typo in translations.

### Removed
- `browser`: `laodCSS` JS library.


## 0.82.6 (2016-08-18)
### Fixed
- `image`: non working HTTP API endpoints.


## 0.82.5 (2016-08-18)
### Added
- `google`: new method `addMarker()` in JS object `pytsite.google.maps.Map`.

### Changed
- `comments`: HTTP API.

### Fixed
- `comments`: reply notification email recipient.


## 0.82.4 (2016-08-13)
### Fixed
- `comments_native`: 
    - widget's layout on small screens;
    - UI error after comment delete.


## 0.82.3 (2016-08-13)
### Fixed
- `comments_native`: widget's layout on small screens. 


## 0.82.2 (2016-08-13)
### Added
- `comments`:
    - russian HTTP API documentation;
    - new property: `model.permissions`;
    - new HTTP API endpoint: `GET comments/settings`.
- `http_api`: new global argument: `language`. 
- `odm_auth`: HTTP API package alias.

### Fixed
- `flag`:
    - work of `is_flagged()` function for anonymous user;
    - typo in english translation;
    - russian HTTP API documentation.


## 0.82.1 (2016-08-13)
### Fixed
- `currency`: HTTP API endpoint alias, ODM permissions.
- `flag`: HTTP API endpoint alias, ODM permissions.
- `wallet`: ODM permissions.


## 0.82 (2016-08-13)
### Added
- `http_api`: endpoints aliasing.

### Changed
- `permission`: huge refactoring of many things.
- `http_api`: processing of endpoints.


## 0.81.3 (2016-08-13)
### Fixed
- `auth`: roles list for anonymous user.


## 0.81.2 (2016-08-13)
### Changed
- `auth_log`: removed 'view' permission for ODM model.
- Initial permissions setup in various packages.

### Fixed
- `auth`: removed usage of 'system' role.
- `auth_storage_odm`: entity locking in property setters. 
- `content`: 
    - permissions check for images deletion before content entity deletion;
    - disabling permissions check while updating taxonomy related entities.

### Removed
- `image`: 'view' permission.


## 0.81.1 (2016-08-12)
### Fixed
- `auth`: 'system' role creation point.


## 0.81 (2016-08-12)
### Added
- `auth`: new arguments in `get_sign_in_url()`: `add_query`, `add_fragment`.
- New package `comments_native`. 
- `comments`: 
    - base HTTP API functions;
    - email notifications about replies.
- `content`: 
    - email notifications about new comments;
    - new function: `find_by_url()`.
- `html`: support for 'disabled' argument in `Input`.
- `lang`: processing references to other message IDs in `t()`.
- `mail`: new function: `mail_from()`.
- `odm`:
    - `min_length` argument in `field.String`;
    - new field in `model.Entity`: `_depth`.
- `permission`: new event: `pytsite.permission.define`. 
- `route_alias`: new sub-module: `error`.

### Changed
- `auth`: 
    - `current_user()` renamed to `get_current_user()`;
    - `first_admin_user()` renamed to `get_first_admin_user()`.
- `odm_auth`: 
    `model.PermissableEntity` renamed to `model.AuthorizableEntity`;
    `model.AuthorizableEntity.check_perm()` renamed to `check_permissions()`
- `validation`: partly refactored.

### Fixed
- `auth_log`: disable permission check while creating ODM entities.
- `auth_storage_odm`: locking entities in property setters.
- `content`: exception raising in 'content:generate' console command.
- `content_import`: missed reset errors counter.
- `odm`:
    - lock check while setting field's value;
    - incorrect `is_empty()` work of `field.Integer`.
- `odm_ui`: href of 'Cancel' button in modification form.
- `widget`: processing `enabled` property in `input.Text`.

### Removed
- `comments_odm` in favour of `comments_native`.
- `image`: `odm_auth`'s `view` permission support.


## 0.80.28 (2016-08-09)
### Fixed
- `router`: processing exception-embedded responses. 


## 0.80.27 (2016-08-08)
### Added
- `util`: new function `format_call_stack_str()`.

### Fixed
- `auth`: 
    - unnecessary entity locking in `get_user()`;
    - double negation in `ep.profile_view()`.
- `auth_google`:
    - missed user locking.
- `odm`: 
    - logging, caching;
    - processing values in `field.RefsUniqueList`;


## 0.80.26 (2016-08-04)
### Added
- `flag`: documentation for HTTP API.

### Changed
- `flag`: refactored.

### Fixed
- `auth`: processing `UserNotExist` exception in `pytsite.router.dispatch` event handler.
- `router`: processing exceptions with embedded responses. 


## 0.80.25 (2016-08-04)
### Fixed
- `auth_storage_odm`: search user by access token.


## 0.80.24 (2016-08-03)
### Fixed
- `odm`: return value of `field.Ref` in case of entity deletion.


## 0.80.23 (2016-08-03)
### Fixed
- `util`: processing XML charrefs in `tidyfy_html()`.


## 0.80.22 (2016-08-02)
### Fixed
- `browser`: iterations limit in `responsive` library.


## 0.80.21 (2016-08-02)
### Added
- `widget`:new constructor's argument `language` in `base.Abstract`.
 
### Changed
- `http`: `inp` is cached property now.
- `lang`: writing 'Just now' instead of '0 seconds' in `time_ago()`.
 
### Fixed
- `odm`: valid types checking in `field.Enum`.
- `content`: permissions checking while processing `ep.index`. 


## 0.80.20 (2016-08-02)
### Fixed
- `widget`: current page number detection in `static.Pager`.


## 0.80.19 (2016-08-02)
### Fixed
- `odm`: empty values processing in `validation.FieldUnique` rule.


## 0.80.18 (2016-08-02)
### Fixed
- `validation`: exceptions throwing.
- `auth_storage_odm`: 'access_token' field name clash while processing user's form. 

### Removed
- `http`: automatic integers detection in request parameters.


## 0.80.17 (2016-07-31)
### Added
- `content`: new arguments in `model.Base.as_jsonable()`: `images_thumb_width`, `images_thumb_height`. 
- `image`: new function `align_length()`.

### Fixed
- `image`: automatic side aligning while resizing in `model.Image`.
- `odm_auth`: anonymous user checking in `check_permissions()`. 


## 0.80.16 (2016-07-31)
### Added
- `odm`: new field: `Enum`.

### Fixed
- `image`: lengths aligning while resizing.


## 0.80.15 (2016-07-31)
### Fixed
- `odm`: processing of setting empty string in `field.String`.  
- `auth_storage_odm`: user entity locking while changing followers and following.
- `flag`: JS code and HTTP endpoint.


## 0.80.14 (2016-07-30)
### Added
- `util`: new arguments in `tidyfy_html()`: `add_safe_tags` and `remove_tags`.

### Fixed
- `auth_ulogin`: `lang`'s package registration.


## 0.80.13 (2016-07-30)
### Added
- `odm`: new arguments in `field.String`: `strip_html`, `tidyfy_html`, `remove_empty_html_tags`.
- `content_import`: new event: `pytsite.content_import.import`.
- `util`: new function: `tidyfy_html()`.

### Fixed
- `browser`: parent width detection in `responsive`.
- `content`: images extraction from body while saving entity.
- `lang`: months names in English.
- `http_api`: arguments processing in JS methods.
- `content_import`: logic.

### Removed
- `js_api`: totally replaced by `http_api`.


## 0.80.12 (2016-07-27)
### Fixed
- `file`: error logging.
- `content`: inde endpoint arguments checking.
- `fb`, `tumblr`, `vk`: session requests timeout.
  

## 0.80.11 (2016-07-27)
### Added
- Project's logo images.

### Fixed
- `content_import`: limit maximum imported items per run to 1 because of moving to single-process work model.
- `fb`, `tumblr`, `vk`: session requests timeout.


## 0.80.10 (2016-07-23)
### Fixed
- `content_export`: exporter's entity improper locking.


## 0.80.9 (2016-07-23)
### Fixed
- `content`: improper MIME type of images in RSS enclosures.
- `feed`: typo while parsing arguments in `feed.rss.em.Enclosure`.


## 0.80.8 (2016-07-23)
### Fixed
Improper entities locking in various places.


## 0.80.7 (2016-07-23)
### Fixed
- `widget`: `None` value processing in `input.Integer` and `input.Decimal`.


## 0.80.6 (2016-07-23)
### Fixed
- `content_export`: exporter's entity improper locking.


## 0.80.5 (2016-07-23)
### Fixed
- `content_export`: exporter's entity proper locking.
- `odm`: support for `model` argument in `field.Ref` and `field.RefsList`.
- `odm_auth`: entities deletion via HTTP API.


## 0.80.4 (2016-07-23)
### Fixed
- `taxonomy`: new terms lock while saving.


## 0.80.3 (2016-07-22)
### Fixed
- `auth_storage_odm`: ODM object proper locking.


## 0.80.2 (2016-07-22)
### Fixed
- `content`: passing taxonomy term model to 'index' route. 


## 0.80.1 (2016-07-22)
### Changed
- Work in multiprocess mode is now considered unsafe and should be fixed in the future.

### Fixed
- Work in multithreaded mode.


## 0.80 (2016-07-20)
### Added
- New package `profiler`.

### Changed
- `mp` is now considered unsafe and not used anymore.
- `logger`: refactored.

### Fixed
- `file`: remote source URL escaping while creating new files.
- `widget`: delayed rendering issue in `BootstrapTable`. 


## 0.79.3 (2016-07-18)
### Fixed
- `content_import`: processing entity body's images, text and tags.


## 0.79.2 (2016-07-17)
### Fixed
- `content_import`: errors processing.


## 0.79.1 (2016-07-17)
### Added
- `content`: attaching 'pdalink' by `generate_rss()`.
- `auth`: session cookie deletion for signed out users.

### Fixed
- `feed`: elements content string conversation.
- `content`: empty RSS feed title issue.


## 0.79 (2016-07-16)
### Changed
- `feed`: totally refactored.

### Fixed
- `file`: URL escaping while loading file from remote source.


## 0.78.3 (2016-07-14)
### Fixed
- `odm_ui`: undefined sort field error in entities browser. 


## 0.78.2 (2016-07-14)
### Fixed
- `odm`: manual collection's name definition. 


## 0.78.1 (2016-07-13)
### Fixed
- `browser`: iframes auto resizing in `responsive` library.


## 0.78 (2016-07-11)
### Added
- `feed`: new RSS item children: `rss.VideoLink`.

### Fixed
- `widget`: automatic form step update of children widgets in `base.Container`.
- `odm_ui`: form step update while submitting. 
- `content_import`: non-working entity form.
- `content_export`: translations of ODM browser titles.


## 0.77.9 (2016-07-10)
### Fixed
- `content`: mail digest subject string translations.


## 0.77.8 (2016-07-10)
### Added
- `content`: new configuration parameter: `content.ep.index.per_page`.


## 0.77.7 (2016-07-10)
### Fixed
- `image`: missing 'Forbidden' HTTP exception throwing,
- `content`: english translations.
- `auth_storage_odm`: hide 'admin' role in ODM admin browser.


## 0.77.6 (2016-07-09)
### Fixed
- `content`: setting images' author while content generation from console.


## 0.77.5 (2016-07-09)
### Fixed
- `file`: updated to support latest `magic`'s update.


## 0.77.4 (2016-07-09)
### Changed
- `content`: `body` field of `model.Page` now is required by default.


### Fixed
- `router`: processing embedded response in HTTP exceptions.
- `assetman`:
    - maintenance mode enable while working with 'update' command in console mode;
    - showing help message instead of error if arguments has not been specified.  


## 0.77.3 (2016-07-08)
### Fixed
- `admin`, `form`, `contact_form`: async JS loading.
- `browser`: async JS loading in 'responsive' library.

### Removed
- `browser`: asynchronous loading of CSS links.


## 0.77.2 (2016-07-08)
### Added
- `assetman`: new arguments in `add()`: `async` and `defer`. 
- `browser`: asynchronous loading of CSS links. 


## 0.77.1 (2016-07-07)
### Added
- `content`: 'author' field in `model.Base.as_jsonable()` return value.


## 0.77 (2016-07-07)
### Added
- `auth`: new event: 'pytsite.auth.http_api.get_user'.
- `currency`: HTTP API 'get_list' endpoint.
- `file`: HTTP API 'get_file' endpoint.
- `http_api`: cookies cleaning from responses.
- `image`: 
    - new function `get_by_ref()`;
    - HTTP API endpoints: 'post_file', 'get_file'.
- `odm`: 
    - new function `resolve_refs()`;
    - new property: `model.Entity.ref_str`.
- `odm_auth`: HTTP API endpoints: 'get_entity', 'post_entity'.
- `widget`: support for Twitter Tokenfield's 'min_length' option. 

### Changed
- `auth`: access token TTL determined by HTTP session TTL by default.
- `odm_auth`: function `perm_check()` renamed to `check_perm()`.
- `odm`:
    - `model.Entity.as_dict()` renamed to `as_jsonable()`;
    - `field.Abstract.get_storable_val()` renamed to `as_storable()`;
    - `field.Abstract.get_serializable_val()` renamed to `as_jsonable()`.
    - improved `resolve_ref()`. 
- `file`: HTTP API endpoint 'post_upload' renamed to 'post_file'.

### Fixed
- `auth`: access token automatic prolongation while HTTP requests. 


## 0.76 (2016-07-01)
### Added
- `auth`:
    - new API functions: `base_path()`, `first_admin_user()`, `get_user_select_widget()`;
    - new exceptions: `RoleModifyForbidden`, `RoleDeleteForbidden`, `NoAdminUser`.
- `content`: permission check in 'view' endpoint.
- `http_api`: new function: `call_ep()`.
- `router`: optional redirect instruction inside exceptions.
- `image`: HTTP API endpoint for uploading.

### Changed
- `auth`: part of logic moved to `auth_storage_odm`. 
- `widget`: `Base` renamed to `Abstract`.
- `file`: file uploading via HTTP API slightly refactored.
- `form`: fully moved from `js_api` to `http_api`.
- `odm`: all arguments of `model.Entity.save()` are optional now.

### Fixed
- `admin`: automatic permission check and redirect for non-authenticated users.
- `auth_google`, `auth_ulogin`: user picture downloading and nickname generation.
- `content`: permissions issue while counting entity views.
- `odm`: cache keys missing error in finder.
- `odm_auth`: error in `is_perm_check_enabled()`. 
- `widget`: language and cookies settings in `misc.BootstrapTable`.


## 0.75.6 (2016-06-28)
### Fixed
- `content`: broken AJAX requests handling in `widget.EntitySelect`.


## 0.75.5 (2016-06-28)
### Fixed
- `content`: comments count recalculation.


## 0.75.4 (2016-06-28)
### Fixed
- `content`: comments count recalculation.
- `http_api`: response MIME type in case of simple string returned by endpoint.


## 0.75.3 (2016-06-26)
### Fixed
- `content`: performance issue while processing 'body''s `[img]` tags.


## 0.75.2 (2016-06-26)
### Fixed
- `auth`: error while displaying non-existent permissions in admin roles browser.
- `auth_log`: default sorting column in ODM browser.


## 0.75.1 (2016-06-26)
### Changed
- `widget`: client library of `misc.BootstrapTable` updated from 1.9.1 to 1.10.1.

### Fixed
- `widget`: default sort field processing in `misc.BootstrapTable`.


## 0.75 (2016-06-26)
Lots of undocumented work.


## 0.74 (2016-06-19)
Huge undocumented refactoring.


## 0.73.5 (2016-06-15)
### Fixed
- `auth`: creating new users.


## 0.73.4 (2016-06-15)
### Fixed
- `auth`: creating new users.


## 0.73.3 (2016-06-15)
### Fixed
- `auth`: creating new users.


## 0.73.2 (2016-06-15)
### Fixed
- `contact_form`: was broken.


## 0.73.1 (2016-06-15)
### Fixed
- `auth`: invalid router's session management.
- `auth_google`: invalid asset paths.


## 0.73 (2016-06-15)
Huge undocumented refactoring.


## 0.72.1 (2016-06-09)
### Changed
- `auth_ui`, `content`: custom endpoints names format.

### Fixed
- `taxonomy`: broken tokenfield's search endpoint.
- `content`, `flag`: invalid JS API endpoints calls.

## 0.72 (2016-06-09)
### Added
- New package: `auth_driver_google`.
- `auth`: sanitizing user's nicknames while setting.

### Changed
- 'password' authentication driver moved to separate package `auth_driver_password`.
- 'ulogin' authentication driver moved to separate package `auth_driver_ulogin`.

### Fixed
- `browser`: incorrect deferred object resolving in JS code.


## 0.71 (2016-06-06)
### Added
- New package: `http_api`.
- `auth`:
    - basic support of `http_api`;
    - access tokens generation functions;
    - new argument in `get_user()` function: `access_token`.
- `cache`: new drivers' method: `ttl()`.
- `content`: `http_api`'s endpoint: 'GET entity'.

### Changed
- `router`: format of rules' names.
- `js_api`: format of endpoints names.
- `auth`: signature of `sign_out()` API function and drivers' method.


## 0.70.1 (2016-06-02)
### Fixed
- `auth`, `contact_form`, `flag`, `content`: inaccessible `js_api`'s endpoints. 


## 0.70 (2016-06-02)
### Added
- New package: `http_api`.

### Changed
- `auth`:
    - hugely refactored;
    - `ulogin` moved to separate package.
    
- `ajax`: moved to `js_api`.
    
### Removed
- `browser`: 'jquery-mobile', 'smoothscroll', 'enllax'.


## 0.69.6 (2016-05-30)
### Added
- `content`: support for additional parameters in `[img]` tags.

### Changed
- `content`: signature of `find()` API's method.

### Fixed
- `content`: description auto fill on content's ODM UI forms.  


## 0.69.5 (2016-05-29)
### Added
- `browser`: new library: 'magnific-popup'.
- `db`: new event: 'pytsite.db.restore'.
- `odm`:
    - cache clearing after restoring database from dump.

### Changed
- `odm`: work with cache refactored.


## 0.69.4 (2016-05-29)
### Fixed
- `widget`: HTML layout of `select.LanguageNav`.


## 0.69.3 (2016-05-26)
### Added
- `wallet`: currency select in `widget.MoneyInput`.
- `form`: new property: `Form.path`.
- `currency`: sorting currencies on add.

### Fixed
- `odm_ui`:
    - entities deletion via AJAX requests;
    - checking permissions on entities deletion.
- `auth_ui`: profile edit button URL in `widget.Profile` template.


## 0.69.2 (2016-05-25)
### Fixed
- `admin`, `auth_ui`: incorrect profile links.
- `google`: map current location tracking.


## 0.69.1 (2016-05-25)
### Added
- `odm_ui`: support for redirection to newly created entity after submitting its form.

### Changed
- `auth_ui`:
    - `model.User.profile_view_url` now is `model.User.url`;
    - `model.User.profile_edit_url` now is `model.User.edit_url`.

### Fixed
- `auth`: nickname generation.
- `content`: default max files value while setting widgets in ODM UI form of `model.Base`.
- `odm_ui`: 'Cancel' button URL on modify forms. 
- `widget`: CSS in 'input.TypeaheadText'.


## 0.69 (2016-05-19)
### Added
- `odm`: new argument `first_save` in `_after_save()` hook.
- `auth_ui`: unfollowing confirmation.

### Changed
- `flag`: improved and refactored.

### Fixed
- `block`: translations.


## 0.68.2 (2016-05-17)
### Fixed
- `logger`: processing codec-related errors while writing data to log-file.


## 0.68.1 (2016-05-17)
### Fixed
- `tpl`: reading non-ascii template files. 


## 0.68 (2016-05-17)
### Added
- New package: `block`.

### Changed
- `content`: base entity classes refactored.

### Fixed
- `odm`: processing default values of fields.
- `odm_ui`: new entity hook: `ui_m_form_validate()`.


## 0.67.6 (2016-05-15)
### Changed
- `odm`: 
    - entities serialization hook refactored;
    - addition of list of entities as argument in `$in` finder's criteria.

### Fixed
- `google`: map center button hiding after map centering.


## 0.67.5 (2016-05-14)
### Added
- `google`: tracking map center while changing position.


## 0.67.4 (2016-05-13)
### Fixed
- `content`: inline JS code addition.
- `auth_ui`: profile view template.
- `widget`: CSS in `input.ListList`.

### Changed
- `browser`: JS function `getLocation()` renamed to `parseLocation()`.


## 0.67.3 (2016-05-12)
### Added
- `google`: various libraries to work with maps.
- `auth`: new ODM index on 'last_login'.

### Fixed
- `browser`: asset type detection while loading via AJAX request.

### Changed
- `auth_ui`: profile template, widget and processing endpoints.
- `geo`: position watching instead of `setInterval()` usage in `widget.Location`.

### Removed
- `reddit`: due to non-completeness.


## 0.67.2 (2016-05-05)
### Fixed
- `form`: error while recursive searching for widgets. 


## 0.67.1 (2016-05-04)
### Changed
- `auth_ui`: profile view and edit form improvements.
- `form`: processing container-like widgets.


## 0.67 (2016-05-01)
### Changed
- `auth`: permissions managements moved to separate package: `permission`.
- `odm_ui`: light refactoring.

### Fixed
- `odm`: non-working method `field.EntitiesRef.sub_val()`.
- `wallet`: various issues.


## 0.66.3 (2016-04-27)
### Fixed
- `cache`: work in multithreaded environments. 
- `mp`: work in multithreaded environments.


## 0.66.2 (2016-04-27)
### Fixed
- `cache`: work in multithreaded environments. 
- `mp`: work in multithreaded environments. 
- `odm`: work in multithreaded environments. 


## 0.66.1 (2016-04-27)
### Fixed
- `cache`: unpickling `None`s in 'redis' driver.


## 0.66 (2016-04-27)
### Added
- `content`: '_created' and '_modified' indices in `model.Content`.
- `currency`: suport for "short" currency titles.
- `google`:
    - `google_maps_map_link()` tpl's global;
    - new widget: `maps.widget.StaticMap`.
- `widget`: automatic non-form widgets initialization.

### Fixed
- `cron`: start precision.

### Removed
- `cache`: 'memory' and 'db' drivers.


## 0.65.1 (2016-04-24)
### Added
- `assetman`: new event: 'pytsite.assetman.build.after';


## 0.65 (2016-04-24)
### Added
- `geo`: automatic location update every 5 seconds in `widget.location`.

### Changed
- Moved part of application's initialization into theme's initialization.

### Fixed
- `form`: scrolling to erroneous fields on modal forms.


## 0.64 (2016-04-21)
### Added
- `odm`:
    - basic support for aggregation operations;
    - automatic collections reindex on every update.
- `widget`: new widgets% `select.Score` and `select.TrafficLightScore`.
- `flag`: big rework.


## 0.63 (2016-04-19)
### Added
- `odm`: support for '2dsphere' geo indexes.

### Changed
- `cron`: switched to uWSGI timer.


## 0.62.19 (2016-04-16)
### Fixed
- `taxonomy`: `widget.TokensInput` input processing by `set_val()`.
- `form`: submit button lock in case of non-200 AJAX response from server.


## 0.62.18 (2016-04-15)
### Fixed
- `form`: multiple checkboxes JS serialization. 


## 0.62.17 (2016-04-15)
### Changed
- `ckeditor`: updated to full 4.5.8 version.


## 0.62.16 (2016-04-15)
### Added
- `file`: new JS events in `widget.FilesUpload()`.
- `geo`: processing 'required' and 'autodetect' properties in `widget.Location`.
- `google`: processing 'required' property `maps.widget.AddressInput`.

### Changed
- `widget`: 'required' property moved from `Input` to `Base`.

### Fixed
- `lang`: thread safety in `lang()`.
- `form`: showing errors on client.


## 0.62.15 (2016-04-12)
### Fixed
- `taxonomy.widget.TokensInput`: setting value exception. 


## 0.62.14 (2016-04-12)
### Added
- `form`: new instance property: `form.Form.modal_close_btn`.

### Fixed 
- `odm`:
    - unexpected exception during pulling fields' data from cache;
    - entities comparison.
- `widget`: text automatic selection in text-related widgets.


## 0.62.13 (2016-04-10)
### Fixed
- `browser`: 'enllax' library minified JS. 


## 0.62.12 (2016-04-09)
### Fixed
- `content_import`: new form API usage.


## 0.62.11 (2016-04-08)
### Added
- `form`: new `pytsite.Form`'s attribute: 'prevent_submit'.


### Fixed
- `contact_form`: didn't worked.


## 0.62.10 (2016-04-07)
### Added
- `form`: smooth progress bar update while waiting for widgets from server.


## 0.62.9 (2016-04-07)
### Changed
- `ckeditor`: updated to version 4.5.8.

### Fixed
- `widget`: error in JS code of `widget.input.StringList`.


## 0.62.8 (2016-04-07)
### Fixed
- `google`: improper initialization of `google.widget.AddressInput`.
- `lang`: working in multithreaded environment.


## 0.62.7 (2016-04-07)
### Fixed
- `google`: duplicated include of Google API JS.


## 0.62.6 (2016-04-07)
### Added
- `form`: some improvements in JS parts.
- `file`: new parameters in `file.widget.FilesUpload`: 'show_numbers', 'dnd'.

### Fixed
- `geo`: assets loading in `geo.widget.Location`.


## 0.62.5 (2016-04-06)
### Fixed
- `form`: various fixes.


## 0.62.4 (2016-04-05)
### Fixed
- `widget`: incorrect page number processing from request input data in `widget.static.Pager`.
- `odm`: incorrect variable usage in `finder.Result.explain()`.
- `lang`: IETF language region completion.
- `browser`: disabled transitions in Bootstrap's progress bar.
- `form`: progress bar update precision.


## 0.62.3 (2016-04-05)
### Fixed
- `ajax`: typo.
- `form`: lazy setup on server side.


## 0.62.2 (2016-04-05)
### Fixed
- `form`: asynchronous widget loading.
- `ckeditor`: automatic update underneath textarea on changes.


## 0.62.1 (2016-04-04)
### Fixed
- `router`: work in multithreaded environment.


## 0.62 (2016-04-04)
### Added
- `form`: multi-step lazy forms. 


## 0.61.5 (2016-03-28)
### Fixed
- `admin`: dynamic paths prefix while asset additions. 


## 0.61.4 (2016-03-28)
### Added
- `assetman`: path-prefixed assets.

### Changed:
- `assetman`: `tpl`'s global `asset_url()` renamed to `assetman_url()`.

### Fixed
- `assetman`, `hreflang`, `metatag`: work in multithreaded environment.


## 0.61.3 (2016-03-28)
### Fixed
- `assetman`: work in multithreaded environment.


## 0.61.2 (2016-03-28)
### Fixed
- `db`: error while invoking 'db' console command.


## 0.61.1 (2016-03-25)
### Changed
- `file`: upload widget's JS library update.

### Fixed
- `content`: non-empty author check in Article and Page models.
- `image`: incorrect EXIF rotation directions.


## 0.61 (2016-03-24)
### Added
- `content`: improvements of 'content:generate' console command.
- `google`: basic geocoding API support.

### Changed
- `google`: names of configuration options.

### Fixed
- `auth`: error while checking session variable.
- `odm`: unsaved entity unlocking exception.
- `router`: errors of work in multithreaded environment.
- `wallet`: `is_empty` checking in `field.Money`.


## 0.60 (2016-03-23)
### Added
- `router`: support for multithreading.
- `auth`: new field in `User` model: 'last_ip'.

### Changed
- `auth`: `User`'s field 'geo_ip' is virtual now.

### Fixed
- `odm`: issues with multithreaded mode.
- `content`: error while displaying 'Propose' form.
- `cron`: autostarting issue.


## 0.59 (2016-03-20)
### Added
- New packages: `mp`, `google`.
- `odm`: new hook: `_setup_indexes()`.
- `ckeditor`: new 'stylescombo' plugin.
- `browser`:
    - new API method: `register()`;
    - new library: 'jquery-mobile'.
- `assetman`: support for regular expressions in `remove()`.
- `cache`:
    - total rework;
    - support for Redis and Database storage.
- `util`: new argument in `random_str()`: 'exclude'.

### Changed
- `odm`: `_setup()` hook renamed to `_setup_fields()`.
- `cron`: now works without storing data on filesystem.


## 0.58 (2016-03-13)
### Added
- `assetman`: TypeScript support.
- `browser`: new JS functions: `addJS()`, `addCSS()`, `getLocationHash()`.
- `auth`: JS functions: `getLoginForm()`, `isAnonymous()`.
- `odm`: serialization of entities, support for `$near` operator in finder.
- `form`: support of modal forms.
- `util`: new function `minify_html()`.

### Changed
- `admin`: AdminLTE theme updated from 2.1.0 to 2.3.2.
- `browser`: part of API moved to new `ajax` package.

### Removed
- `assetman`: `assetman_add()` `tpl`'s global.
- `auth`: `auth_login_form()` `tpl`'s global.

### Fixed
- `cache`: error while cleaning up pools.


## 0.57.2 (2016-02-24)
### Added
- New 'content:generate' console command argument: '--description-len'.


## 0.57.1 (2016-02-24)
### Fixed
- Post trimming in `lj`'s content_export driver.

## 0.57 (2016-02-23)
### Added
- Support for uWSGI auto-reloading via file touch.
- Two-step application update process.


## 0.56.6 (2016-02-23)
### Fixed
- Cron start in uWSGI request context.


## 0.56.5 (2016-02-23)
### Fixed
- Some ODM caching rework.


## 0.56.4 (2016-02-22)
### Fixed
- Incorrect ODM requests cache clearing.


## 0.56.3 (2016-02-22)
### Fixed
- Some rework of ODM caching.


## 0.56.2 (2016-02-22)
### Fixed
- UTF-8 issue while working with some files on MacOS.


## 0.56.1 (2016-02-20)
### Fixed
- Invalid 'debug' configuration default value while init.
- Disabled cron starting in console mode.


## 0.56 (2016-02-20)
### Fixed
- Dictionary checking in `util.dict_merge()`.

### Changed
- `cache` totally reworked.
- `odm`'s finder caching reworked.
- `cron` is now starting more precisely.
- Configuration parameter 'debug.enabled' renamed to 'debug'.
- Class `odm.Model` renamed to `odm.Entity`.
- Class `odm_ui.Model` renamed to `odm_ui.Entity`.
- 1 hour delay removed from `content_export`.


## 0.55.9 (2016-02-17)
### Fixed
- Errors in `fb` and `vk` `content_export`'s drivers.


## 0.55.8 (2016-02-17)
### Fixed
- OpenGraph issue in `fb._content_export.Driver`.


## 0.55.7 (2016-02-16)
### Fixed
- Route alias generation in `content.model.Content`.


## 0.55.6 (2016-02-15)
### Fixed
- Sortable refreshing in `file.widget.FilesUpload`.


## 0.55.5 (2016-02-15)
### Added
- Sortable thumbs in `file.widget.FilesUpload`.

### Fixed
- Processing img body tags in `content`'s model.


## 0.55.4 (2016-02-14)
### Added
- 'codesnippet' plugin to `ckeditor`.


## 0.55.3 (2016-02-14)
### Fixed
- Enabled native browser's spellchecker in `ckeditor`.


## 0.55.2 (2016-02-14)
### Added
- Support for 'code' and 'pre' tags in `ckeditor`.


## 0.55.1 (2016-02-14)
### Added
- New `browser`'s library: 'highlight'.


## 0.55 (2016-02-14)
### Added
- `odm`'s queries caching.
- New functions: `content.find_tag_by_alias()`, `content.find_tag_by_title()`.


## 0.54.3 (2016-02-11)
### Added
- New function: `util.parse_rfc822_datetime_str()`.

### Changed
- `util.rfc822_datetime()` renamed to `util.rfc822_datetime_str()`.
- `util._util.w3c_datetime()` renamed to `util._util.w3c_datetime_str()`.

### Fixed
- Improvements in `feed.rss.Reader`.


## 0.54.2 (2016-02-10)
### Added
- New `browser`'s library: 'gotop'.

### Changed
- `content.model.Content.publish_time_pretty` renamed to `content.model.Content.publish_date_time_pretty`.


## 0.54.1 (2016-02-09)
### Fixed
- Error in 'update' `console`'s command while compiling assets by `assetman`.


## 0.54 (2016-02-09)
### Added
- Declaring command options and processing errors improvements in `console`.


## 0.53.3 (2016-02-08)
### Added
- New console command: `auth passwd`.


## 0.53.2 (2016-02-08)
### Fixed
- Incorrect default argument types in `image.model.Image.get_html()`.


## 0.53.1 (2016-02-08)
### Added
- New `metatag`'s property support: 'og:url'.


## 0.53 (2016-02-07)
### Added
- New event: 'pytsite.odm.model.setup'.
- New configuration option: 'content.feed.length'.
- Support for `add_val()` method in `odm.field.Dict`.
- New `tpl`'s global: `url_parse()`.


## 0.52.6 (2016-02-07)
### Fixed
- Widgets placement in `content_export`'s ODM form.


## 0.52.5 (2016-02-06)
### Fixed
- Index definition parsing in `odm.Model.define_index()`.


## 0.52.4 (2016-02-05)
### Added
- Automatic conversion of BMP to JPEG in `image` while uploading.

### Fixed
- Invalid search algorithm in `taxonomy.find_by_title()`.


## 0.52.3 (2016-02-04)
### Added
- New argument in `content.widget.Search`: 'title_css'.
- Anchor HTML escaping in `util.nav_link()`.


## 0.52.2 (2016-02-04)
### Added
- New functions: `taxonomy.find_by_alias()`, `content.find_section_by_alias()`.


## 0.52.1 (2016-02-01)
### Fixed
- Error in `fb` `content_export`'s driver.


## 0.52 (2016-02-01)
### Added
- New `browser`'s library: 'slippry'.

### Changed
- `content_export`'s publish time delay is 1 hour now.


## 0.51 (2016-01-30)
### Added
- 'icon' argument in `util.nav_link()`.
- Tpl's global: `auth_login_url()`.
- Sorting by weight in `content.get_tags()`.

### Changed
- Tpl's global `get_current_user()` renamed to `auth_current_user()`.
- Tpl's global `get_login_form()` renamed to `auth_login_form()`.
- Tpl's global `get_logout_url()` renamed to `auth_logout_url()`.


## 0.50.3 (2016-01-29)
### Added
- New functions: `content.find_section_by_title()`, `taxonomy.find_by_title()`

### Fixed
- Suppress output of empty `taxonomy.widget.Cloud`.


## 0.50.2 (2016-01-29)
### Changed
- Huge refactoring of `content_export`.


## 0.50.1 (2016-01-26)
### Added
- Translations in `content_import`.


## 0.50 (2016-01-26)
### Added
- New package: `content_import`.
- `content`'s functions: `dispense_tag()`, `dispense_section()`.
- `odm`'s functions: `explain()`, `explain_winning_plan()`, `explain_parsed_query()` and `explain_execution_stats()`.

### Changed
- ODM fields 'section' and 'ext_links' moved from `content.model.Article` to `content.model.Content`.

### Removed
- `content`'s functions: `get_tag()`, `get_section()`.


## 0.49 (2016-01-23)
### Changed
- Refactoring of `console`, `form`, `content`, `feed`.

### Fixed
- Invalid date format in `sitemap` while generating index files.


## 0.48.5 (2016-01-19)
### Added
- New content's body 'img' tag option: 'skip_enlarge'.


## 0.48.4 (2016-01-19)
### Fixed
- Image sizes for OpenGraph stories.


## 0.48.3 (2016-01-18)
### Changed
- Step of responsive images resizing lowered to 100px.


## 0.48.2 (2016-01-16)
### Fixed
- Responsive image heights aligning.


## 0.48.1 (2016-01-15)
### Added
- New `content`'s model 'img' body tag argument: 'alt'.

### Changed
- Improved resizing logic in `image`.


## 0.48 (2016-01-14)
### Added
- New `browser`'s library: 'throttle'.
- Preliminary thumb image generation in `fb` content export driver.
- Improved behaviour of 'responsive' `browser`'s library.


## 0.47.4 (2016-01-13)
### Added
- Support for tags 'fb:app_id' and 'fb:admins' by `metatag`.


## 0.47.3 (2016-01-12)
### Changed
- Entity's comments count update logic in `content`.


## 0.47.2 (2016-01-12)
### Fixed
- Comments counting issue in `fb`.


## 0.47.1 (2016-01-12)
### Fixed
- Comments counting issue in `fb`.


## 0.47 (2016-01-12)
### Added
- New package: `comments`.
- Support for comments count by `fb` comments driver.


## 0.46.3 (2016-01-11)
### Fixed
- Single tag's attributes processing in `util.trim_str()`.
- Incorrect favicon metatag href via HTTPS requests.


## 0.46.2 (2016-01-11)
### Changed
- Configuration parameter 'contact.recipients' changed to 'contact_form.recipients'.


## 0.46.1 (2016-01-11)
### Fixed
- Language selector in `admin`'s template header.


## 0.46 (2016-01-11)
### Added
- New widget: `fb.widget.Comments`.
- New function: `lang.ietf_tag()`.
- Inline JavaScript code minification.


## 0.45 (2016-01-11)
### Changed
- `contact` renamed to `contact_form`.
- `odm_ui.UIMixin.ui_is_modification_allowed()` renamed to `odm_ui.UIMixin.ui_model_modification_allowed()`.
- `odm_ui.UIMixin.ui_is_deletion_allowed()` renamed to `odm_ui.UIMixin.ui_model_deletion_allowed()`.
- `browser`'s 'imagesLoaded' plugin updated from 3.1.8 to 4.0.0.

### Fixed
- Processing double quotes in HTML tag arguments in `util.trim_str()`.

### Removed
- `add_this` from `tpl`'s globals.


## 0.44.3 (2016-01-10)
### Fixed
- Incorrect HTML references processing in `util.trim_str()`.


## 0.44.2 (2016-01-09)
### Added
- New argument 'single_tags' in `util.trim_str()`.
- Support for <lj-like> tag by `lj` `content_export`'s driver.

### Fixed
- Incorrect HTML tags attribute values escaping in `util.trim_str()`.


## 0.44.1 (2016-01-09)
### Added
- Carriage returns stripping in `util.trim_str()`.


## 0.44 (2016-01-09)
### Added
- New function: `util.trim_str()`.
- Improvements in `lj` `content_export`'s driver.

### Changed
- `util.list_cleanup()` renamed to `util.cleanup_list()`.
- `util.dict_cleanup()` renamed to `util.cleanup_dict()`.
- `image.model.Image.get_html()` renamed to `image.model.Image.get_responsive_html()`.


## 0.43 (2016-01-07)
### Added
- New package: `lj`.
- New function: `util.md5_hex_digest()`.


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

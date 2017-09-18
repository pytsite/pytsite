# PytSite Changelog


## 5.0.4 (2017-09-18)
### Fixed
- `odm`: behaviour of `field.Virtual`.


## 5.0.3 (2017-09-14)
### Fixed
- `odm`: `Decimal` field serialization.


## 5.0.2 (2017-09-14)
### Fixed
- `auth`: missing event.


## 5.0.1 (2017-09-14)
### Fixed
- `odm`: entities caching issue.


## 5.0 (2017-09-13)
### Added
- New package `queue`.
- `odm`: distributed entity processing.
- `cache`: new functions: `l_push()` and `r_pop()`.

### Changed
- `util`: `get_class()` renamed to `get_module_attr()`.

### Removed
- `dlm` package.
- `form` caching.
- `threading`: locks related functions.


## 4.2 (2017-09-10)
### Added
- New package: `dlm` -- Distributed Lock Manager.
- `odm`: distributed entities caching.
- `cache`: methods for manage mappings.


## 4.1.1 (2017-09-08)
Fixed `pytsite.json`.


## 4.1 (2017-09-08)
### Added
- `odm_http_api`:
    - new endpoint: `get/entities`;
    - JavaScript API.


## 4.0.7 (2017-09-06)
### Fixed
- `plugman`: required plugins specs parsing.


## 4.0.6 (2017-09-06)
### Added
- `widget`: optional constructor argument `source_url_query_arg` in
  `input.TypeaheadText`.


## 4.0.5 (2017-09-06)
### Fixed
- `auth_password`: Twitter Bootstrap preload with sign-in form.
- `form`: display of hidden inputs.

### Changed
- `plugman`: '\*.upgrade' events renamed to '\*.update'.


## 4.0.4 (2017-09-04)
### Changed
- `util`: style is allowed now by default fo "p" tags in `tidyfy_html()`.


## 4.0.3 (2017-09-04)
### Fixed
- `validation`: support for lists, tuples and dicts in `rule.Url`.


## 4.0.2 (2017-09-04)
### Fixed
- `plugman`: updating plugins issue.


## 4.0.1 (2017-09-04)
### Added
- `assetman`: automatic updating of NPM packages.

### Fixed
- `setup`, `update`: installation and updating of pip packages.
- `theme`: error in settings form.
- `update`: missing events.

### Removed
- `package_info`: `check_requirements()` function.


## 4.0.0 (2017-09-03)
### Added
- `auth`: prompt for first admin password while setup.
- `console`: optional trace printing in `print_error()`.
- `github`: new argument `ref` in `repo_contents()`.
- `http_api`: verbose HTTP exceptions logging in debug mode.
- `odm`: new hook method in `Entity`: `_on_set_storable()`.
- `settings`: home page metatag settings.
- `util`: new functions: `is_url()`, `load_json`, `install_pip_package`,
  `get_installed_pip_package_info`, `get_installed_pip_package_version`,
  `is_pip_package_installed`.
- `valiadation`:  new rule: `UrlList`.

### Changed
- `admin`: sidebar sorting is now language aware.
- `odm`: `Entity.as_db_object()` renamed to `as_storable()`.
- `semver`, `package_info`, `plugman`: greatly refactored.
- `plugman': switched to HTTP API version 2.


## 3.1.2 (2017-08-18)
### Fixed
- `browser`: responsive images enlarging error is JS code.


## 3.1.1 (2017-08-17)
### Added
- `admin`: events on sidebar item add.


## 3.1 (2017-08-16)
### Added
- `assetman`: support for shim RequireJS's modules.
- `tpl`: new filter: `tojson`.

### Changed
- `assetman`:
    - RequireJS upgraded from 2.3.3 to 2.3.4;
    - JS resources now load synchronously by default.

### Fixed
- `assetman`: asynchronous resources loading error.


## 3.0.2 (2017-08-10)
### Fixed
- `file`: value processing in `widget.FilesUpload`.


## 3.0.1 (2017-08-09)
### Fixed
- `lang`: incorrect cache keys format.


## 3.0 (2017-08-09)
### Added
- `assetman`: asynchronous loading support in JS functions `loadJS()` and `loadCSS()`.
- `browser`: automatic preloading of JS assets in `twitter-bootstrap`.
- `file`:
    - new method: `get_multiple()`;
    - new argument in method `get()`: `suppress_exception`;
    - new exceptions: `error.Error`, `error.InvalidFileUidFormat`.
    - new method: `widget.FilesUpload.get_files()`.
- `lang`:
    - new event: `pytsite.lang.translate`;
    - new API functions: `on_translate()`, `clear_cache()`.
- `reload`: new API functiosn: `on_before_reload()`, `on_reload()`.
- `theme`: support for user defined messages translation.
- `widget`:
    - new widget: `input.Url`;
    - new option: `widget.Abstract.h_size_label`.

### Changed
- `events`: `first()` now returns single element instead of list.
- `file`: `widget.FilesUpload` now stores and returns files' UIDs instead of file objects.
- `html`: `Element.append()` now returns appended element instead of self.

### Removed
- `file`: support for options in `widget.FilesUpload`: `image_max_width` and `image_max_height`.
- `theme` support for separate theme settings form.


## 2.1 (2017-08-02)
### Added
- `threading`: new function `create_timer()`.

### Changed
- `cron`: eliminated usage of uwsgi's scheduler in favor of native threads.
- `router`: HTTP errors now log always, not only in debug mode.

### Fixed
- `odm`: enttites cache removed as it didn't work well with uWSGI threads.
- `odm_auth`: checking if entity is new in `model.f_get()`.
- `widget`: setting value issue in `select.Checkbox`.


## 2.0.11 (2017-08-01)
### Fixed
- `odm_auth`: missing entity locking.


## 2.0.10 (2017-08-01)
### Fixed
- `odm_auth`: missing return value.


## 2.0.9 (2017-08-01)
### Fixed
- `odm_auth`: automatic entity's owner setting in case if owner was deleted.


## 2.0.8 (2017-08-01)
### Fixed
- `odm_auth`: automatic entity's owner setting exception handling.

### Changed
- `router`: logging of 4xx errors performs only in debug mode now.


## 2.0.7 (2017-07-31)
### Fixed
- `assetman`: babelifying JS files.


## 2.0.6 (2017-07-31)
### Added
- `update`: automatic pulling application's configuration from git.
- `plugman`: automatic installing required plugins after application's update.


## 2.0.5 (2017-07-31)
### Fixed
- `update`: pulling all themes from git instead of only current one.


## 2.0.4 (2017-07-30)
### Added
- `settings`: new form's event.


## 2.0.3 (2017-07-30)
### Added
- `settings`: new form's event.


## 2.0.2 (2017-07-30)
### Fixed
- `form`: form's UID processing.
- `settings`: form's name setup.


## 2.0.1 (2017-07-29)
### Fixed
- `settings`: form's UID setup.


## 2.0 (2017-07-29)
### Added
- `auth`:
    - new API function: `get_auth_drivers()`;
    - new method: `driver.Authentication.get_description()` and associated property.
    - new methods: `model.AbstractUser.get/set_option()`.
- `auth_settings`: ability to select authentication driver via admin UI.
- `routing`: new property `Controller.files`.
- `util`: new argument in `mk_tmp_file()`: `subdir`.

### Changed
- `auth_password`: improved sign-in form.
- `pkg_util` renamed to `package_info`.
- `routing`: files now pass via separate controller's property, not in `args`.

### Fixed
- `auth`: argument checking in `auth:passwd` console command.
- `auth_web`: redirecting issues and missing session messages.
- `odm`: erroneous entities caching in cases where it isn't necessary.
- `widget`: horizontal sizing issue.

### Removed
- `auth_ulogin`: moved to separate plugin.


## 1.2 (2017-07-15)
### Fixed
Web login critical security issue.


## 1.1.3 (2017-07-14)
### Added
- `assetman`: new API function: `check_setup()`.

### Fixed
- `theme`: `assetman`'s setup checking and automatic setup during application startup.


## 1.1.2 (2017-07-14)
Fixed **setup.py**.


## 1.1.1 (2017-07-14)
Fixed **pytsite.json**.


## 1.1 (2017-07-14)
### Added
- `browser`: responsive backgrounds support in **pytsite.responsive**.
- `html`:
    - default value in signature of `Element.get_attr()`;
    - new methods in `Element`: `has_css()`, `add_css()`, `remove_css()` and `toggle_css()`.
- `settings`: default application's settings form implementation.
- `theme`: support for themes' settings.
- `tpl`:
    - new argument in `render()`: `issue_event`;
    - new API function: `on_render()`.

### Fixed
- `admin`: header menu issue.
- `browser`: visibility add-on classes in **twitter-bootstrap**.


## 1.0 (2017-07-03)
### Added
- New packages: `pkg_util`, `auth_settings`.
- `http_api`: new API function: `endpoint()`.
- `router`: automatic files addition in controller arguments.
- `theme`: (un)installation and update web, API and HTTP API functions.
- `util`: new API function: `mk_tmp_dir()`.
- `widget`: new widget: `input.File`.

### Changed
- `auth`: part of code decomposed to different packages: `auth_http_api`, `auth_profile`, `auth_ui`.
- `assetman`: arguments format in **assetman:build** console command.
- `reload`: call to `reload()` is now asynchronous.
- `semver`: refactored.

### Fixed
- `assetman`: error processing issue.
- `reload`: JS code.

### Removed
- `geo_ip`, `plugman`: legacy code.

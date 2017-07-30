# PytSite Changelog


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

# PytSite 2 Changelog


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

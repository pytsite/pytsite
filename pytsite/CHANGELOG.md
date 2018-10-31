# PytSite 8 Changelog


## 8.1.2 (2018-10-31)

Input data processing fixed in `http.Request`.


## 8.1.1 (2018-10-23)

Temporary fix of updating dependencies issue in `plugman`.


## 8.1 (2018-10-22)

- `formatters`: new constructor's parameter: `default`.
- `lang`: removed unused parameter `alias` from `register_package`.
- `plugman`:
    - removed unused console command `plugman:update`;
    - plugins dependencies processing partly fixed.
- `tpl`: removed unused function `is_package_registered()`.


## 8.0.4 (2018-10-12)

Unused `strip_lang_prefix` argument removed from `router.url()`.


## 8.0.3 (2018-10-06)

Bugfix of `plugman:install` console command.


## 8.0.2 (2018-10-06)

Cleanup, bugfixes in `package_info`, `pip`, `plugman` and `semver`.


## 8.0.1 (2018-10-04)

`pytsite.json` fixed.


## 8.0 (2018-10-04)

- `core`:
    - app's resources moved to `res` directory;
    - `app_load_uwsgi()` hook support removed.
- `plugman`:
    - new API functions added: `plugin_package_name()`, `on_pre_load()`,
      `on_load()`;
    - automatic `lang`'s and `tpl`'s resources registration added;
    - `plugins_path()` renamed to `plugins_dir_path()`;
    - `plugin_load_uwsgi()` hook support removed.
- `semver`:
    - new class `VersionRange` added;
    - API functions removed: `increment()`, `decrement()`, `minimum()`,
      `maximum()`;
    - `error.InvalidVersionString` renamed to `InvalidVersionIdentifier`.

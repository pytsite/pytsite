# PytSite 8 Changelog


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

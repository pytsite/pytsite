# PytSite 7 Changelog


## 7.31 (2018-08-20)

New methods in `plugman`: `on_install_all()`, `on_update_all()`.


## 7.30 (2018-07-16)

- `http.Session` refactored.
- `plugman`: new configuration option `disabled_plugins` added.
- `router`: session management improved.
- `routing`: new method: `Controller.warning()`.


## 7.29.2 (2018-06-21)

`app` package load errors processing fixed.


## 7.29.1 (2018-06-13)

- `routing`: encoding of filename URL fixed.
- `lang`: obsolete 'neutral' language support removed.


## 7.29 (2018-06-07)

- `router`:
    - `handle()`'s signature types updated;
    - filters processing chnaged.
- `routing`:
    - new class `Filter` added;
    - new method `Controller.file()` added;
    - new property `Controller.response` added;
    - new property `Rule.filters` added.


## 7.28.1 (2018-06-05)

Package version fixed.


## 7.28 (2018-06-05)

New argument `formats` added to `validation.rule.DateTime()`.


## 7.27.1 (2018-06-04)

Removed `settings` argument from `util.parse_date_time()`.


## 7.27 (2018-06-04)

Added `dateparser`'s arguments support in `util.parse_date_time()`.


## 7.26.2 (2018-06-03)

Bug fixed in `routing.Controller.validate()`.


## 7.26.1 (2018-06-03)

Empty value processing bug fixed in `Int` and `Float`.


## 7.26 (2018-06-03)

- `routing`: new method `Controller.validate()`.
- `formatters`: empty values processing issues fixed.


## 7.25 (2018-06-01)

- `lang`: singular forms of months names added.
- `tpl`: new global: `langs`.


## 7.24 (2018-06-01)

Changed signatures of `router.current_path()` and
`router.current_url()`.


## 7.23 (2018-05-30)

- `router.url()`:
  - argument `strip_lang` renamed to `strip_lang_prefix`;
  - new argument `add_lang_prefix` added.
- `errors`: new class `NotFound` added.


## 7.22 (2018-05-28)

`validation.Choice` renamed to `Enum` and its `options` constructor's
argument renamed to `values`.


## 7.21 (2018-05-23)

- `logger`: support for `*args` in module functions.
- `plugman`: support for hook `plugin_pre_install()`.


## 7.20 (2018-05-13)

- `cron`: tasks now start simultaneously.
- `events`: new arguments in `fire()`: `_concurrent`, `_wait`.
- `lang`: weekday names added.
- `plugman`: update hook call issue fixed.
- `queue`:
  - `Queue.put()` signature changed and now supports callables as a
    handler;
  - `Queue.execute()` argument `blocking_mode` rnamed to `wait`.
- `threading`: `run_in_thread()` now returns thread instance.
- `util`:
  - new function added: `parse_date_time()`;
  - functions removed: `parse_rfc822_datetime_str` and
    `parse_w3c_datetime_str`.


## 7.19.3 (2018-05-07)

Plugins hooks call issue #2 fixed in `plugman`.


## 7.19.2 (2018-05-07)

Plugins hooks call issue fixed in `plugman`.


## 7.19.1 (2018-05-06)

`plugman.is_management_mode()` now works right after start of the
PytSite, not after `plugman` starts.


## 7.19 (2018-05-06)

New API functions: `console.get_current_command()`,
`plugman.is_management_mode()`.


## 7.18.1 (2018-05-06)

Exception handling fixed in `plugman`'s updater.


## 7.18 (2018-05-06)

- New event `pytsite.load` added.
- New API function `on_pytsite_load()` added.
- `plugman`: plugins installation hooks calls fixed.


## 7.17 (2018-05-06)

- `http`: new public API classes: `Request`, `Response`,
  `RedirectResponse`, `JSONResponse`, `Session`.


## 7.16.3 (2018-04-25)

Event firing order fixed in `plugman`.


## 7.16.2 (2018-04-25)

Exceptions handling fixed in `plugman`.


## 7.16.1 (2018-04-25)

- `setup.py` fixed.
- Obsolete `TODO.md` removed.


## 7.16 (2018-04-25)

- `cron`: new API functions added: `on_start()`, `on_stop()`.
- `plugman`:
  - new API functions added: `on_pre_install()`, `on_install()`,
    `on_install_error()`.
  - Fixed some unexpected behaviour.

## 7.15 (2018-04-14)

New argument `as_list` added to `router.url()`.


## 7.14.1 (2018-04-06)

Version number fixed.


## 7.14 (2018-04-06)

- `http`: input data processing in `Request` fixed.
- `router`:
  - `get_no_cache()` and `set_no_cache()` merged into one
    function;
  - arguments passing order to controller fixed.
- `util.dicgt_merge` lists processing fixed.


## 7.13.1 (2018-03-17)

Year calculation fixed in `util.pretty_date()`.


## 7.13 (2018-03-15)

- `formatters`: new formatter: `AboveZeroInt`.
- `html`: new element: `Small`.
- `router`: fragment processing fixed in `url()`.
- `routing`: `ControllerArgs` now extends `dict`.


## 7.12 (2018-03-06)

New `tpl`'s global: `plugins`.


## 7.11.6 (2018-03-05)

Attributes list of some elements in `html` extended.


## 7.11.5 (2018-03-02)

`util.tidyfy_html()` fixed.


## 7.11.4 (2018-03-01)

'_' removed from filter list in `util.str_transform_1`.


## 7.11.3 (2018-02-21)

Error in `plugman`'s console commands fixed.


## 7.11.2 (2018-02-21)

Old `router`'s dependency removed.


## 7.11.1 (2018-02-20)

Error in `plugman:update` console command fixed.


## 7.11 (2018-02-20)

- New method `tpl.on_resolve_name()` added.
- `tpl.on_split_location()` renamed to `tpl.on_resolve_location()`.
- `pytsite.tpl@split_location` event renamed to
  `pytsite.tpl@resolve_location`.


## 7.10.4 (2018-02-16)

Automatic reloading after plugins install/update issue fixed.


## 7.10.3 (2018-02-15)

Application reload fix in `plugman`.


## 7.10.2 (2018-02-14)

Automatic uWSGI-reload request while updating plugins added.


## 7.10.1 (2018-02-13)

Typo fixed.


## 7.10 (2018-02-13)

- `cache`: fixed and refactored;
- `plugman`: pending updates check added.
- `update`: new methods added: `on_update_pytsite()`, `on_update_app()`.


## 7.9 (2018-02-11)

- Environment type 'uwsgi' renamed to 'wsgi'.
- Support for `__le__()` and `__ge()__` methods added to
  `semver.Version`.


## 7.8 (2018-02-11)

- New functions added: `console.print_normal()`, `plugman.on_update()`.
- `plugman` and `update` refactored.


## 7.7.2 (2018-02-10)

- New configuration option `plugman.autoload` added.


## 7.7.1 (2018-02-08)

- Core init code fixed.
- New exception `console.error.MissingOption` added.


## 7.7 (2018-02-07)

- Part of `util` moved to new `pip` module.
- `util.check_package_requirements()` moved to
  `package_info.check_requirements()`
- New exception `console.CommandExecutionError` added.


## 7.6.2 (2018-01-29)

Location's splitting issue in `tpl` fixed.


## 7.6.1 (2018-01-29)

Application's load hooks added.


## 7.6 (2018-01-16)

- `plugman`: two-stage update process added.
- `package_data`: cache related arguments added.


## 7.5.9 (2018-01-15)

New method `pytsite.on_app_load()` added.


## 7.5.8 (2018-01-15)

- `plugman`: `plugin_update()` hook's call order changed.


## 7.5.7 (2018-01-13)

- `plugman`: typo fixed.


## 7.5.6 (2018-01-13)

- `plugman`: maintenance mode during loading of plugins at start.


## 7.5.5 (2018-01-13)

- `plugman`: plugins upgrading issues fixed.


## 7.5.4 (2018-01-13)

- `plugman`: plugins upgrading issues fixed.


## 7.5.3 (2018-01-13)

- `plugman`: plugins upgrading issues fixed.


## 7.5.2 (2018-01-12)

- `plugman`: plugins upgrading issues fixed.


## 7.5.1 (2018-01-12)

- `plugman`: plugins upgrading issues fixed.


## 7.5 (2018-01-12)

### Added

- `core`: exceptions handling in application init code.
- `cron`: support for maintenance mode.
- `maintenance`: support for multiprocess environment.
- `plugman`: plugins update hook.

### Changed

- `plugman`: dependencies management improved.


## 7.4.2 (2018-01-08)

- `core`: new environment type: **testing** added.
- `plugman`: new method: `get()` added.


## 7.4.1 (2018-01-04)

- `util`: `remove_obsolete_files()` renamed to `cleanup_files()`.
- `log`: default log file's TTL increased from 1 day to 30 days.


## 7.4 (2018-01-03)

- `util`: empty directories check in `remove_obsolete_files()` added.
- `plugman`: fixed numerous errors and refactored.
- `cache`: dependency from `cron` fixed.


## 7.3 (2018-01-02)

### Added

- `cleanup`: `on_cleanup()` function.
- `plugman`:
  - plugins imports monitoring;
  - new API functions: `is_loading()`, `plugin_path()`.
- `util`: `remove_obsolete_files()` function.


## 7.2.8 (2017-12-29)

- `cache`: signature of `driver.Abstract.get_hash_item()` changed.


## 7.2.7 (2017-12-22)

- `plugman`: pip dependencies installation error fixed.


## 7.2.6 (2017-12-22)

- `update`: automatic application's dependencies update fixed.


## 7.2.5 (2017-12-21)

- `mongodb`: using exception instead of printing warning fixed.
- `plugman`: automatic loading plugin after installation fixed.


## 7.2.4 (2017-12-20)

- `plugman`: exception handling while plugins loading fixed.


## 7.2.3 (2017-12-20)

- `plugman`: plugin's module reloading while installation fixed.


## 7.2.2 (2017-12-19)

- `router`: `call()`'s arguments management fixed.


## 7.2.1 (2017-12-19)

### Fixed

- `lang`: message ID splitting.
- `logger`, `plugman`, `router`: logging issues.

### Removed

- `plugman`: `on_update()` API function.


## 7.2 (2017-12-18)

### Changed

- `plugman`: refactored and fixed issues with versions management.

### Fixed

- `core`: `jsmin` dependency.


## 7.1.1 (2017-12-14)

- `router`: filters processing fixed.


## 7.1 (2017-12-14)

- `routing`: `Controller`'s and `ControllerArgs`'s constructors'
  signatures changed.


## 7.0 (2017-12-13)

### Changed

- Events' names in various packages.
- `cache` refactored.

### Fixed

- `cleanup`: registry key name.
- `cron`: work in multiprocess environment.
- `lang`: `app_name`'s global return value.
- `plugman`: dependency detection.


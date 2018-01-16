# PytSite 7 Changelog


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


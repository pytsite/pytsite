# PytSite 6 Changelog


## 7.5.4 (2018-01-13)

### Fixed

- `plugman`: plugins upgrading issues.


## 7.5.3 (2018-01-13)

### Fixed

- `plugman`: plugins upgrading issues.


## 7.5.2 (2018-01-12)

### Fixed

- `plugman`: plugins upgrading issues.


## 7.5.1 (2018-01-12)

### Fixed

- `cache`: error in file driver.


## 7.5 (2018-01-12)

### Added

- `core`: exceptions handling in application init code.
- `cron`: support for maintenance mode.
- `maintenance`: support for multiprocess environment.
- `plugman`: plugins update hook.

### Changed

- `plugman`: dependencies management improved.



## 7.4.2 (2018-01-08)

### Added

- `core`: new environment type: **testing**.
- `plugman`: new method: `get()`.


## 7.4.1 (2018-01-04)

### Changed

- `util`: `remove_obsolete_files()` renamed to `cleanup_files()`.

### Fixed

- `log`: default log file's TTL increased from 1 day to 30 days.


## 7.4 (2018-01-03)

### Added

- `util`: empty directories check in `remove_obsolete_files()`.


### Changed

- `plugman`: fixed numerous errors and refactored.


### Fixed

- `cache`: dependency from `cron`.


## 7.3 (2018-01-02)

### Added

- `cleanup`: `on_cleanup()` function.
- `plugman`:
  - plugins imports monitoring;
  - new API functions: `is_loading()`, `plugin_path()`.
- `util`: `remove_obsolete_files()` function.


## 7.2.8 (2017-12-29)

### Changed

- `cache`: signature of `driver.Abstract.get_hash_item()`.


## 7.2.7 (2017-12-22)

### Fixed

- `plugman`: pip dependencies installation error.


## 7.2.6 (2017-12-22)

### Fixed

- `update`: automatic application's dependencies update.


## 7.2.5 (2017-12-21)

### Fixed

- `mongodb`: using exception instead of printing warning.
- `plugman`: automatic loading plugin after installation.


## 7.2.4 (2017-12-20)

### Fixed

- `plugman`: exception handling while plugins loading.


## 7.2.3 (2017-12-20)

### Fixed

- `plugman`: plugin's module reloading while installation.


## 7.2.2 (2017-12-19)

### Fixed

- `router`: `call()`'s arguments management.


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

### Fixed

- `router`: filters processing.


## 7.1 (2017-12-14)

### Changed

- `routing`: `Controller`'s and `ControllerArgs`'s constructors' signatures.


## 7.0 (2017-12-13)

### Changed

- Events' names in various packages.
- `cache` refactored.

### Fixed

- `cleanup`: registry key name.
- `cron`: work in multiprocess environment.
- `lang`: `app_name`'s global return value.
- `plugman`: dependency detection.


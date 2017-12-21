# PytSite 6 Changelog


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


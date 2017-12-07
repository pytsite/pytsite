# PytSite 6 Changelog


## 6.1 (2017-12-07)

### Added

- `cache`: file driver.
- `reg`: support for drivers.
- `plugman`: load and installation hooks.
- `util`: new argument `alphanum_only` in `random_password()`.

### Changed

- `cache`: redis driver moved to separate plugin.
- `reg`, `plugman`: refactored.
- `router`:
    - filters must be only controllers now;
    - `handle()` requires controller's class instead of an instance.

### Removed

- `setup` completely removed
- `router`: support for response in exception's body.



## 6.0.1 (2017-11-27)

### Fixed

- `mongodb`: invalid language resources IDs.
- `plugman`: recursion detection.


### Changed

- `reload`: part of the code moved to the separate plugin.



## 6.0 (2017-11-24)

### Changed

- `db` renamed to `mongodb`.

### Removed

- `admin`, `assetman`, `auth`, `auth_http_api`, `auth_password`,
  `auth_profile`, `auth_settings`, `auth_storage_odm`, `auth_ui`,
  `auth_web`, `browser`, `ckeditor`, `feed`, `file`, `file_storage_odm`,
  `form`, `geo`, `geo_ip`, `hreflang`, `odm`, `odm_auth`,
  `odm_http_api`, `odm_ui`, `permissions`, `robots`, `route_alias`,
  `settings`, `sitemap`, `theme`, `widget` moved to separate plugins.

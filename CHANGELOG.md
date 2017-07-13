# PytSite Changelog


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

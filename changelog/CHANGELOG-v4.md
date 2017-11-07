# PytSite 4 Changelog

## 4.2 (2017-09-10)
### Added
- New package: `dlm` -- Distributed Lock Manager.
- `odm`: distributed entities caching.
- `cache`: methods for manage mappings.


## 4.1.1 (2017-09-08)
Fixed `pytsite.json`.


## 4.1 (2017-09-08)
### Added
- `odm_http_api`:
    - new endpoint: `get/entities`;
    - JavaScript API.


## 4.0.7 (2017-09-06)
### Fixed
- `plugman`: required plugins specs parsing.


## 4.0.6 (2017-09-06)
### Added
- `widget`: optional constructor argument `source_url_query_arg` in
  `input.TypeaheadText`.


## 4.0.5 (2017-09-06)
### Fixed
- `auth_password`: Twitter Bootstrap preload with sign-in form.
- `form`: display of hidden inputs.

### Changed
- `plugman`: '\*.upgrade' events renamed to '\*.update'.


## 4.0.4 (2017-09-04)
### Changed
- `util`: style is allowed now by default fo "p" tags in `tidyfy_html()`.


## 4.0.3 (2017-09-04)
### Fixed
- `validation`: support for lists, tuples and dicts in `rule.Url`.


## 4.0.2 (2017-09-04)
### Fixed
- `plugman`: updating plugins issue.


## 4.0.1 (2017-09-04)
### Added
- `assetman`: automatic updating of NPM packages.

### Fixed
- `setup`, `update`: installation and updating of pip packages.
- `theme`: error in settings form.
- `update`: missing events.

### Removed
- `package_info`: `check_requirements()` function.


## 4.0.0 (2017-09-03)
### Added
- `auth`: prompt for first admin password while setup.
- `console`: optional trace printing in `print_error()`.
- `github`: new argument `ref` in `repo_contents()`.
- `http_api`: verbose HTTP exceptions logging in debug mode.
- `odm`: new hook method in `Entity`: `_on_set_storable()`.
- `settings`: home page metatag settings.
- `util`: new functions: `is_url()`, `load_json`, `install_pip_package`,
  `get_installed_pip_package_info`, `get_installed_pip_package_version`,
  `is_pip_package_installed`.
- `valiadation`:  new rule: `UrlList`.

### Changed
- `admin`: sidebar sorting is now language aware.
- `odm`: `Entity.as_db_object()` renamed to `as_storable()`.
- `semver`, `package_info`, `plugman`: greatly refactored.
- `plugman': switched to HTTP API version 2.

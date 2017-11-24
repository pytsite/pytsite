# PytSite 5 Changelog


## 5.6.9 (2017-11-18)
### Fixed
- `auth_http_api`: missing event call in `PATCH', 'auth/user` endpoint.


## 5.6.8 (2017-11-18)
### Fixed
- `core`, `theme`: automatic file structure while initialization.


## 5.6.7 (2017-11-18)
### Fixed
- `auth`: unnecessary manipulations with fields.
- `core`, `theme`: automatic file structure while initialization.


## 5.6.6 (2017-11-12)
### Fixed
- `auth_storage_odm`: model indexes.


## 5.6.5 (2017-11-12)
### Fixed
- `auth_http_api`: incorrect controller's argument name.
- `html`: missing whitespace in `Element.add_css()` method.


## 5.6.4 (2017-11-12)
### Added
- `html`: new element: `Nav`.
- `widget`: new widget: `Breadcrumb`.

### Fixed
- `widget`: support for Bootstrap4-style hiding.


## 5.6.3 (2017-11-12)
### Added
- `routing`: new properties `Controller.request`, `Controller.headers`.

### Changed
- `http_api`: automatically added arg `rule_name` renamed to
  `_pytsite_http_api_rule_name` and `http_api_version` renamed to
  `_pytsite_http_api_version`.
- `router`: automatically added arg `rule_name` renamed to
  `_pytsite_router_rule_name`.

### Fixed
- `auth_http_api`: value of `remains` field in responses of
  **GET auth/follows/:uid** and **GET auth/followers/:uid**.


## 5.6.2 (2017-11-07)
### Added
- `auth`, `auth_http_api`: returned fields to
  `model.AbstractUser.as_jsonable()`: `follows_count`,
  `followers_count`, `is_follows`, `is_followed`.
- `odm`: result caching of `Finder.count()`.

### Removed
- `auth`: `roles` field from `model.AbstractUser.as_jsonable()`.


## 5.6.1 (2017-11-07)
### Fixed
- `odm_http_api`: check for non-existent fields.


## 5.6 (2017-11-06)
### Added
- `auth`:
  - getters `follows_count`, `followers_count`, `blocked_users_count` in
    `model.AbstractUser`;
  - methods `is_follows()`, `is_followed()` in `model.AbstractUser`.
- `auth_http_api`: HTTP API version 2.
- `http_api`: passing arguments `http_api_version` and `rule_name` to
  all controllers.
- `odm`: new method in `Finder`: `delete()`.
- `router`: passing argument `rule_name` to all controllers.
- `testing`: new methods in `TestCase`: `assertHttpRespJsonEquals()`,
  `assertHttpRespJsonDictLen()`, `assertHttpRespJsonListLen()`.

### Changed
- `auth`: return value of `model.AbstractUser.as_jsonable()`.
- `auth_storage_odm`: way to store followers and blocked users.
- `http_api`: HTTP response header `PytSite-HTTP-API` renamed to
  `PytSite-HTTP-API-Version`.
- `routing`: `RulesMap.match()` now returns a list.
- `testing`: console command `test:run` renamed to `test`.

### Removed
- `auth`: setters `follows`, `followers`, `blocked_users` in
  `model.AbstractUser`.

### Fixed
- `routing`: processing JSON-dumpable args in `RulesMap.path()`.
- `testing`: string checking issue in
  `TestCase.assertHttpRespContentStrEquals()`.


## 5.5 (2017-10-25)
### Added
- `auth_http_api`: new HTTP API endpoint: `GET auth/users`.

### Changed
- `auth_http_api`: argument `response` of event
  `pytsite.auth.http_api.get_user` renamed to `json`.


## 5.4.5 (2017-10-24)
### Fixed
- `auth`, `auth_http_api`: user serialization error.


## 5.4.4 (2017-10-19)
### Fixed
- `widget`: default value of `h_size_row_css` argument in `Abstract`'s
  constructor.


## 5.4.3 (2017-10-18)
### Fixed
- `auth_storage_odm`: infinite recursion.

### Removed
- `odm`: automatic reindexing on update.


## 5.4.2 (2017-10-18)
### Fixed
- `auth_storage_odm`: infinite recursion.
- `auth_web`: error notification.


## 5.4.1 (2017-10-18)
### Added
- `widget`: new argument in `Abstract`: `h_size_row_css`.

### Fixed
- `auth_password`: form's layout.


## 5.4 (2017-10-18)
### Added
- `assetman`: support for multiple `path_prefix` and
  `exclude_path_prefix` arguments in `preload()`.
- `auth`:
    - new methods in `model.AuthEntity`: `add_to_field()`,
      `remove_from_field()`;
    - new methods in `model.AbstractUser`: `add_blocked_user()`,
      `remove_blocked_user()`;
    - new property `model.AbstractUser.blocked_users`.
- `auth_http_api`: new endpoints: `POST | DELETE auth/block_user/<uid>`.
- `auth_password`: support for Twitter Bootstrap 4.
- `auth_storage_odm`: new argument in `field.User` and `field.Users`:
  `disallowed_users`.

### Changed
- `auth`: methods `add_role()`, `remove_role()`, `add_follower()`, `remove_follower()`,
  `add_follows()`, `remove_follows()`of the `model.AbstractUser` is not abstract now.


## 5.3.4 (2017-10-16)
### Fixed
- `auth_http_api`: user's picture update issue.


## 5.3.3 (2017-10-13)
### Added
- `assetman`: new argument in `preload()`: `exclude_path_prefix`.
- `util`: support for Twitter Bootstrap 4 in `nav_link()`.

### Changed
- `router`: hook route `pytsite_router_exception` renamed to
  `router_exception`.


## 5.3.2 (2017-10-12)
### Changed
- `router`: hook route `$theme@exception` renamed to
  `pytsite_router_exception`.

### Fixed
- `permissions`, `settings`: translations.


## 5.3.1 (2017-10-11)
### Changed
- `odm`: entity delete-related event names.


## 5.3 (2017-10-10)
### Added
- `odm`:
    - cache manipulation argument in `Finder`'s methods.
    - new event: **pytsite.odm.finder_cache.clear**.

### Changed
- `odm`:
    - `Finder.where_text()` renamed to `Finder.text()`;
    - `Finder.or_where_text()` renamed to `Finder.or_text()`.
    - `Finder.remove_where()` renamed to `Finder.remove_field()`.
    - `Finder.remove_or_where()` renamed to `Finder.remove_or_field()`.


## 5.2.6 (2017-10-09)
### Fixed
- `widget`: cookie storage uasge in `misc.BootstrapTable`.


## 5.2.5 (2017-10-08)
### Fixed
- `odm`: circular references issue handling in `field.Ref` and
  `field.RefsList`.


## 5.2.4 (2017-10-08)
### Fixed
- `odm`: circular references issue handling in `field.RefsList`.


## 5.2.3 (2017-10-08)
### Added
- `auth`: `model.AbstractUser.has_permission()` now accepts list and
  tuple as an argument.


## 5.2.2 (2017-10-05)
### Fixed
- `odm`: default value processing in fields.


## 5.2.1 (2017-10-02)
### Fixed
- `auth_web`: session deletion issue.


## 5.2 (2017-10-02)
### Added
- `browser`: Twitter Bootstrap 4 Alpha.
- `http_api`: new tpl global: `http_api_endpoint`.
- `router`: new API function: `delete_session()`.
- `settings`: new tpl globals: `app_name` and `app_version`.

### Fixed
- `assetman`: synchronous JS code loading.
- `auth_web`: users' sessions prolongation and deletion.
- `validation`: empty values validation issue in `rule.Url`.


## 5.1.1 (2017-09-24)
### Fixed
- `file_storage_odm`: missing ODM entity exception handling.


## 5.1 (2017-09-24)
### Added
- `odm`:
    - entities cache TTL;
    - aggregation method `lookup()`.

### Changed
- `odm`: entities cache pool name.

### Fixed
- `odm`: aggregator's pipeline processing.


## 5.0.6 (2017-09-20)
### Added
- `http_api`: new argument in `handle()`: `defaults`.
- `semver`: new functions: `increment()`, `decrement()`.

### Fixed
- `plugman`: dependencies checking.


## 5.0.5 (2017-09-18)
### Fixed
- `plugman`: dependencies checking.


## 5.0.4 (2017-09-18)
### Fixed
- `odm`: behaviour of `field.Virtual`.


## 5.0.3 (2017-09-14)
### Fixed
- `odm`: `Decimal` field serialization.


## 5.0.2 (2017-09-14)
### Fixed
- `auth`: missing event.


## 5.0.1 (2017-09-14)
### Fixed
- `odm`: entities caching issue.


## 5.0 (2017-09-13)
### Added
- New package `queue`.
- `odm`: distributed entity processing.
- `cache`: new functions: `l_push()` and `r_pop()`.

### Changed
- `util`: `get_class()` renamed to `get_module_attr()`.

### Removed
- `dlm` package.
- `form` caching.
- `threading`: locks related functions.

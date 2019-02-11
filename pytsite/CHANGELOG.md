# PytSite 8 Changelog


### 8.9 (2019-02-11)

Support of `^` and `~` shortcuts in version range specifications in
`semver` package.


### 8.8.1 (2019-02-07)

Various bugfixes in `router`.


### 8.8 (2019-01-07)

Changes in `cache`:
- new methods in `driver.Abstract`: `expire()`, `type()`, `list_len()`,
  `get_list()`, `put_list()`, `list_r_push()`, `list_l_pop()`;
- New `ttl` argument added to method `put_hash_item()`;
- `driver.Abstract.l_push()` renamed ro `list_l_push()`;
- `driver.Abstract.r_pop()` renamed ro `list_r_pop()`.


### 8.7.3 (2019-01-02)

- `router.url()` fixed.
- `html.Li` fixed.


## 8.7.2 (2018-12-21)

`router.is_base_url()` fixed.


## 8.7.1 (2018-12-20)

`router.is_main_host()` fixed.


## 8.7 (2018-12-20)

- New function: `router.is_main_host()`.
- New `tpl`'s global: `is_main_host()`.
- `router.server_name()`'s `force_config` arg renamed to `use_main`.
- `router`'s `base_url()`, `url()` and `current_url()`'s
  `force_config_server_name` arg renamed to `use_main_host`.


## 8.6.1 (2018-12-20)

New `force_config_server_name` arg in `router.base_url()` function.


## 8.6 (2018-12-20)

- New `force_config` arg in `router.server_name()` function.
- New `force_config_server_name` arg in `router.url()` function.


## 8.5 (2018-12-18)

New `validation`'s rule: `DNSName`.


## 8.4.2 (2018-12-18)

`validation.rule.Regex` fixed.


## 8.4.1 (2018-12-12)

`formatters.JSONArray` and `formatters.JSONObject` default value
setting fixed.


## 8.4 (2018-12-11)

- New `routing.ControllerArgs.add_formatter()`'s arg: `use_default`.
- `http`:
    - new class `Headers` added;
    - new `response.JSON`'s constructor arg `headers` added.
- `formatters`:
    - `JSON` got new constructor's arg `allowed_type`;
    - `JSONArrayToList` renamed to `JSONArray`;
    - `JSONObjectToDict` renamed to `JSONObject`;
    - `JSONArrayToTuple` removed.


## 8.3 (2018-12-06)

- Signature of `routing.ControllerArgs.__init__()` changed.
- New methods added to `routing.ControllerArgs`: `rm_formatter()`,
  `rm_validation()`.


## 8.2 (2018-11-14)

- New formatters added: `Transform`, `Enum`.
- New arguments added to `Str` formatter: `min_len`, `lower`, `upper`.


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

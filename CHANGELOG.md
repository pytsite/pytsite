# PytSite 9 Changelog

For previous versions see [changelog](changelog/) folder.


### 9.3.6 (2019-07-29)

Error in `console update` fixed.


### 9.3.5 (2019-07-29)

Requirements typo fixed.


### 9.3.4 (2019-07-29)

Updating of pip packages on `console update` fixed.


### 9.3.3 (2019-07-27)

Resetting of `Cache-Control`'s `max-age` parameter fixed.  


### 9.3.2 (2019-07-26)

- `Cache-Control`'s `max-age` parameter is not set by default now.
- `Cache-Control`'s `must-revalidate` and `proxy-revalidate` added.  


### 9.3.1 (2019-07-24)

- `Cache-Control` values setting fix.
- `Cache-Control: max-age` set to `0` by default.


### 9.3 (2019-07-24)

`ETag` HTTP header generation enabled for `GET` methods by default.


### 9.2.1 (2019-07-18)

Missing `router`'s public API function added.


### 9.2 (2019-07-18)

- New methods added to the `router`: `no_store()`, `private()` and `max_age()`.
- `Cache-Control` HTTP response header formatting fixed.


### 9.1 (2019-07-17)

New argument `fields` added to `validation.Validator.validate()` method.


### 9.0.1 (2019-07-13)

Missing update of locally installed plugins fixed.


### 9.0 (2019-07-13)

- `html` moved to separate PyPi package 
  [htmler](https://github.com/ashep/htmler).
- `semver` moved to separate PyPi package 
  [semaver](https://github.com/ashep/semaver).
- `util.dict_merge()` moved to separate PyPi package 
  [dicmer](https://github.com/ashep/dicmer).
- `testing` removed.

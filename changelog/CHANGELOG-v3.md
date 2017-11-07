# PytSite 3 Changelog

## 3.1.2 (2017-08-18)
### Fixed
- `browser`: responsive images enlarging error is JS code.


## 3.1.1 (2017-08-17)
### Added
- `admin`: events on sidebar item add.


## 3.1 (2017-08-16)
### Added
- `assetman`: support for shim RequireJS's modules.
- `tpl`: new filter: `tojson`.

### Changed
- `assetman`:
    - RequireJS upgraded from 2.3.3 to 2.3.4;
    - JS resources now load synchronously by default.

### Fixed
- `assetman`: asynchronous resources loading error.


## 3.0.2 (2017-08-10)
### Fixed
- `file`: value processing in `widget.FilesUpload`.


## 3.0.1 (2017-08-09)
### Fixed
- `lang`: incorrect cache keys format.


## 3.0 (2017-08-09)
### Added
- `assetman`: asynchronous loading support in JS functions `loadJS()` and `loadCSS()`.
- `browser`: automatic preloading of JS assets in `twitter-bootstrap`.
- `file`:
    - new method: `get_multiple()`;
    - new argument in method `get()`: `suppress_exception`;
    - new exceptions: `error.Error`, `error.InvalidFileUidFormat`.
    - new method: `widget.FilesUpload.get_files()`.
- `lang`:
    - new event: `pytsite.lang.translate`;
    - new API functions: `on_translate()`, `clear_cache()`.
- `reload`: new API functiosn: `on_before_reload()`, `on_reload()`.
- `theme`: support for user defined messages translation.
- `widget`:
    - new widget: `input.Url`;
    - new option: `widget.Abstract.h_size_label`.

### Changed
- `events`: `first()` now returns single element instead of list.
- `file`: `widget.FilesUpload` now stores and returns files' UIDs instead of file objects.
- `html`: `Element.append()` now returns appended element instead of self.

### Removed
- `file`: support for options in `widget.FilesUpload`: `image_max_width` and `image_max_height`.
- `theme` support for separate theme settings form.

# PytSite Changelog

## 0.2.10 (2015-07-24)
### Added
- `[img:N:link_orig]` tag support in `pytsite.content.model.Content` models.

## 0.2.9 (2015-07-24)
### Added
- Twitter content cross posting. 

### Changed
- `pytsite.poster` moved to `pytsite.export` and refactored.
- `pytsite.oauth` removed.

### Fixed
- Handling lost connections in `pytsite.core.db`.
- Route alias generation in `pytsite.content.model.Article`.

## 0.2.8 (2015-07-22)
### Fixed
- YouTube links validation in `pytsite.core.validation.rule.VideoHostingUrl` 

## 0.2.7 (2015-07-22)
### Fixed
- Catch exceptions in `pytsite.core.mail.Message.send()`.
- YouTube links detection in `pytsite.core.widget.static.VideoPlayer()`.

## 0.2.6 (2015-07-22)
### Added
- `pytsite.settings`:
    - Permissions support.

### Changed
- `pytsite.core.assetman` refactored.
- `pytsite.core.client` improved and renamed to `pytsite.core.browser`.
- `pytsite.content.model.Content` publish time widget is now visible for non admins.
- `pytsite.core.mail`: asynchronous messages delivery. 

## 0.2.4 (2015-07-21)
### Fixed
- Incorrect value of 'og:url' in `pytsite.content.eps.view`. 

## 0.2.3 (2015-07-21)
### Added
- Support for 'author' and 'og:url' in `pytsite.core.metatag`.

## 0.2.2 (2015-07-21)
### Added
- `pytsite.core`:
    - Support for 'article:author' and 'article:publisher' in `metatag`.

### Fixed
- setup.py
- Host and port usage in `db:*` console commands.
- Permissions check in `pytsite.admin.sidebar`.
- Permissions check in `pytsite.odm_ui`.

## 0.2.1 (2015-07-21)
### Fixed
- setup.py

## 0.2.0 (2015-07-21)
### Added
- New plugins: `pytsite.oauth`, `pytsite.twitter`, `pytsite.poster`, `pytsite.page`, `pytsite.add_this`.
- Some english and ukrainian translations.
- `pytsite.core`:
    - SSL and authorization basic support in `pytsite.core.db`.
    - New events:
        - `odm.entity.pre_save`;
        - `odm.entity.save`.
    - New validation rules:
        - `pytsite.core.validation.rule.ListListItemNotEmpty`;
        - `pytsite.core.validation.rule.ListListItemUrl`;
        - `pytsite.core.validation.rule.VideoHostingUrl`.
    - New `args` argument in `pytsite.core.odm.Model.t()`.
    - New widgets: 
        - `core.widget.static.Pager`;
        - `core.widget.input.StringList`;
        - `core.widget.static.VideoPlayer`.
    - New functions:
        - `pytsite.core.util.list_cleanup()`;
        - `pytsite.core.util.dict_cleanup()`;
        - `pytsite.core.util.nav_link()`.
    - New `pytsite.core.tpl` globals: `url()`, `current_url()`, `base_url()` , `endpoint_url()`, `nav_link()`.
    - Sorting ability in `pytsite.odm.field.RefList.get_val()`.
    - New console commands:
        - `db:dump`
        - `db:restore`
    - Support for some OpenGraph and Twitter properties in `pytsite.core.metatag`.
- `pytsite.auth`:
    - New ODM `pytsite.auth.model.User` properties: `full_name`.
- `pytsite.content`:
    - New public package method: `pytsite.content.create()`
    - `pytsite. content.model.Content` model:
        - Processing `[img]` and `[vid]` body tags.
        - New field properties.
        - New events `content.entity.pre_save`, `content.entity.save`.
    - "Propose content" form.
    - Weekly email digest subscription.
    - SEO settings form for home page.
    - Support for OpenGraph and Twitter meta tags.
    - Simple content search.
- `pytsite.ckeditor`:
    - Images upload.
- `pytsite.file`:
    - New ODM `pytsite.file.model.File` properties: `url`, `path`, `abs_path`.
    - New field: `attached_to`.
- `pytsite.odm_ui`:
    - New `stage` argument in `pytsite.odm_ui.UIMixin.setup_m_form()` hook.
- `pytsite.route_alias`:
    - New `pytsite.route_alias.model.RouteAlias` properties: `alias`, `target`, `language`.
- `pytsite.taxonomy`:
    - New ODM `pytsite.taxonomy.model.Term` properties: `title`, `alias`, `language`, `weight`, `order`.

### Changed
- `pytsite.core.widget` plugin:
    - New argument in `geo.widget.SearchAddress`: `autodetect`. 
- `pytsite.geo` plugin:
    - New `autodetect` argument in `geo.widget.SearchAddress`.
- `pytsite.auth`
    - Config parameter changed `auth.auto_signup` -> `auth.allow_signup`.
- `pytsite.admin` plugin templates improvements.
- `pytsite.core.validation.rule.Url` now can work with lists and dicts.
- `pytsite.core.widget.input.CKEditor` moved to `ckeditor.widget.CKEditor`.
- `pytsite.tag` joined with `pytsite.content`.

### Fixed
- Empty configuration files read error.
- Incorrect usage of 'server_name' configuration value in `pytsite.core.router`.
- Check for app assets directory existence during `lang:build` console command.
- Exceptions handling during `odm_ui`'s form submit.
- Router's `current_url` incorrect behaviour in some situations.
- Incorrect entity caption field get in `odm_ui.widget.ODMSelect`.
- Incorrect method call in `pytsite.admin@tpl/header.jinja2`.
- Issue with `core.odm.Model.t()` in inheritance cases.
- Incorrect return value of `core.http.request.values_dict` in case of list input.
- Non-working JS for `core.widget.select.DateTime()`.
- Open files leak in `pytsite.file.create()`.

## 0.1.0 (2015-07-01)
First release.

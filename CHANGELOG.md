# PytSite Changelog

## Unreleased (2015-07-15)
### Added
- New plugins: `pytsite.oauth`, `pytsite.twitter`, `pytsite.poster`, `pytsite.page`, `pytsite.add_this`.
- Some english and ukrainian translations.
- `pytsite.core`:
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
- `pytsite.auth`:
    - New ODM `pytsite.auth.model.User` properties: `full_name`.
- `pytsite.content`:
    - New public package method: `pytsite.content.create()`
    - `pytsite. content.model.Content` model:
        - Processing `[img]` and `[vid]` body tags.
        - New properties: `title`, `description`, `body`, `url`, `tags`, `images`, `links`, `author`, `section`, 
          `starred`.
        - New events `content.entity.pre_save`, `content.entity.save`.
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
- Non-working JS for `core.widget.select.DateTime()`

## 0.1.0 (2015-07-01)
First release.

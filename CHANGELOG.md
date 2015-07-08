# PytSite Changelog

## Unreleased (2015-07-15)
### Added
- Plugins: `oauth`, `twitter`, `poster`.
- Some english and ukrainian translations.
- `stage` argument in `odm_ui.UIMixin.setup_m_form()` hook.
- `args` argument in `core.odm.Model.t()`
- Events in ODM model: `odm.entity.pre_save`, `odm.entity.save` 
- Events in Content ODM model: `content.entity.pre_save`, `content.entity.save`
- Properties in Content ODM model: `title`, `description`, `body`, `url`, `tags`, `images`
- Properties in Taxonomy ODM model: `title`, `alias`, `language`, `weight`, `order` 
- `stage` argument in `pytsite.odm_ui.UIMixin.setup_m_form()` hook.
- `args` argument in `pytsite.core.odm.Model.t()`.
- Now possible to specify package name without 'pytsite.' prefix in `core.lang.t()`, `core.router.endpoint_url`,
  `core.tpl.render()` and `core.assetman.add()`
- Widget: 'core.widget.input.StringList'
- Functions `core.util.list_cleanup()`, `core.util.dict_cleanup()`.

### Changed
- Config parameter changed `auth.auto_signup` -> `auth.allow_signup`
- `admin` templates improvements.

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

## 0.1.0 (2015-07-01)
First release.

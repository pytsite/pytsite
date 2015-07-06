# PytSite Changelog

## Unreleased (2015-07-15)
### Added
- New plugins: `oauth`, `twitter`, `poster`.
- Some english translations.
- New `stage` argument in `pytsite.odm_ui.UIMixin.setup_m_form()` hook.
- New `args` argument in `pytsite.core.odm.Model.t()`.
- Now possible to specify package name without 'pytsite.' prefix in `core.lang.t()` and `core.router.endpoint_url`.


### Changed
- Config parameter changed `auth.auto_signup` -> `auth.allow_signup`
- `admin` templates improvements.

### Fixed
- Empty configuration files read error.
- Incorrect usage of 'server_name' configuration value in `pytsite.core.router`.
- Check for app assets directory existence during `lang:build` console command.
- Exceptions handling during `odm_ui`'s form submit.
- Router's `current_url` incorrect behaviour in some situations.
- Incorrect entity caption field get in `odm_ui.widget.ODMSelect`
- Incorrect method call in `pytsite.admin@tpl/header.jinja2`

## 0.1.0 (2015-07-01)
First release.

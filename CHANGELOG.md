# PytSite Changelog

## Unreleased (2015-07-15)
### Added
- oAuth plugin.
- Twitter plugin.
- Poster plugin.
- Some english translations.
- New `stage` argument in `odm_ui.UIMixin.setup_m_form()` hook.
- New `args` argument in `core.odm.Model.t()`
- New events in ODM model: `odm.entity.pre_save`, `odm.entity.save` 
- New events in Content ODM model: `content.entity.pre_save`, `content.entity.save`
- New properties in Content ODM model: `title`, `description`, `body`, `url`, `tags` 
- New properties in Taxonomy ODM model: `title`, `alias`, `language`, `weight`, `order` 

### Fixed
- Empty configuration files read error.
- Incorrect usage of 'server_name' configuration value in `pytsite.core.router`.
- Check for app assets directory existence during `lang:build` console command.
- Exceptions handling during `odm_ui`'s form submit.
- Router's `current_url` incorrect behaviour in some situations.
- Incorrect entity caption field get in `odm_ui.widget.ODMSelect`

## 0.1.0 (2015-07-01)
First release.

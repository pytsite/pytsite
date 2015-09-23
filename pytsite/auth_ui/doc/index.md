# auth_ui
Implements UI for the `auth` module.

## Configuration parameters

### auth_ui.tpl.profile_view
Template's name to use by endpoint `pytsite.auth_ui.ep.profile_view`.

Type: string

Default: `'pytsite.auth_ui@profile_view'`

### auth_ui.tpl.profile_edit
Template's name to use by endpoint `pytsite.auth_ui.ep.profile_view`.

Type: string

Default: `'pytsite.auth_ui@profile_edit'`

### auth_ui.model.user
Class name to use as UserUI implementation.

Type: string

Default: `'pytsite.auth_ui._model.UserUI'`

### auth_ui.model.role
Class name to use as RoleUI implementation.

Type: string

Default: `'pytsite.auth_ui._model.RoleUI'`

### auth_ui.model.role


## Models

### pytsite.auth_ui.model.UserUI
Extends [`pytsite.auth.model.User`](../auth/doc/index.md).

#### Properties
- `profile_is_public`: `bool` 
- `profile_view_url`: `str`
- `profile_edit_url`: `str`

### pytsite.auth_ui.model.RoleUI
Extends `pytsite.auth.model.Role`.

## Widgets

### pytsite.auth_ui.widget.Follow
Extends `pytsite.widget.Base`.

### pytsite.auth_ui.widget.Profile
Extends `pytsite.widget.Base`.

### pytsite.auth_ui.widget.UserSelect
Extends `pytsite.widget.Base`.

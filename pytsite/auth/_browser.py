"""
"""
from pytsite import widget as _widget, lang as _lang, http_api as _http_api, html as _html, router as _router, \
    permission as _permission
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Browser(_widget.misc.BootstrapTable):
    def __init__(self, uid: str = 'pytsite-auth-admin-browser', **kwargs):
        super().__init__(uid, **kwargs)

        self._entity_type = kwargs.get('entity_type')
        if not self._entity_type:
            raise RuntimeError('Entity type must be specified.')

        self.assets.append('pytsite.auth@js/widget/browser.js')
        self._data_url = _http_api.url('pytsite.auth@admin_browser_rows', entity_type=self._entity_type)

        # Data fields
        if self._entity_type == 'user':
            self._data_fields = [
                ('login', _lang.t('pytsite.auth@login')),
                ('full_name', _lang.t('pytsite.auth@full_name')),
                ('roles', _lang.t('pytsite.auth@roles')),
                ('status', _lang.t('pytsite.auth@status')),
                ('profile_is_public', _lang.t('pytsite.auth@profile_is_public')),
                ('is_online', _lang.t('pytsite.auth@is_online')),
                ('created', _lang.t('pytsite.auth@created')),
                ('last_activity', _lang.t('pytsite.auth@last_activity')),
                ('actions', _lang.t('pytsite.auth@actions')),
            ]
        elif self._entity_type == 'role':
            self._data_fields = [
                ('name', _lang.t('pytsite.auth@name')),
                ('description', _lang.t('pytsite.auth@description')),
                ('permissions', _lang.t('pytsite.auth@permissions')),
                ('actions', _lang.t('pytsite.auth@actions')),
            ]

        c_user = _api.current_user()

        # Toolbar's 'Add' button
        if c_user.has_permission('pytsite.auth.create.' + self._entity_type):
            btn_url = _router.ep_url('pytsite.auth@admin_modify', {
                'entity_type': self._entity_type,
                'uid': 0,
                '__redirect': _router.ep_url('pytsite.auth@admin_browse', {'entity_type': self._entity_type}),
            })
            btn = _html.A(href=btn_url, cls='btn btn-default')
            btn.append(_html.I(cls='fa fa-fw fa-plus'))
            self._toolbar.append(btn)

        # Toolbar's 'Delete' button
        if c_user.has_permission('pytsite.auth.delete.' + self._entity_type):
            btn_url = _router.ep_url('pytsite.auth@admin_delete', {'entity_type': self._entity_type})
            btn = _html.A(href=btn_url, cls='btn btn-danger mass-action-button hidden')
            btn.append(_html.I(cls='fa fa-fw fa-remove'))
            self._toolbar.append(btn)

    def get_rows(self, offset: int = 0, limit: int = 0, sort_field: str = None, sort_order: str = None,
                 search: str = None) -> list:
        """Get browser rows.
        """
        total = 0
        rows = []

        sort_order = 1 if sort_order == 'asc' else -1

        if self._entity_type == 'user':
            for u in _api.get_users(sort_field=sort_field, sort_order=sort_order, limit=limit, skip=offset):
                yes = _lang.t('pytsite.auth@word_yes')

                login = '<a href="' + u.profile_view_url + '">' + u.login + '</a>'

                roles = ''
                for role in sorted(u.roles, key=lambda role: role.name):
                    cls = 'label label-default'
                    if role.name == 'admin':
                        cls += ' label-danger'
                    roles += str(_html.Span(_lang.t(role.description), cls=cls)) + ' '

                status_cls = 'info' if u.status == 'active' else 'default'
                status_word = _lang.t('pytsite.auth@status_' + u.status)
                status = '<span class="label label-{}">{}</span>'.format(status_cls, status_word)

                p_is_public = '<span class="label label-info">{}</span>'.format(yes) if u.profile_is_public else '',
                is_online = '<span class="label label-success">{}</span>'.format(yes) if u.is_online else ''

                total = _api.count_users()

                rows.append({
                    'login': login,
                    'full_name': u.full_name,
                    'roles': roles,
                    'status': status,
                    'profile_is_public': p_is_public,
                    'is_online': is_online,
                    'created': _lang.pretty_date_time(u.created),
                    'last_activity': _lang.pretty_date_time(u.last_activity),
                    'actions': self._get_actions_buttons(u),
                })

        elif self._entity_type == 'role':
            for r in _api.get_roles(sort_field=sort_field, sort_order=sort_order, limit=limit, skip=offset):
                if r.name == 'admin':
                    continue

                perms = []
                for perm_name in r.permissions:
                    perm = _permission.get_permission(perm_name)
                    cls = 'label label-default permission-' + perm[0]
                    if perm[0] == 'admin':
                        cls += ' label-danger'
                    perms.append(str(_html.Span(_lang.t(perm[1]), cls=cls)))

                rows.append({
                    'name': r.name,
                    'description': _lang.t(r.description),
                    'permissions': ' '.join(perms),
                    'actions': self._get_actions_buttons(r),
                })

        return {
            'total': total,
            'rows': rows,
        }

    def _get_actions_buttons(self, entity) -> str:
        r = ''
        c_user = _api.current_user()

        wrap = _html.Div(cls='entity-actions', data_entity_id=entity.uid, child_sep='&nbsp;')

        if c_user.has_permission('pytsite.auth.modify.' + self._entity_type):
            btn_url = _router.ep_url('pytsite.auth@admin_modify', {
                'entity_type': self._entity_type,
                'uid': entity.uid,
                '__redirect': _router.ep_url('pytsite.auth@admin_browse', {'entity_type': self._entity_type}),
            })
            btn = _html.A(href=btn_url, cls='btn btn-default btn-xs')
            btn.append(_html.I(cls='fa fa-fw fa-edit'))
            wrap.append(btn)

        if c_user.has_permission('pytsite.auth.delete.' + self._entity_type):
            btn_url = _router.ep_url('pytsite.auth@admin_delete', {
                'entity_type': self._entity_type,
                'ids': entity.uid,
                '__redirect': _router.ep_url('pytsite.auth@admin_browse', {'entity_type': self._entity_type}),
            })
            btn = _html.A(href=btn_url, cls='btn btn-danger btn-xs')
            btn.append(_html.I(cls='fa fa-fw fa-remove'))
            wrap.append(btn)

        return wrap.render()

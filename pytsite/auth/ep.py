"""Pytsite Auth Endpoints.
"""
from typing import List as _List, Union as _Union
from werkzeug.utils import escape as _escape
from pytsite import lang as _lang, http as _http, metatag as _metatag, tpl as _tpl, assetman as _assetman, \
    router as _router, logger as _logger, admin as _admin, html as _html, form as _form, widget as _widget
from . import _api, _error, _model, _widget as _auth_widget, _browser

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _EntitiesDeleteForm(_form.Form):
    def _setup_form(self, **kwargs):
        """Hook.
        """
        self._entity_type = kwargs.get('entity_type')
        self._ids = kwargs.get('ids')

        if isinstance(self._ids, str):
            self._ids = self._ids.split(',')

        if not isinstance(self._ids, list):
            raise RuntimeError('List expected.')

        self._action = _router.ep_url('pytsite.auth@admin_delete_submit', {
            'entity_type': self._entity_type
        })

    def _setup_widgets(self):
        """Hook.
        """
        submit = self.get_widget('action-submit')
        submit.color = 'danger'
        submit.icon = 'remove'
        submit.value = _lang.t('pytsite.auth@delete')

        wrap = _html.TagLessElement()
        ol = _html.Ol()
        wrap.append(ol)
        for entity in _get_entities(self._entity_type, self._ids):
            t = ''
            if self._entity_type == 'user':
                t = entity.login
            elif self._entity_type == 'role':
                t = entity.name

            ol.append(_html.Li(t))
            wrap.append(_html.Input(type='hidden', name='ids', value=entity.uid))

        self.add_widget(_widget.static.HTML('entities', em=wrap))


def sign_in(args: dict, inp: dict) -> str:
    """Page with login form.
    """
    # Redirect user if it already authorized
    if not _api.current_user().is_anonymous:
        redirect_url = _router.base_url()
        if 'redirect' in inp:
            redirect_url = _router.url(inp['redirect'])
        return _http.response.Redirect(redirect_url)

    _assetman.add('pytsite.auth@css/common.css')
    _metatag.t_set('title', _lang.t('pytsite.auth@authentication'))

    try:
        return _tpl.render('pytsite.auth@sign-in', {
            'driver': args['driver'],
            'form': _api.get_sign_in_form(args.get('driver')),
        })
    except _error.DriverNotRegistered:
        raise _http.error.NotFound()


def sign_in_submit(args: dict, inp: dict) -> _http.response.Redirect:
    """Process login form submit.
    """
    for i in ('__form_steps', '__form_step'):
        if i in inp:
            del inp[i]

    driver = args.pop('driver')
    redirect = inp.pop('__redirect', _router.base_url())

    try:
        _api.sign_in(driver, inp)
        return _http.response.Redirect(redirect)

    except _error.AuthenticationError:
        _router.session().add_error(_lang.t('pytsite.auth@authentication_error'))
        return _http.response.Redirect(_router.ep_url('pytsite.auth@sign_in', args={
            'driver': driver,
            '__redirect': redirect,
        }))

    except Exception as e:
        _logger.error(str(e))
        _router.session().add_error(str(e))
        return _http.response.Redirect(_router.ep_url('pytsite.auth@sign_in', args={
            'driver': driver,
            '__redirect': redirect,
        }))


def sign_out(args: dict, inp: dict) -> _http.response.Redirect:
    """Logout endpoint.
    """
    _api.sign_out(_api.current_user())

    return _http.response.Redirect(inp.get('__redirect', _router.base_url()))


def profile_view(args: dict, inp: dict) -> str:
    """Profile view endpoint.
    """
    try:
        profile_owner = _api.get_user(nickname=args.get('nickname'))  # type: _model.AbstractUser
    except _error.UserNotExist:
        raise _http.error.NotFound()

    c_user = _api.current_user()

    if _tpl.tpl_exists('app@auth/profile-view'):
        tpl_name = 'app@auth/profile-view'
    else:
        tpl_name = 'pytsite.auth@profile-view'

    # Non-public profiles cannot be viewed
    if not profile_owner.profile_is_public and c_user.login != profile_owner.login and not not c_user.is_admin:
        raise _http.error.NotFound()

    # Page title
    _metatag.t_set('title', profile_owner.full_name)

    # Widgets
    profile_widget = _auth_widget.Profile('auth-ui-profile-widget', user=profile_owner)

    # Give control of the response to an alternate endpoint
    if _router.is_ep_callable('$theme@auth_profile_view'):
        args.update({
            'tpl': tpl_name,
            'user': profile_owner,
            'profile_widget': profile_widget,
        })

        return _router.call_ep('$theme@auth_profile_view', args, inp)

    # Default response
    return _tpl.render(tpl_name, {
        'user': profile_owner,
        'profile_widget': profile_widget,
    })


def profile_edit(args: dict, inp: dict) -> str:
    """Profile edit endpoint.
    """
    # Check if the profile owner is exists
    profile_owner = _api.get_user(nickname=args.get('nickname'))
    if not profile_owner:
        raise _http.error.NotFound()

    tpl_name = 'pytsite.auth@profile-edit'

    frm = profile_owner.get_profile_edit_form()
    frm.title = None
    frm.redirect = profile_owner.profile_view_url

    _metatag.t_set('title', _lang.t('pytsite.auth@profile_edit'))

    # Give control of the response to an alternate endpoint
    if _router.is_ep_callable('$theme@auth_profile_edit'):
        args.update({
            'tpl': tpl_name,
            'user': profile_owner,
            'frm': frm,
        })
        return _router.call_ep('$theme@auth_profile_edit', args, inp)

    # Default response
    return _tpl.render(tpl_name, {'frm': frm})


def f_authorize(args: dict, inp: dict) -> _http.response.Redirect:
    """Authorization filter.
    """
    user = _api.current_user()

    # If user already authenticated, check its permissions
    if not user.is_anonymous:
        # Checking permissions if this is necessary
        req_perms_str = args.get('perms', '')
        if req_perms_str:
            for perm in req_perms_str.split(','):
                if not user.has_permission(perm.strip()):
                    raise _http.error.Forbidden()

        # All permissions has been checked successfully, simply do nothing
        return

    # Redirecting to the authorization endpoint
    inp['__redirect'] = _escape(_router.current_url(True))
    inp['driver'] = _api.get_auth_driver().name

    if '__form_location' in inp:
        del inp['__form_location']

    return _http.response.Redirect(_router.ep_url('pytsite.auth@sign_in', inp))


def admin_browse(args: dict, inp: dict) -> str:
    _metatag.t_set('title', _lang.t('pytsite.auth@browser_title_' + args['entity_type']))

    return _admin.render(_tpl.render('pytsite.auth@admin-browser', {
        'table': _browser.Browser('auth-admin-browser', entity_type=args['entity_type']).render()
    }))


def admin_modify(args: dict, inp: dict) -> str:
    entity_type = args['entity_type']

    c_user = _api.current_user()
    if not c_user.has_permission('pytsite.auth.delete.' + entity_type):
        raise _http.error.Unauthorized()

    entity = None
    if args['uid'] == '0':
        title = _lang.t('pytsite.auth@form_title_create_' + entity_type)
    else:
        title = _lang.t('pytsite.auth@form_title_modify_' + entity_type)
    if entity_type == 'user':
        if args['uid'] != '0':
            entity = _api.get_user(uid=args['uid'])
        frm = _api.get_user_modify_form(entity)
        _metatag.t_set('title', title)
        return _admin.render_form(frm)
    elif entity_type == 'role':
        if args['uid'] != '0':
            entity = _api.get_role(uid=args['uid'])
        return _admin.render_form(_api.get_role_modify_form(entity))
    else:
        raise _http.error.InternalServerError('Wrong entity type.')


def admin_delete(args: dict, inp: dict) -> str:
    entity_type = args['entity_type']
    ids = inp['ids']

    c_user = _api.current_user()
    if not c_user.has_permission('pytsite.auth.delete.' + entity_type):
        raise _http.error.Forbidden()

    _metatag.t_set('title', _lang.t('pytsite.auth@form_title_delete_' + entity_type))

    return _admin.render_form(_EntitiesDeleteForm('pytsite-auth-admin-delete', entity_type=entity_type, ids=ids))


def admin_delete_submit(args: dict, inp: dict) -> str:
    entity_type = args['entity_type']

    c_user = _api.current_user()
    if not c_user.has_permission('pytsite.auth.delete.' + entity_type):
        raise _http.error.Forbidden()

    try:
        for entity in _get_entities(entity_type, inp['ids']):
            # Admin users cannot delete themselves
            if entity == c_user:
                raise _error.UserDeletionForbidden(_lang.t('pytsite.auth@you_cannot_delete_yourself'))
            _api.delete_entity(entity)
    except (_error.UserDeletionForbidden, _error.RoleDeletionForbidden) as e:
        _router.session().add_error(str(e))

    return _http.response.Redirect(_router.ep_url('pytsite.auth@admin_browse', {'entity_type': entity_type}))


def _get_entities(entity_type: str, ids: _Union[str, list]) -> _List[_Union[_model.AbstractUser, _model.AbstractRole]]:
    r = []

    if isinstance(ids, str):
        ids = [ids]

    for uid in ids:
        if entity_type == 'user':
            r.append(_api.get_user(uid=uid))
        elif entity_type == 'role':
            r.append(_api.get_role(uid=uid))
        else:
            raise _http.error.InternalServerError('Wrong entity type.')

    return r

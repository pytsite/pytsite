"""Pytsite Auth Endpoints.
"""
from typing import Union as _Union, Optional as _Optional
from werkzeug.utils import escape as _escape
from pytsite import lang as _lang, http as _http, metatag as _metatag, tpl as _tpl, assetman as _assetman, \
    router as _router, logger as _logger, routing as _routing
from . import _api, _error, _widget as _auth_widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class SignIn(_routing.Controller):
    def exec(self) -> _Union[str, _http.response.Redirect]:
        # Redirect user if it already authenticated
        if not _api.get_current_user().is_anonymous:
            return self.redirect(_router.request().inp.get('__redirect', _router.base_url()))

        _assetman.preload('pytsite.auth@css/common.css')
        _metatag.t_set('title', _lang.t('pytsite.auth@authentication'))

        try:
            driver = self.arg('driver')
            frm = _api.get_sign_in_form(driver, nocache=True)
            args = {'driver': driver, 'form': frm}

            try:
                return _tpl.render('$theme@auth/sign-in', args)
            except _tpl.error.TemplateNotFound:
                return _tpl.render('pytsite.auth@sign-in', args)

        except _error.DriverNotRegistered:
            raise self.not_found()


class SignInSubmit(_routing.Controller):
    def exec(self):
        inp = _router.request().inp

        for i in ('__form_steps', '__form_step'):
            if i in inp:
                del inp[i]

        driver = self.arg('driver')
        redirect = inp.pop('__redirect', _router.base_url())

        try:
            _api.sign_in(driver, inp)

            return self.redirect(redirect)

        except _error.AuthenticationError:
            _router.session().add_error_message(_lang.t('pytsite.auth@authentication_error'))

            return self.redirect(_router.rule_url('pytsite.auth@sign_in', rule_args={
                'driver': driver,
                '__redirect': redirect,
            }))

        except Exception as e:
            _logger.error(str(e), exc_info=e)
            _router.session().add_error_message(str(e))
            return self.redirect(_router.rule_url('pytsite.auth@sign_in', rule_args={
                'driver': driver,
                '__redirect': redirect,
            }))


class SignOut(_routing.Controller):
    def exec(self):
        _api.sign_out(_api.get_current_user())

        return self.redirect(_router.request().inp.get('__redirect', _router.base_url()))


class ProfileView(_routing.Controller):
    def exec(self) -> str:
        """Profile view endpoint.
        """
        try:
            profile_owner = _api.get_user(nickname=self.arg('nickname'))
        except _error.UserNotExist:
            raise self.not_found()

        c_user = _api.get_current_user()

        if _tpl.tpl_exists('$theme@auth/profile-view'):
            tpl_name = '$theme@auth/profile-view'
        else:
            tpl_name = 'pytsite.auth@profile-view'

        # Non-public profiles cannot be viewed
        if not profile_owner.profile_is_public and c_user.login != profile_owner.login and not c_user.is_admin:
            raise _http.error.NotFound()

        # Page title
        _metatag.t_set('title', profile_owner.full_name)

        # Widgets
        profile_widget = _auth_widget.Profile('auth-ui-profile-widget', user=profile_owner)

        self.args.update({
            'profile_is_editable': c_user == profile_owner or c_user.is_admin,
            'user': profile_owner,
            'profile_widget': profile_widget,
        })

        # Give control of the response to an alternate endpoint
        if _router.has_rule('$theme@auth_profile_view'):
            self.args.update({
                'tpl': tpl_name,
            })

            return _router.call('$theme@auth_profile_view', **self.args)

        # Preload CSS
        _assetman.preload('pytsite.auth@css/pytsite-auth-widget-profile.css')

        # Default response
        return _tpl.render(tpl_name, self.args)


class ProfileEdit(_routing.Controller):
    def exec(self) -> str:
        """Profile edit endpoint.
        """
        # Check if the profile owner is exists
        profile_owner = _api.get_user(nickname=self.arg('nickname'))
        if not profile_owner:
            raise _http.error.NotFound()

        tpl_name = 'pytsite.auth@profile-edit'

        frm = _api.get_user_modify_form(profile_owner)
        frm.title = _lang.t('pytsite.auth@profile_edit')
        frm.redirect = profile_owner.profile_view_url

        _metatag.t_set('title', frm.title)

        # Give control of the response to an alternate endpoint
        if _router.has_rule('$theme@auth_profile_edit'):
            self.args.update({
                'tpl': tpl_name,
                'user': profile_owner,
                'frm': frm,
            })
            return _router.call('$theme@auth_profile_edit', **self.args)

        # Default response
        return _tpl.render(tpl_name, {'frm': frm})


class FilterAuthorize(_routing.Controller):
    """Authorization filter
    """

    def exec(self) -> _Optional[_http.response.Redirect]:
        user = _api.get_current_user()

        # If user already authenticated, check its permissions
        if not user.is_anonymous:
            # Checking permissions if this is necessary
            req_perms_str = self.arg('perms', '')
            if req_perms_str:
                for perm in req_perms_str.split(','):
                    if not user.has_permission(perm.strip()):
                        raise _http.error.Forbidden()

            # All permissions has been checked successfully, simply do nothing
            return

        # Redirecting to the authorization endpoint
        inp = _router.request().inp
        inp['__redirect'] = _escape(_router.current_url(True))
        inp['driver'] = _api.get_auth_driver().name

        if '__form_location' in inp:
            del inp['__form_location']

        return _http.response.Redirect(_router.rule_url('pytsite.auth@sign_in', inp))

"""Pytsite Auth Controllers
"""
from typing import Union as _Union, Optional as _Optional
from werkzeug.utils import escape as _escape
from pytsite import lang as _lang, http as _http, metatag as _metatag, tpl as _tpl, assetman as _assetman, \
    router as _router, logger as _logger, routing as _routing, auth as _auth
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class SignIn(_routing.Controller):
    def exec(self) -> _Union[str, _http.response.Redirect]:
        # Redirect user if it already authenticated
        if not _auth.get_current_user().is_anonymous:
            return self.redirect(_router.request().inp.get('__redirect', _router.base_url()))

        _assetman.preload('pytsite.auth_web@css/pytsite-auth-web-sign-in.css')
        _metatag.t_set('title', _lang.t('pytsite.auth_web@authentication'))

        try:
            driver = self.arg('driver')
            frm = _api.sign_in_form(driver, nocache=True)
            args = {'driver': driver, 'form': frm}

            try:
                return _tpl.render('$theme@auth_web/sign-in', args)
            except _tpl.error.TemplateNotFound:
                return _tpl.render('pytsite.auth_web@sign-in', args)

        except _auth.error.DriverNotRegistered:
            raise self.not_found()


class SignInSubmit(_routing.Controller):
    def exec(self):
        inp = _router.request().inp

        for i in ('__form_steps', '__form_step'):
            if i in inp:
                del inp[i]

        driver = self.arg('driver')

        redirect = inp.pop('__redirect', _router.base_url())
        if isinstance(redirect, list):
            redirect = redirect.pop()

        try:
            _auth.sign_in(driver, inp)

            return self.redirect(redirect)

        except _auth.error.AuthenticationError:
            _router.session().add_error_message(_lang.t('pytsite.auth_web@authentication_error'))

            return self.redirect(_router.rule_url('pytsite.auth_web@sign_in', rule_args={
                'driver': driver,
                '__redirect': redirect,
            }))

        except Exception as e:
            _logger.error(str(e), exc_info=e)
            _router.session().add_error_message(str(e))
            return self.redirect(_router.rule_url('pytsite.auth_web@sign_in', rule_args={
                'driver': driver,
                '__redirect': redirect,
            }))


class SignOut(_routing.Controller):
    def exec(self):
        _auth.sign_out(_auth.get_current_user())

        return self.redirect(_router.request().inp.get('__redirect', _router.base_url()))


class FilterAuthorize(_routing.Controller):
    """Authorization filter
    """

    def exec(self) -> _Optional[_http.response.Redirect]:
        user = _auth.get_current_user()

        # If user already authenticated, check its permissions
        if not user.is_anonymous:
            # Checking permissions if this is necessary
            req_perms_str = self.arg('perms', '')
            if req_perms_str:
                for perm in req_perms_str.split(','):
                    if not user.has_permission(perm.strip()):
                        raise self.forbidden()

            # All permissions has been checked successfully, simply do nothing
            return

        # Redirecting to the authorization endpoint
        inp = _router.request().inp.copy()
        inp['__redirect'] = _escape(_router.current_url(True))
        inp['driver'] = _auth.get_auth_driver().name

        if '__form_location' in inp:
            del inp['__form_location']

        return self.redirect(_router.rule_url('pytsite.auth_web@sign_in', inp))

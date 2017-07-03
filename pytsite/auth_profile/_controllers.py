"""PytSite Auth Profile Controllers
"""
from pytsite import routing as _routing, auth as _auth, auth_web as _auth_web, metatag as _metatag, \
    router as _router, tpl as _tpl, lang as _lang
from . import _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ProfileView(_routing.Controller):
    def exec(self) -> str:
        """Profile view endpoint.
        """
        try:
            profile_owner = _auth.get_user(nickname=self.arg('nickname'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        c_user = _auth.get_current_user()

        if _tpl.tpl_exists('$theme@auth/profile-view'):
            tpl_name = '$theme@auth/profile-view'
        else:
            tpl_name = 'pytsite.auth_profile@profile-view'

        # Non-public profiles cannot be viewed
        if not profile_owner.profile_is_public and c_user.login != profile_owner.login and not c_user.is_admin:
            raise self.not_found()

        # Page title
        _metatag.t_set('title', profile_owner.full_name)

        # Widgets
        profile_widget = _widget.Profile('auth-ui-profile-widget', user=profile_owner)

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

            return _router.call('$theme@auth_profile_view', self.args)

        # Default response
        return _tpl.render(tpl_name, self.args)


class ProfileEdit(_routing.Controller):
    def exec(self) -> str:
        """Profile edit endpoint.
        """
        # Check if the profile owner is exists
        profile_owner = _auth.get_user(nickname=self.arg('nickname'))
        if not profile_owner:
            raise self.not_found()

        tpl_name = 'pytsite.auth_profile@profile-edit'

        frm = _auth_web.user_modify_form(profile_owner)
        frm.title = _lang.t('pytsite.auth_profile@profile_edit')
        frm.redirect = profile_owner.profile_view_url

        _metatag.t_set('title', frm.title)

        # Give control of the response to an alternate endpoint
        if _router.has_rule('$theme@auth_profile_edit'):
            self.args.update({
                'tpl': tpl_name,
                'user': profile_owner,
                'frm': frm,
            })
            return _router.call('$theme@auth_profile_edit', self.args)

        # Default response
        return _tpl.render(tpl_name, {'frm': frm})

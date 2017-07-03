"""PytSite Theme HTTP API
"""
from os import close as _file_close
from werkzeug.datastructures import FileStorage as _FileStorage
from pytsite import auth as _auth, routing as _routing, lang as _lang, http as _http, util as _util
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Install(_routing.Controller):
    def exec(self):
        if not _auth.get_current_user().has_permission('pytsite.theme.manage'):
            raise self.forbidden()

        file = self.args.pop('file')  # type: _FileStorage

        if not file:
            # It is important to return all input arguments back (except file, of course)
            self.args.update({'error': _lang.t('pytsite.theme@theme_file_not_provided')})
            raise self.server_error(response=_http.response.JSON(dict(self.args)))

        if file.mimetype != 'application/zip':
            # It is important to return all input arguments back (except file, of course)
            self.args.update({'error': _lang.t('pytsite.theme@only_zip_files_supported')})
            raise self.server_error(response=_http.response.JSON(dict(self.args)))

        # Save received file to temporary directory
        tmp_file_id, tmp_file_path = _util.mk_tmp_file('.zip')
        file.save(tmp_file_path)
        _file_close(tmp_file_id)

        # Install theme from ZIP file
        try:
            _api.install(tmp_file_path)
        except Exception as e:
            self.args.update({'error': _lang.t('pytsite.theme@theme_installation_failed', {'msg': str(e)})})
            raise self.server_error(response=_http.response.JSON(dict(self.args)))

        # It is important to return all input arguments back (except file, of course)
        self.args.update({
            'message': _lang.t('pytsite.theme@wait_theme_being_installed'),
            'eval': 'setTimeout(function() {window.location.reload()}, 3000)',
        })

        return self.args


class Switch(_routing.Controller):
    def exec(self):
        if not _auth.get_current_user().has_permission('pytsite.theme.manage'):
            raise self.forbidden()

        _api.switch(self.arg('package_name'))

        return {'status': True}


class Uninstall(_routing.Controller):
    def exec(self):
        if not _auth.get_current_user().has_permission('pytsite.theme.manage'):
            raise self.forbidden()

        _api.uninstall(self.arg('package_name'))

        return {'status': True}

"""PytSite Form HTTP API Controllers
"""
from pytsite import routing as _routing
from . import _error, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class GetWidgets(_routing.Controller):
    """Get widgets of the form for particular step

    POST method is used here due to large request size in some cases.
    """

    def exec(self) -> list:
        self.args['__form_data_uid'] = self.args['uid']

        frm = _api.dispense(self.args)

        r = []
        for w in frm.get_widgets():
            # Return only top widgets, because they render their children's HTML code by themselves
            if not w.parent:
                r.append(w.render())

        return r


class PostValidate(_routing.Controller):
    """Default form's AJAX validator
    """

    def exec(self) -> dict:
        try:
            self.args['__form_data_uid'] = self.args['uid']
            _api.dispense(self.args, 'validation').validate()
            return {'status': True}

        except _error.ValidationError as e:
            return {'status': False, 'messages': e.errors}

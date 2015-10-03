"""PytSite Contact Endpoints.
"""
from pytsite import lang as _lang, reg as _reg, mail as _mail, tpl as _tpl

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def submit(args: dict, inp: dict) -> dict:
    """Precess form submission.
    """
    for field in ('contact_name', 'contact_email', 'contact_message'):
        if field not in inp:
            raise ValueError("'{}' is not in input parameters".format(field))

    recipients = _reg.get('contact.recipients', 'info@{}'.format(_reg.get('server.name')))
    if isinstance(recipients, str):
        recipients = (recipients,)

    for rcp in recipients:
        _mail.Message(
            rcp,
            _lang.t('pytsite.contact@message_from_site', {'name': _lang.t('app_name')}),
            _tpl.render('pytsite.contact@mail', inp),
            reply_to=inp.get('contact_email'),
        ).send()

    return _lang.t('pytsite.contact@message_successfully_sent')

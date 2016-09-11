"""PytSite Contact Endpoints.
"""
from pytsite import lang as _lang, reg as _reg, mail as _mail, tpl as _tpl, router as _router, settings as _settings

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post_submit(inp: dict) -> dict:
    """Precess form submission.
    """
    for field in ('contact_name', 'contact_email', 'contact_message'):
        if field not in inp:
            raise ValueError("'{}' is not in input parameters".format(field))

    recipients = _settings.get('contact_form.recipients', 'info@{}'.format(_router.server_name()))
    if isinstance(recipients, str):
        recipients = (recipients,)

    for rcp in recipients:
        _mail.Message(
            rcp,
            _lang.t('pytsite.contact_form@message_from_site', {'name': _lang.t('app_name')}),
            _tpl.render(_reg.get('contact_form.tpl', 'pytsite.contact_form@mail'), inp),
            reply_to=inp.get('contact_email'),
        ).send()

    return {'message': _lang.t('pytsite.contact_form@message_successfully_sent')}

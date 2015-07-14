"""Pytsite Mail Subsystem.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from os import path as _path
from mimetypes import guess_type as _guess_mime_type
from smtplib import SMTP as _SMTP
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.image import MIMEImage as _MIMEImage
from email.mime.text import MIMEText as _MIMEText


class Message(_MIMEMultipart):
    def __init__(self, from_addr: str, to_addrs, subject: str, body: str=''):
        super().__init__()

        self._from_addr = from_addr
        self._subject = subject

        if isinstance(to_addrs, str):
            to_addrs = (to_addrs,)
        elif not isinstance(to_addrs, tuple):
            raise ValueError('String ot tuple expected as recipient(s) address.')

        self._to_addrs = to_addrs

        self['From'] = self._from_addr
        self['To'] = ', '.join(self._to_addrs)
        self['Subject'] = self._subject

        super().attach(_MIMEText(body, 'html', 'utf-8'))

    @property
    def from_addr(self) -> str:
        return self._from_addr

    @property
    def to_addrs(self) -> tuple:
        return self._to_addrs

    def attach(self, path: str):
        ctype, encoding = _guess_mime_type(path)

        if ctype:
            ctype = ctype.split('/')
            if ctype[0] == 'image':
                with open(path, 'rb') as f:
                    attachment = _MIMEImage(f.read(), _subtype=ctype[1])
                    attachment.add_header('Content-Disposition', 'attachment', filename=_path.basename(path))
                    super().attach(attachment)
            else:
                raise Exception('Unsupported attachment type: {}.'.format(repr(ctype)))


def send(msg: Message):
    engine = _SMTP('localhost')
    print(engine.sendmail(msg.from_addr, msg.to_addrs, str(msg)))

"""Pytsite Mail Subsystem.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path as _path
from mimetypes import guess_type as _guess_mime_type
from smtplib import SMTP as _SMTP
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.image import MIMEImage as _MIMEImage
from email.mime.text import MIMEText as _MIMEText


class Message(_MIMEMultipart):
    """Mail Message.
    """
    def __init__(self, from_addr: str, to_addrs, subject: str, body: str=''):
        """Init.
        """
        super().__init__()

        self._from_addr = None
        self._to_addrs = None
        self._subject = None
        self._body = None

        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.subject = subject
        self.body = body

        self._attachments = []

    @property
    def from_addr(self) -> str:
        return self._from_addr

    @from_addr.setter
    def from_addr(self, value: str) -> str:
        self['From'] = self._from_addr = value

    @property
    def to_addrs(self) -> tuple:
        return self._to_addrs

    @to_addrs.setter
    def to_addrs(self, value):
        """
        :param value: str|tuple
        """
        if isinstance(value, str):
            value = (value,)
        elif not isinstance(value, tuple):
            raise ValueError('String ot tuple expected as recipient(s) address.')
        self['To'] = self._to_addrs = ', '.join(value)

    @property
    def subject(self) -> str:
        return self._subject

    @subject.setter
    def subject(self, value: str):
        self['Subject'] = self._subject = value

    @property
    def body(self) -> str:
        return self._body

    @body.setter
    def body(self, value: str):
        self._body = value

    def attach(self, file_path: str):
        if not _path.isfile(file_path):
            raise Exception("'{}' is not a file.".format(file_path))

        ctype, encoding = _guess_mime_type(file_path)
        if ctype:
            ctype = ctype.split('/')
            if ctype[0] == 'image':
                with open(file_path, 'rb') as f:
                    attachment = _MIMEImage(f.read(), _subtype=ctype[1])
                    attachment.add_header('Content-Disposition', 'attachment', filename=_path.basename(file_path))
                    self._attachments.append(attachment)
            else:
                raise Exception("Unsupported MIME type '{}', file '{}'.".format(repr(ctype), file_path))
        else:
            raise Exception("Cannot guess MIME type for '{}'.".format(file_path))

    def send(self):
        """Send message.
        """
        super().attach(_MIMEText(self.body, 'html', 'utf-8'))
        for attachment in self._attachments:
            super().attach(attachment)

        engine = _SMTP('localhost')
        engine.sendmail(self._from_addr, self._to_addrs, str(self))

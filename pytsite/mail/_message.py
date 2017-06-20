"""PytSite Mail Message.
"""
import threading
from os import path as _path
from mimetypes import guess_type as _guess_mime_type
from smtplib import SMTP as _SMTP
from email.header import Header as _Header
from email.mime.multipart import MIMEMultipart as _MIMEMultipart
from email.mime.image import MIMEImage as _MIMEImage
from email.mime.text import MIMEText as _MIMEText
from pytsite import logger as _logger
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Message(_MIMEMultipart):
    """Mail Message.
    """

    def __init__(self, to_addrs, subject: str, body: str = '', from_addr: str = None, reply_to: str = None):
        """Init.
        """
        super().__init__()

        self._from_addr = self._to_addrs = self._subject = self._body = self._reply_to = None

        self.from_addr = from_addr if from_addr else _api.mail_from()
        self.to_addrs = to_addrs
        self.subject = subject
        self.body = body

        if reply_to:
            self.reply_to = reply_to

        self._attachments = []

    @property
    def from_addr(self) -> str:
        return self._from_addr

    @from_addr.setter
    def from_addr(self, value: str):
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
            raise ValueError('String or tuple expected as recipient(s) address.')
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

    @property
    def reply_to(self) -> str:
        return self._reply_to

    @reply_to.setter
    def reply_to(self, value):
        self['Reply-To'] = self._reply_to = value

    def attach(self, file_path: str):
        if not _path.isfile(file_path):
            raise RuntimeError("'{}' is not a file.".format(file_path))

        ctype, encoding = _guess_mime_type(file_path)
        if ctype:
            ctype = ctype.split('/')
            if ctype[0] == 'image':
                with open(file_path, 'rb') as f:
                    attachment = _MIMEImage(f.read(), _subtype=ctype[1])
                    attachment.add_header('Content-Disposition', 'attachment', filename=_path.basename(file_path))
                    self._attachments.append(attachment)
            else:
                raise RuntimeError("Unsupported MIME type '{}', file '{}'.".format(repr(ctype), file_path))
        else:
            raise RuntimeError("Cannot guess MIME type for '{}'.".format(file_path))

    def send(self):
        """Send message.
        """

        def do_send(msg: Message):
            try:
                engine = _SMTP('localhost')
                engine.sendmail(msg._from_addr, msg._to_addrs, str(msg))
                log_msg = "Message '{}' has been sent to {}.".format(msg.subject, msg.to_addrs)
                _logger.info(log_msg)
            except Exception as e:
                _logger.error('Unable to send message to {}. {}.'.format(msg.to_addrs, e), exc_info=e, stack_info=True)

        super().attach(_MIMEText(self.body, 'html', 'utf-8'))
        for attachment in self._attachments:
            super().attach(attachment)

        threading.Thread(target=do_send, kwargs={'msg': self}).start()
        _logger.info('Started new message send thread to {}.'.format(self.to_addrs))

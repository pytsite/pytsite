"""PytSite Database Console Commands.
"""
import subprocess as _subprocess
import shutil as _shutil
from os import path as _path
from datetime import datetime as _datetime
from pytsite import console as _console, reg as _reg, validation as _validation, maintenance as _maintenance

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Db(_console.command.Abstract):
    """Database Dump Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'db'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.lang import t

        return t('pytsite.db@db_console_command_description')

    def get_options_help(self) -> str:
        """Get help for the command.
        """
        return '--dump | --restore'

    def get_options(self) -> tuple:
        """Get command options.
        """
        return (
            ('dump', _validation.rule.Dummy()),
            ('restore', _validation.rule.Dummy())
        )

    def _dump(self):
        if _subprocess.call('which mongodump', stdout=_subprocess.DEVNULL, stderr=_subprocess.DEVNULL, shell=True) != 0:
            raise Exception('Cannot find mongodump executable.')

        _maintenance.enable()

        db_name = _reg.get('db.database')
        target_dir = _path.join(_reg.get('paths.root'), 'misc', 'dbdump')
        target_subdir = _path.join(target_dir, db_name)

        if _path.exists(target_subdir):
            ctime = _datetime.fromtimestamp(_path.getctime(target_subdir))
            target_subdir_move = '{}-{}'.format(target_subdir, ctime.strftime('%Y%m%d-%H%M%S'))
            _shutil.move(target_subdir, target_subdir_move)

        from . import _api
        config = _api.get_config()

        command = 'mongodump -h {}:{} --gzip -o {} -d {}'.format(config['host'], config['port'], target_dir, db_name)

        if config['user']:
            command += ' -u {} -p {}'.format(config['user'], config['password'])
        if config['ssl']:
            command += ' --ssl --sslAllowInvalidCertificates'

        r = _subprocess.call(command, shell=True)

        _maintenance.disable()

        return r

    def _restore(self):
        if _subprocess.call('which mongorestore', stdout=_subprocess.DEVNULL, stderr=_subprocess.DEVNULL, shell=True):
            raise Exception('Cannot find mongorestore executable.')

        _maintenance.enable()

        db_name = _reg.get('db.database')
        source_dir = _path.join(_reg.get('paths.root'), 'misc', 'dbdump', db_name)

        from . import _api
        config = _api.get_config()

        command = 'mongorestore -h {}:{} --drop --gzip --stopOnError --dir {} -d {}'.\
            format(config['host'], config['port'], source_dir, db_name)

        if config['user']:
            command += ' -u {} -p {}'.format(config['user'], config['password'])
        if config['ssl']:
            command += ' --ssl --sslAllowInvalidCertificates'

        r = _subprocess.call(command, shell=True)

        _maintenance.disable()

        return r

    def execute(self, args: tuple=(), **kwargs):
        """Execute the command.
        """
        if not kwargs:
            raise _console.error.InsufficientArguments()

        for k in kwargs:
            if k == 'dump':
                self._dump()
            if k == 'restore':
                self._restore()

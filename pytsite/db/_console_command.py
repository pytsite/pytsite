"""PytSite Database Console Commands.
"""
import subprocess as _subprocess
import shutil as _shutil
from os import path as _path
from datetime import datetime as _datetime
from pytsite import console as _console, reg as _reg, maintenance as _maintenance, events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Db(_console.Command):
    """Database Dump Command.
    """

    def __init__(self):
        super().__init__()

        self._define_argument(_console.argument.Choice('action', True, options=['dump', 'restore']))

    @property
    def name(self) -> str:
        """Get name of the command.
        """
        return 'db'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.db@db_console_command_description'

    def _dump(self):
        if _subprocess.call('which mongodump', stdout=_subprocess.DEVNULL, stderr=_subprocess.DEVNULL, shell=True) != 0:
            raise RuntimeError('Cannot find mongodump executable.')

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
            raise RuntimeError('Cannot find mongorestore executable.')

        _maintenance.enable()

        db_name = _reg.get('db.database')
        source_dir = _path.join(_reg.get('paths.root'), 'misc', 'dbdump', db_name)

        from . import _api
        config = _api.get_config()

        command = 'mongorestore -h {}:{} --drop --gzip --stopOnError --dir {} -d {}'. \
            format(config['host'], config['port'], source_dir, db_name)

        if config['user']:
            command += ' -u {} -p {}'.format(config['user'], config['password'])
        if config['ssl']:
            command += ' --ssl --sslAllowInvalidCertificates'

        r = _subprocess.call(command, shell=True)

        _events.fire('pytsite.db.restore')

        _maintenance.disable()

        return r

    def execute(self):
        """Execute the command.
        """
        action = self.get_argument_value(0)

        if action == 'dump':
            self._dump()
        if action == 'restore':
            self._restore()

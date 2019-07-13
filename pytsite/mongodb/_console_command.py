"""PytSite MongoDB Support Console Commands
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import subprocess
import shutil
from os import path
from datetime import datetime
from pytsite import console, reg, maintenance, events


class Db(console.Command):
    """Database Dump Command.
    """

    @property
    def name(self) -> str:
        """Get name of the command.
        """
        return 'db'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.mongodb@db_console_command_description'

    @staticmethod
    def _dump():
        if subprocess.call('which mongodump', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) != 0:
            raise RuntimeError('Cannot find mongodump executable.')

        maintenance.enable()

        db_name = reg.get('db.database')
        target_dir = path.join(reg.get('paths.root'), 'misc', 'dbdump')
        target_subdir = path.join(target_dir, db_name)

        if path.exists(target_subdir):
            ctime = datetime.fromtimestamp(path.getctime(target_subdir))
            target_subdir_move = '{}-{}'.format(target_subdir, ctime.strftime('%Y%m%d-%H%M%S'))
            shutil.move(target_subdir, target_subdir_move)

        from . import _api
        config = _api.get_config()

        command = 'mongodump -h {}:{} --gzip -o {} -d {}'.format(config['host'], config['port'], target_dir, db_name)

        if config['user']:
            command += ' -u {} -p {}'.format(config['user'], config['password'])
        if config['ssl']:
            command += ' --ssl --sslAllowInvalidCertificates'

        r = subprocess.call(command, shell=True)

        maintenance.disable()

        return r

    @staticmethod
    def _restore():
        if subprocess.call('which mongorestore', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True):
            raise RuntimeError('Cannot find mongorestore executable.')

        maintenance.enable()

        db_name = reg.get('db.database')
        source_dir = path.join(reg.get('paths.root'), 'misc', 'dbdump', db_name)

        from . import _api
        config = _api.get_config()

        command = 'mongorestore -h {}:{} --drop --gzip --stopOnError --dir {} -d {}'. \
            format(config['host'], config['port'], source_dir, db_name)

        if config['user']:
            command += ' -u {} -p {}'.format(config['user'], config['password'])
        if config['ssl']:
            command += ' --ssl --sslAllowInvalidCertificates'

        r = subprocess.call(command, shell=True)

        events.fire('pytsite.mongodb@restore')

        maintenance.disable()

        return r

    def exec(self):
        """Execute the command.
        """
        action = self.arg(0)

        if action == 'dump':
            self._dump()
        elif action == 'restore':
            self._restore()
        else:
            raise console.error.InvalidArgument(0, action)

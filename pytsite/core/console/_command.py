"""Console Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pickle as _pickle
import subprocess as _subprocess
import shutil as _shutil
import time as _time
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from datetime import datetime as _datetime
from os import listdir as _listdir, path as _path, unlink as _unlink, makedirs as _makedirs
from pytsite.core import reg as _reg, events as _events, logger as _logger, db as _db
from . import _error


class Abstract(_ABC):
    """Abstract command.
    """
    @_abstractmethod
    def get_name(self) -> str:
        pass

    @_abstractmethod
    def get_description(self) -> str:
        pass

    @_abstractmethod
    def execute(self, **kwargs: dict):
        pass


class Cleanup(Abstract):
    """Cleanup All Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'app:cleanup'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@cleanup_all_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        from ._functions import run_command
        run_command('cleanup:tmp', **kwargs)
        run_command('cleanup:session', **kwargs)


class CleanupTmpFiles(Abstract):
    """Cleanup Tmp Files Command.
    """
    def get_name(self) -> str:
        return 'app:cleanup:tmp'

    def get_description(self):
        from pytsite.core.lang import t
        return t('pytsite.core@cleanup_tmp_console_command_description')

    def execute(self, **kwargs: dict):
        tmp_dir = _reg.get('paths.tmp')
        for file_name in _listdir(tmp_dir):
            file_path = _path.join(tmp_dir, file_name)
            if _path.isfile(file_path):
                _unlink(file_path)


class CleanupOldSessions(Abstract):
    """Cleanup Old Session Files Command.
    """
    def get_name(self) -> str:
        return 'app:cleanup:session'

    def get_description(self):
        from pytsite.core.lang import t
        return t('pytsite.core@cleanup_session_console_command_description')

    def execute(self, **kwargs: dict):
        session_dir = _reg.get('paths.session')
        ttl = int(_reg.get('session.ttl', 21600))  # 6 hours
        for file_name in _listdir(session_dir):
            file_path = _path.join(session_dir, file_name)
            if _path.isfile(file_path) and (_time.time() - _path.getmtime(file_path)) >= ttl:
                _unlink(file_path)


class Cron(Abstract):
    """Cron command.
    """
    def get_name(self):
        """Get command name.
        """
        return 'cron:start'

    def get_description(self):
        """Get command description.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@cron_console_command_description')




class Maintenance(Abstract):
    """Maintenance Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'app:maintenance'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@maintenance_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        from pytsite.core.lang import t
        from . import _functions
        lock_path = _reg.get('paths.maintenance.lock')

        if 'enable' in kwargs:
            with open(lock_path, 'wt') as f:
                f.write(str(_datetime.now()))
            _functions.print_success(t('pytsite.core@maintenance_mode_enabled'))
        elif 'disable' in kwargs:
            _unlink(lock_path)
            _functions.print_success(t('pytsite.core@maintenance_mode_disabled'))
        else:
            _functions.print_info('Usage: app:maintenance --enable | --disable')


class Setup(Abstract):
    """Setup Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'app:setup'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@setup_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        from pytsite.core.lang import t

        lock_path = _reg.get('paths.setup.lock')
        if _path.exists(lock_path):
            raise _error.ConsoleRuntimeError(t('pytsite.core@setup_already_completed'))

        _events.fire('app.setup')

        # Writing lock file
        lock_dir = _path.dirname(lock_path)
        if not _path.isdir(lock_dir):
            _makedirs(lock_dir, 0o755, True)
        with open(lock_path, 'wt') as f:
            f.write(_datetime.now().isoformat())

        from ._functions import print_info
        print_info(t('pytsite.core@setup_has_been_completed'))


class Update(Abstract):
    """Setup Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'app:update'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@update_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        from . import _functions

        _functions.run_command('app:maintenance', enable=True)
        _events.fire('app.update')
        _functions.run_command('app:maintenance', disable=True)


class DbDump(Abstract):
    """Database Dump Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'db:dump'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@db_dump_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        if _subprocess.call('which mongodump', stdout=_subprocess.DEVNULL, stderr=_subprocess.DEVNULL, shell=True) != 0:
            raise Exception('Cannot find mongodump executable.')

        from ._functions import run_command

        run_command('app:maintenance', enable=True)

        db_name = _reg.get('db.database')
        target_dir = _path.join(_reg.get('paths.root'), 'misc', 'dbdump')
        target_subdir = _path.join(target_dir, db_name)

        if _path.exists(target_subdir):
            ctime = _datetime.fromtimestamp(_path.getctime(target_subdir))
            target_subdir_move = '{}-{}'.format(target_subdir, ctime.strftime('%Y%m%d-%H%M%S'))
            _shutil.move(target_subdir, target_subdir_move)

        config = _db.get_config()

        command = 'mongodump -h {}:{} --gzip -o {} -d {}'.format(config['host'], config['port'], target_dir, db_name)

        if config['user']:
            command += '-u {} -p {}'.format(config['user'], config['password'])
        if config['ssl']:
            command += ' --ssl --sslAllowInvalidCertificates'

        r = _subprocess.call(command, shell=True)

        run_command('app:maintenance', disable=True)

        return r


class DbRestore(Abstract):
    """Database Dump Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'db:restore'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@db_restore_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        if _subprocess.call('which mongorestore', stdout=_subprocess.DEVNULL, stderr=_subprocess.DEVNULL, shell=True) != 0:
            raise Exception('Cannot find mongorestore executable.')

        from ._functions import run_command

        run_command('app:maintenance', enable=True)

        db_name = _reg.get('db.database')
        source_dir = _path.join(_reg.get('paths.root'), 'misc', 'dbdump', db_name)

        config = _db.get_config()

        command = 'mongorestore -h {}:{} --drop --gzip --stopOnError --dir {} -d {}'.\
            format(config['host'], config['port'], source_dir, db_name)

        if config['user']:
            command += ' -u {} -p {}'.format(config['user'], config['password'])
        if config['ssl']:
            command += ' --ssl --sslAllowInvalidCertificates'

        r = _subprocess.call(command, shell=True)

        run_command('app:maintenance', disable=True)

        return r

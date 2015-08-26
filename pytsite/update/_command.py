"""PytSite Update Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pickle as _pickle
from os import path as _path
from pytsite import console as _console, events as _events, lang as _lang, version as _pytsite_ver, reg as _reg
__import__('pytsite.maintenance')


class Update(_console.command.Abstract):
    """Setup Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'update'

    def get_description(self) -> str:
        """Get description of the command.
        """
        return _lang.t('pytsite.update@update_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        last_update = self._get_state()
        current_ver_list = _pytsite_ver.split('.')
        cur_ver = {'major': int(current_ver_list[0]), 'minor': int(current_ver_list[1])}
        cur_ver['rev'] = int(current_ver_list[2]) if len(current_ver_list) == 3 else 0

        last_major = last_update['major']
        last_minor = last_update['minor']
        last_rev = last_update['rev']

        print(cur_ver)
        print(last_update)

        # return

        if last_major == cur_ver['major'] and last_minor == cur_ver['minor'] and last_rev == cur_ver['rev']:
            return

        _console.run_command('maintenance', enable=True)

        stop = False
        for major in range(0, 100):
            if major < last_major:
                continue
            if stop:
                break
            for minor in range(0, 100):
                if minor < last_minor:
                    continue
                if stop:
                    break
                for rev in range(0, 100):
                    if rev < last_rev:
                        continue
                    if stop:
                        break

                    if cur_ver['major'] <= major and cur_ver['minor'] <= minor and cur_ver['rev'] <= rev:
                        stop = True


                    if rev:
                        ver_str = '{}.{}.{}'.format(major, minor, rev)
                    else:
                        ver_str = '{}.{}'.format(major, minor)

                    print(ver_str)

        self._save_state(cur_ver)
        _console.run_command('maintenance', disable=True)

        # _events.fire('pytsite.update')




    def _get_state(self, as_str: bool=False):
        """
        :return: dict|str
        """
        data = {'major': 0, 'minor': 0, 'rev': 0}

        data_path = self._get_data_path()
        if not _path.exists(data_path):
            return data
        else:
            with open(data_path, 'rb') as f:
                data = _pickle.load(f)

        if as_str:
            if data['rev']:
                data = '{}.{}.{}'.format(data['major'], data['minor'], data['rev'])
            else:
                data = '{}.{}'.format(data['major'], data['minor'])

        return data

    def _save_state(self, state: dict):
        with open(self._get_data_path(), 'wb') as f:
            _pickle.dump(state, f)

    def _get_data_path(self) -> str:
        return _path.join(_reg.get('paths.storage'), 'update.data')

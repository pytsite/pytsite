import sys as _sys
import unittest as _unittest
from os import path as _path
from pytsite import console as _console, reg as _reg


class Test(_console.Command):
    def __init__(self):
        super().__init__()

        self._define_argument(_console.argument.Argument('target', required=True))

    @property
    def name(self) -> str:
        return 'test:run'

    @property
    def description(self) -> str:
        return 'pytsite.testing@console_command_description'

    def execute(self):
        argv = [_sys.argv[0], 'discover']
        verbosity = 2 if _reg.get('debug') else 1
        target_paths = []

        target = self.get_argument_value(0)  # type: str

        if target.startswith('plugins.'):
            target_paths.append(_path.join(_reg.get('paths.plugins'), target, 'tests'))
        else:
            target_paths.append(_path.join(_reg.get('paths.pytsite'), target, 'tests'))

        for target_path in target_paths:
            if not _path.exists(target_path):
                raise _console.error.Error('Directory {} is not found'.format(target_path))

            argv[2:3] = ['-s', target_path]
            _unittest.TestProgram(None, argv=argv, failfast=True, verbosity=verbosity)

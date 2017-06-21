import sys as _sys
import unittest as _unittest
from os import path as _path
from pytsite import console as _console, reg as _reg


class Test(_console.Command):
    def __init__(self):
        super().__init__()

        self.define_option(_console.option.Bool('no-discover'))

    @property
    def name(self) -> str:
        return 'test:run'

    @property
    def description(self) -> str:
        return 'pytsite.testing@console_command_description'

    @property
    def signature(self) -> str:
        return '{} <TARGET>...'.format(super().signature)

    def exec(self):
        verbosity = 2 if _reg.get('debug') else 1

        if not self.args:
            raise _console.error.MissingArgument('pytsite.testing@target_is_not_specified')

        for target in self.args:
            argv = [_sys.argv[0]]

            if self.opt('no-discover') or '.tests.' in target:
                argv.append(target)
                _unittest.TestProgram(None, argv=argv, failfast=True, verbosity=verbosity)

            else:
                argv += ['discover', '-s']

                if target.startswith('pytsite.'):
                    target = _path.join(_reg.get('paths.pytsite'), target.replace('pytsite.', ''), 'tests')
                else:
                    target = _path.join(_reg.get('paths.root'), target.replace('.', _path.sep), 'tests')

                if not _path.exists(target):
                    raise _console.error.Error('Directory {} is not found'.format(target))

                argv.append(target)
                _unittest.TestProgram(None, argv=argv, failfast=True, verbosity=verbosity)

"""PytSite Console.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod
from sys import argv, exit
from re import sub
from os import path
from . import reg

__commands = {}


class AbstractCommand(ABC):
    """Abstract command.
    """

    @abstractmethod
    def get_name(self)->str:
        pass

    @abstractmethod
    def get_description(self)->str:
        pass

    @abstractmethod
    def execute(self, **kwargs: dict):
        pass


def register_command(obj: AbstractCommand):
    """Register a console command.
    """

    global __commands
    __commands[obj.get_name()] = obj


def get_command(name: str)->AbstractCommand:
    """Get a console command.
    """

    global __commands
    if name not in __commands:
        raise Exception("Command '{0}' is not registered.".format(name))

    return __commands[name]


def run_command(name: str, **kwargs: dict):
    """Run a console command.
    """

    return get_command(name).execute(**kwargs)


def usage():
    """Print the usage message.
    """

    global __commands
    r = ''
    for name, cmd in sorted(__commands.items()):
        r += "{0} -- {1}\n".format(name, cmd.get_description())

    return r


def run():
    """Run the console.
    """

    if len(argv) < 2:
        print(usage())
        exit(-1)

    cmd_args = {}
    for arg in argv[2:]:
        if arg.startswith('--'):
            arg = sub(r'^--', '', arg)
            arg_split = arg.split('=')
            if len(arg_split) == 1:
                cmd_args[arg_split[0]] = True
            else:
                arg_val = arg_split[1]
                cmd_args[arg_split[0]] = arg_val

    # Check if the setup completed
    if not path.exists(reg.get('paths.setup.lock')) and argv[1] != 'app:setup':
        from pytsite.core.lang import t
        raise Exception(t('pytsite.core@setup_is_not_completed'))

    return run_command(argv[1], **cmd_args)

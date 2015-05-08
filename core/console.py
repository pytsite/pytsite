__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod
from sys import argv, exit
from re import sub
from . import application

__commands = dict()


class Command(ABC):
    @abstractmethod
    def get_name(self)->str:
        pass

    @abstractmethod
    def get_description(self)->str:
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass


def register_command(obj: Command):
    """Register a console command.
    """
    __commands[obj.get_name()] = obj


def get_command(name: str)->Command:
    """Get a console command.
    """
    if name not in __commands:
        raise Exception("Command '{0}' is not registered.".format(name))
    return __commands[name]


def run_command(name: str, args: dict):
    """Run a console command.
    """
    return get_command(name).execute(args)


def usage():
    """Print the usage.
    """
    r = ''
    for name, cmd in __commands.items():
        r += "{0}\t{1}".format(name, cmd.get_description())
    return r


def run():
    """Run the console.
    """
    if not application.is_initialized():
        raise Exception("Application is not initialized.")

    if len(argv) == 1:
        print(usage())
        exit(-1)

    cmd_args = dict()
    for arg in argv[2:]:
        if arg.startswith('--'):
            arg = sub(r'^--', '', arg)
            arg_split = arg.split('=')
            if len(arg_split) == 1:
                cmd_args[arg_split[0]] = True
            else:
                arg_val = arg_split[1]
                cmd_args[arg_split[0]] = arg_val

    return run_command(argv[1], cmd_args)
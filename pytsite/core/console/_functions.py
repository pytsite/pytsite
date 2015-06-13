"""PytSite Console.
"""
from pytsite.core.console._commands import Abstract

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from sys import argv, exit
from re import sub
from os import path
from pytsite.core.console.errors import ConsoleRuntimeError
from pytsite.core import reg

__commands = {}

COLOR_HEADER = '\033[95m'
COLOR_INFO = '\033[94m'
COLOR_SUCCESS = '\033[92m'
COLOR_WARNING = '\033[93m'
COLOR_ERROR = '\033[91m'
COLOR_BOLD = '\033[1m'
COLOR_UNDERLINE = '\033[4m'
COLOR_END = '\033[0m'


def register_command(obj: Abstract):
    """Register a console command.
    """
    global __commands
    __commands[obj.get_name()] = obj


def get_command(name: str)->Abstract:
    """Get a console command.
    """

    global __commands
    if name not in __commands:
        raise Exception("Command '{0}' is not registered.".format(name))

    return __commands[name]


def run_console_command(name: str, **kwargs: dict):
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

    try:
        # Check if the setup completed
        if not path.exists(reg.get('paths.setup.lock')) and argv[1] != 'app:setup':
            from pytsite.core.lang import t
            raise ConsoleRuntimeError(t('pytsite.core@setup_is_not_completed'))

        return run_console_command(argv[1], **cmd_args)

    except ConsoleRuntimeError as e:
        print_error(str(e))
        exit(-1)


def print_info(msg: str):
    print('{}{}{}'.format(COLOR_INFO, msg, COLOR_END))


def print_success(msg: str):
    print('{}{}{}'.format(COLOR_SUCCESS, msg, COLOR_END))


def print_warning(msg: str):
    print('{}{}{}'.format(COLOR_WARNING, msg, COLOR_END))


def print_error(msg: str):
    print('{}{}{}'.format(COLOR_ERROR, msg, COLOR_END))

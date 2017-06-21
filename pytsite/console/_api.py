"""PytSite Console.
"""
import re as _re
from pytsite import reg as _reg, lang as _lang, logger as _logger
from . import _error, _command

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_commands = {}

COLOR_HEADER = '\033[95m'
COLOR_INFO = '\033[94m'
COLOR_SUCCESS = '\033[92m'
COLOR_WARNING = '\033[93m'
COLOR_ERROR = '\033[91m'
COLOR_BOLD = '\033[1m'
COLOR_UNDERLINE = '\033[4m'
COLOR_END = '\033[0m'


def register_command(obj: _command.Command):
    """Register a console command.
    """
    global _commands
    _commands[obj.name] = obj


def get_command(name: str) -> _command.Command:
    """Get a console command.
    """
    if name not in _commands:
        raise _error.CommandNotFound(_lang.t('pytsite.console@unknown_command', {'name': name}))

    return _commands[name]


def run_command(name: str, options: dict = None, arguments: list = None):
    """Run a console command.
    """
    cmd = get_command(name)

    # Set options
    if options:
        for opt_name, opt_val in options.items():
            opt_name = opt_name.replace('_', '-')
            cmd.set_opt(opt_name, opt_val)

    # Set arguments
    if arguments:
        cmd.set_args(arguments)

    try:
        return cmd.do_execute()
    except Exception as e:
        _logger.error(str(e), exc_info=e)
        raise e


def usage():
    """Print the usage message.
    """
    global _commands
    r = ''
    for name, cmd in sorted(_commands.items()):
        r += "{}{}{} -- {}\n".format(COLOR_HEADER, name, COLOR_END, _lang.t(cmd.description))

    return r


def run():
    """Run the console.
    """
    from sys import argv, exit

    # Print usage
    if len(argv) < 2:
        print(usage())
        exit(-1)

    # Command name
    cmd_name = argv[1]

    # Parse arguments
    options = {}
    arguments = []
    for arg_v in argv[2:]:
        if arg_v.startswith('--'):
            opt = _re.sub(r'^--', '', arg_v)
            opt_split = opt.split('=')
            if len(opt_split) == 1:
                options[opt_split[0]] = True
            else:
                opt_val = opt_split[1]
                options[opt_split[0]] = opt_val
        else:
            arguments.append(arg_v)

    try:
        # Check if the setup completed
        from os import path
        if not path.exists(_reg.get('paths.setup.lock')) and argv[1] != 'setup':
            from pytsite.lang import t
            raise _error.Error(t('pytsite.setup@setup_is_not_completed'))

        return run_command(cmd_name, options, arguments)

    except _error.Error as e:
        print_error(str(e))
        exit(-1)


def _print(msg: str, color: str):
    if _reg.get('env.type') == 'console':
        print('{}{}{}'.format(color, msg, COLOR_END))


def print_info(msg: str):
    _logger.info(msg)
    _print(msg, COLOR_INFO)


def print_success(msg: str):
    _logger.info(msg)
    _print(msg, COLOR_SUCCESS)


def print_warning(msg: str):
    _logger.warn(msg)
    _print(msg, COLOR_WARNING)


def print_error(msg: str):
    _logger.error(msg)
    _print(msg, COLOR_ERROR)

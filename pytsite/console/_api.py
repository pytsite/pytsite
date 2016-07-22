"""PytSite Console.
"""
from pytsite import reg as _reg, lang as _lang, validation as _validation, logger as _logger
from . import _error, _command

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__commands = {}

COLOR_HEADER = '\033[95m'
COLOR_INFO = '\033[94m'
COLOR_SUCCESS = '\033[92m'
COLOR_WARNING = '\033[93m'
COLOR_ERROR = '\033[91m'
COLOR_BOLD = '\033[1m'
COLOR_UNDERLINE = '\033[4m'
COLOR_END = '\033[0m'


def register_command(obj: _command.Abstract):
    """Register a console command.
    """
    global __commands
    __commands[obj.get_name()] = obj


def get_command(name: str) -> _command.Abstract:
    """Get a console command.
    """
    if name not in __commands:
        raise _error.CommandNotFound(_lang.t('pytsite.console@unknown_command', {'name': name}))

    return __commands[name]


def run_command(name: str, args: tuple=(), **kwargs):
    """Run a console command.
    """
    cmd = get_command(name)
    valid_options = []

    for opts in cmd.get_options():
        opt_name = opts[0]
        valid_options.append(opt_name)
        opt_rule = opts[1] if len(opts) >= 2 else None  # type: _validation.rule.Base

        if opt_rule:
            try:
                opt_rule.validate(kwargs.get(opt_name))
            except _validation.error.RuleError as e:
                raise _error.Error('--{}: {}'.format(opt_name, e))

    kwargs = {k.replace('_', '-'): v for k, v in kwargs.items()}
    for k in kwargs.keys():
        if k not in valid_options:
            raise _error.InvalidOption('Invalid option: --{}'.format(k))

    try:
        return cmd.execute(args, **kwargs)
    except Exception as e:
        _logger.error(str(e), exc_info=e)
        raise e


def usage():
    """Print the usage message.
    """
    global __commands
    r = ''
    for name, cmd in sorted(__commands.items()):
        r += "{}{}{} -- {}\n".format(COLOR_HEADER, name, COLOR_END, cmd.get_description())

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
    cmd_opts = {}
    cmd_args = []
    for arg in argv[2:]:
        if arg.startswith('--'):
            from re import sub
            arg = sub(r'^--', '', arg)
            arg_split = arg.split('=')
            if len(arg_split) == 1:
                cmd_opts[arg_split[0]] = True
            else:
                arg_val = arg_split[1]
                cmd_opts[arg_split[0]] = arg_val
        else:
            cmd_args.append(arg)

    try:
        # Check if the setup completed
        from os import path
        if not path.exists(_reg.get('paths.setup.lock')) and argv[1] != 'setup':
            from pytsite.lang import t
            raise _error.Error(t('pytsite.setup@setup_is_not_completed'))

        return run_command(cmd_name, args=tuple(cmd_args), **cmd_opts)

    except _error.Error as e:
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

from pytsite import console as _console


def pytsite_update_after():
    _console.run_command('odm', reindex=True)

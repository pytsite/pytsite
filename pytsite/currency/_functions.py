"""Currency Functions
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'



__currencies = []


def define(code: str):
    """Define a currency.
    """
    code = code.upper()
    if code in __currencies:
        raise KeyError("Currency '{}' already defined.")

    __currencies.append(code)


def get_currencies(include_main: bool=True) -> list:
    """Get defined currencies.
    """
    r = []
    for c in __currencies:
        if not include_main and c == get_main():
            continue
        r.append(c)

    return r


def get_main() -> str:
    """Get main currency code.
    """
    if not __currencies:
        raise Exception('No currencies are defined.')

    return __currencies[0]


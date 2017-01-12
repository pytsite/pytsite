"""PytSite Form Endpoints.
"""
from . import _cache

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def submit(args: dict, inp: dict):
    """Default submit endpoint.
    """
    # Dispense the form
    frm = _cache.get(args.get('uid'))

    # Setup widgets for all steps
    frm.remove_widgets()
    for step in range(1, frm.steps + 1):
        frm.step = step
        frm.setup_widgets(False)

    # Validate the form
    frm.fill(inp, mode='validation').validate()

    # Refill the form in 'normal' mode
    frm.fill(inp)

    # Notify form about submit
    return frm.submit()

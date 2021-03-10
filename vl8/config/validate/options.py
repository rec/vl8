from .. import parse_args
from ..expand import Expander

"""Command line options from flags"""

DEFAULTS = dict(parse_args.DEFAULTS)
DEFAULTS.pop('commands')
validate = Expander('options', DEFAULTS)

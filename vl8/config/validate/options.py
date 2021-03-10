from .. import parse_args
from ..expand import Expander

"""Command line options from flags"""

DEFAULTS = vars(parse_args([]))
DEFAULTS.pop('commands')
validate = Expander('options', DEFAULTS)

from .. import parse_args
from ..expand import Expander

"""Command line options from flags"""

validate = Expander('options', parse_args.DEFAULTS)

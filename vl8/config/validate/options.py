from .. import parse_args
from ..expand import Expander

DEFAULTS = vars(parse_args.parse([]))
DEFAULTS.pop('arguments')
validate = Expander('options', DEFAULTS)

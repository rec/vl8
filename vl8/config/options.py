from . import parse_args
from .expand import Expander

DEFAULTS = vars(parse_args.PARSER.parse([]))
DEFAULTS.pop('arguments')
validate = Expander('options', DEFAULTS)

from . import args
from .expand import Expander

DEFAULTS = vars(args.PARSER.parse([]))
DEFAULTS.pop('arguments')
validate = Expander('options', DEFAULTS)

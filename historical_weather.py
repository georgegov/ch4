from constants import *
from utils import arg_parser


args = arg_parser.parse_args()

# TODO: Remove this
print(args)

if args['function_name'] == DAYS_OF_PRECIP:
    pass
elif args['function_name'] == MAX_TEMP_DELTA:
    pass

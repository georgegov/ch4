import argparse
from constants import *
import os
import sys


MAIN_FILE_BASENAME = os.path.basename(sys.modules["__main__"].__file__)


def parse_args():
    f"""
    Parse command-line arguments
    :return:
       dict with key-value pairs for keys: {FUNCTION_NAME}, {CITY}, {YEAR}, {MONTH}
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(f'{FUNCTION_NAME}', choices=[DAYS_OF_PRECIP, MAX_TEMP_DELTA])
    parser.add_argument(f'--{CITY}', required=True, choices=[BOSTON, JUNEAU, MIAMI])

    max_temp_delta_group = parser.add_argument_group(MAX_TEMP_DELTA)
    max_temp_delta_group.add_argument(f'--{YEAR}', type=int, choices=range(MIN_YEAR, MAX_YEAR + 1))
    max_temp_delta_group.add_argument(f'--{MONTH}', type=int, choices=range(1, 13))

    args = vars(parser.parse_args())

    # --year and --month arguments do not apply to DAYS_OF_PRECIP
    if args[FUNCTION_NAME] == DAYS_OF_PRECIP:
        if args[YEAR] is not None:
            __exit_with_message(parser, f'{MAIN_FILE_BASENAME}: error: --year not applicable for {DAYS_OF_PRECIP}')
        if args[MONTH] is not None:
            __exit_with_message(parser, f'{MAIN_FILE_BASENAME}: error: --month not applicable for {DAYS_OF_PRECIP}')

    # if --month argument is specified, --year is also required
    if args[MONTH] is not None and args[YEAR] is None:
        __exit_with_message(parser, f'{MAIN_FILE_BASENAME}: error: argument --{MONTH}: also requires --{YEAR}')

    return args


def __exit_with_message(parser, message):
    parser.print_usage()
    sys.exit(message)

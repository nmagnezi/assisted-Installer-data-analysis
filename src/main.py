import logging
import sys

from src.common import arg_parser
from src.common import helpers


LOG = logging.getLogger(__name__)


def main(args):
    pass


if __name__ == '__main__':
    cmd_line_args = arg_parser.process_args()
    helpers.configure_logger(cmd_line_args.debug)
    sys.exit(main(cmd_line_args))

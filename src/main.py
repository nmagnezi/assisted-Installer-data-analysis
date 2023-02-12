import logging
import sys

from src.client import client
from src.common import helpers, arg_parser

LOG = logging.getLogger(__name__)


def main(args):
    helpers.configure_logger(args.debug)
    assisted_client = client.APIClient(args.env, args.download)


if __name__ == '__main__':
    cmd_line_args = arg_parser.process_args()
    helpers.configure_logger(cmd_line_args.debug)
    sys.exit(main(cmd_line_args))

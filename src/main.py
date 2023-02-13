import logging
import sys

from client import client
from common import helpers, arg_parser

LOG = logging.getLogger(__name__)


def main(args):
    assisted_client = client.APIClient(args.env, args.download)
    helpers.print_data_stats(
        clusters=assisted_client.clusters,
        infraenvs=assisted_client.infraenvs,
        hosts=assisted_client.hosts,
        env=args.env,
    )


if __name__ == '__main__':
    cmd_line_args = arg_parser.process_args()
    helpers.configure_logger(cmd_line_args.debug)
    sys.exit(main(cmd_line_args))

import argparse

from common import constants


def process_args():
    parser = argparse.ArgumentParser(
        description='Assisted Installer Data Analysis'
    )
    parser.add_argument(
        '-e', '--env',
        default=constants.PROD,
        help='Assisted Installer Environment',
        choices=[constants.PROD, constants.STAGE, constants.INTEGRATION],
        required=False
    )
    parser.add_argument(
        '--download',
        default=False,
        action='store_true',
        help='Debug mode True/False, defaults to False',
        required=False
    )
    parser.add_argument(
        '-f', '--folder',
        default=constants.DATA_FOLDER,
        action='store_true',
        help='Data folder to store information about Clusters, InfraEnvs and Hosts',
        required=False
    )
    parser.add_argument(
        '-d', '--debug',
        default=False,
        action='store_true',
        help='Debug mode True/False, defaults to False',
        required=False
    )
    return parser.parse_args()

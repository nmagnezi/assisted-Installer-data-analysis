import json
import logging

LOG = logging.getLogger(__name__)

from common import stats

def configure_logger(debug_mode):
    logging.basicConfig(
        level=logging.DEBUG if debug_mode is True else logging.INFO,
        format='%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s'
    )


def load_json_from_file(file):
    with open(file, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object


def print_data_stats(clusters, infraenvs, hosts, env):
    data = stats.prepare_data(clusters, infraenvs, hosts)

    LOG.info(f"Facts about the data scraped from {env}")
    LOG.info(f"Total of {len(clusters)} clusters and {len(infraenvs)} infraenvs total")
    LOG.info(f"Detected {data['count_unbound_infraenvs']} unbounded infraenvs")
    LOG.info(f"Out of {len(infraenvs)} infraenvs, {data['infraenvs_with_static_network_config']} "
             f"were configured with static_network_config")
    LOG.info(f"Out of {data['infraenvs_with_static_network_config']} were configured with static_network_config,"
             f" {data['infraenvs_with_static_network_config_bonds']} were configured with bonds")

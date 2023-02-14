import json
import logging

LOG = logging.getLogger(__name__)

from common import stats


class Dict2Class(object):

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


def configure_logger(debug_mode):
    logging.basicConfig(
        level=logging.DEBUG if debug_mode is True else logging.INFO,
        format='%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s'
    )


def load_json_from_file(file):
    with open(file, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object


def _print_cluster_states(cluster_states):
    for state, amount in cluster_states.items():
        LOG.info(f"Cluster states: {amount} {state} ")


def print_data_stats(clusters, infraenvs, hosts, env):
    data = stats.prepare_data(clusters, infraenvs, hosts)
    LOG.info(f"Facts about the data scraped from {env}")
    LOG.info(f"Total of {len(clusters)} clusters and {len(infraenvs)} infraenvs total")
    _print_cluster_states(data.cluster_states)
    LOG.info(f"Detected {data.count_unbound_infraenvs} unbounded infraenvs")
    LOG.info(f"Out of {len(infraenvs)} infraenvs, {data.infraenvs_with_static_network_config} "
             f"were configured with static_network_config")
    LOG.info(f"Out of {data.infraenvs_with_static_network_config} were configured with static_network_config,"
             f" {data.infraenvs_with_static_network_config_bonds} were configured with bonds")

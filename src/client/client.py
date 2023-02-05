import json
import requests
import logging
import time

from src.client import client_helpers
from src.common import constants

LOG = logging.getLogger(__name__)


def get_clusters(url, download_files):
    if download_files:
        LOG.info("Downloading Clusters data...")
        clusters = requests.get(
            url=f'{url}/clusters',
            headers={'Authorization': f'Bearer {client_helpers.get_token()}'},
        ).json()
        LOG.info("Done!")
        json_object = json.dumps(clusters, indent=4)
        with open(constants.CLUSTERS_FILE, "w") as f:
            f.seek(0)
            f.write(json_object)
            f.truncate()
    clusters = client_helpers.load_json_from_file(constants.CLUSTERS_FILE)
    return client_helpers.build_search_index_by_id(clusters)


def get_infraenvs(url, download_files):
    if download_files:
        LOG.info("Downloading InfraEnvs data...")
        infraenvs = requests.get(
            url=f'{url}/infra-envs/',
            headers={'Authorization': f'Bearer {client_helpers.get_token()}'},
        ).json()
        LOG.info("Done!")
        json_object = json.dumps(infraenvs, indent=4)
        with open(constants.INFRAENV_FILE, "w") as f:
            f.seek(0)
            f.write(json_object)
            f.truncate()
    return client_helpers.load_json_from_file(constants.INFRAENV_FILE)


def get_hosts(url, download_files, infraenvs):
    infraenv_hosts = dict()
    if download_files:
        LOG.info("Downloading Hosts data. This might take a while...")
        for i, infraenv in enumerate(infraenvs):
            time.sleep(0.5)
            infraenv_id = infraenv["id"]
            attempts = 3
            hosts = []
            for j in range(constants.HOSTS_GET_ATTEMPTS):
                try:
                    hosts = requests.get(url=f'{url}/infra-envs/{infraenv_id}/hosts',
                                         headers={'Authorization': f'Bearer {client_helpers.get_token()}'}).json()
                except requests.exceptions.RequestException:
                    LOG.debug(f"failed requesting hosts for infraenv {infraenv_id} - attempt ({j}/{attempts})")
                    continue
                break
            infraenv_hosts[infraenv['id']] = list()
            if not hosts:
                LOG.debug(f"adding infraenv ({i}/{len(infraenvs)}) {infraenv_id} has no hosts")
                continue
            for host in hosts:
                host_id = host['id']
                infraenv_hosts[infraenv['id']].append(host)
                LOG.debug(f"adding infraenv ({i}/{len(infraenvs)}) {infraenv_id} host {host_id}")
        LOG.info("Done!")
        json_object = json.dumps(infraenv_hosts, indent=4)
        with open(constants.HOSTS_FILE, "w") as f:
            f.seek(0)
            f.write(json_object)
            f.truncate()
    return client_helpers.load_json_from_file(constants.HOSTS_FILE)

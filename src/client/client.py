import json
import requests
import logging
import os
import subprocess
import time

from client import client_helpers
from common import constants

LOG = logging.getLogger(__name__)


class APIClient(object):

    def __init__(self, url, download_files):
        self.url = url
        self.download_files = download_files
        self.token = self._get_token()
        self.clusters = self._get_clusters()
        self.infraenvs = self._get_infraenvs()
        self.hosts = self._get_hosts()

    def get_clusters(self):
        return self.clusters

    def _get_clusters(self):
        if self.download_files:
            LOG.info("Downloading Clusters data...")
            clusters = requests.get(
                url=f'{self.url}/clusters',
                headers={'Authorization': f'Bearer {self.token}'},
            ).json()
            LOG.info("Done!")
            json_object = json.dumps(clusters, indent=4)
            with open(constants.CLUSTERS_FILE, "w") as f:
                f.seek(0)
                f.write(json_object)
                f.truncate()
        clusters = client_helpers.load_json_from_file(constants.CLUSTERS_FILE)
        return client_helpers.build_search_index_by_id(clusters)

    def get_infraenvs(self):
        return self.infraenvs

    def _get_infraenvs(self):
        if self.download_files:
            LOG.info("Downloading InfraEnvs data...")
            infraenvs = requests.get(
                url=f'{self.url}/infra-envs/',
                headers={'Authorization': f'Bearer {self.token}'},
            ).json()
            LOG.info("Done!")
            json_object = json.dumps(infraenvs, indent=4)
            with open(constants.INFRAENV_FILE, "w") as f:
                f.seek(0)
                f.write(json_object)
                f.truncate()
        return client_helpers.load_json_from_file(constants.INFRAENV_FILE)

    def get_hosts(self):
        return self.hosts

    def _get_infraenv_hosts(self, infraenv_id):
        hosts = list()
        for j in range(constants.HOSTS_GET_ATTEMPTS):
            try:
                hosts = requests.get(url=f'{self.url}/infra-envs/{infraenv_id}/hosts',
                                     headers={'Authorization': f'Bearer {self._get_token()}'}).json()
            except requests.exceptions.RequestException:
                LOG.info(
                    f"failed requesting hosts for infraenv {infraenv_id} - attempt ({j}/{constants.HOSTS_GET_ATTEMPTS})")
                continue
            break
        return hosts

    def _index_hosts(self, infraenv_id, infraenv_idx, infraenv_hosts, hosts):
        infraenv_hosts[infraenv_id] = list()

        for host in hosts:
            if not (host or host.get('id')):
                continue

            host_id = host.get('id')
            if infraenv_hosts.get(infraenv_id) is not None:
                infraenv_hosts[infraenv_id].append(host)
                LOG.info(f"adding infraenv ({infraenv_idx}/{len(self.infraenvs)}) {infraenv_id} host {host_id}")

    def _get_hosts(self):
        infraenv_hosts = dict()
        if self.download_files:
            LOG.info("Downloading Hosts data. This might take a while...")
            for i, infraenv in enumerate(self.infraenvs):

                time.sleep(0.5)  # So it won't flood the env
                if not (infraenv or infraenv.get("id")):
                    LOG.warning("Invalid InfraEnv, skipping")
                    continue
                infraenv_id = infraenv["id"]
                hosts = self._get_infraenv_hosts(infraenv_id)
                if not hosts:
                    LOG.info(f"adding infraenv ({i}/{len(self.infraenvs)}) {infraenv_id} has no hosts")
                    continue

                self._index_hosts(
                    infraenv_id=infraenv_id,
                    infraenv_idx=i,
                    infraenv_hosts=infraenv_hosts,
                    hosts=hosts
                )

            LOG.info("Done!")
            json_object = json.dumps(infraenv_hosts, indent=4)
            with open(constants.HOSTS_FILE, "w") as f:
                f.seek(0)
                f.write(json_object)
                f.truncate()
        return client_helpers.load_json_from_file(constants.HOSTS_FILE)

    def _get_token(self):
        if not self.download_files:
            return ""
        token = os.getenv('TOKEN')
        if token:
            return token
        try:
            token = subprocess.check_output('ocm token', shell=True).decode("utf-8")[:-1]
        except Exception:
            LOG.error(f"FATAL: Unable to get a token via 'ocm token'. Make sure you fetch a token for {self.url} "
                      f"and use it in 'ocm login --token=\"...\"'")
            raise
        return token

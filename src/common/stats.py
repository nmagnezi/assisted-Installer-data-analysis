class Dict2Class(object):

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


def count_unbounded_infraenvs(infraenvs):
    count_unbound_infraenvs = 0
    for infraenv in infraenvs:
        cluster_id = infraenv.get('cluster_id')
        if not cluster_id:
            count_unbound_infraenvs += 1
    return count_unbound_infraenvs


def count_infraenvs_with_static_network_config(infraenvs):
    infraenvs_with_nmstate = 0
    for infraenv in infraenvs:
        if infraenv.get('static_network_config'):
            infraenvs_with_nmstate += 1
    return infraenvs_with_nmstate


def count_infraenvs_with_static_network_config_bonds(infraenvs):
    infraenvs_with_static_network_config_bonds = 0
    for infraenv in infraenvs:
        if infraenv.get('static_network_config') and 'bond' in infraenv.get('static_network_config'):
            infraenvs_with_static_network_config_bonds += 1
    return infraenvs_with_static_network_config_bonds


def get_cluster_states(clusters):
    cluster_states = dict()
    for _, cluster in clusters.items():
        try:
            cluster_states[cluster.get('status')] += 1
        except KeyError:
            cluster_states[cluster.get('status')] = 1
    return cluster_states


def prepare_data(clusters, infraenvs, hosts):
    data = dict()
    data['cluster_states'] = get_cluster_states(clusters)
    data['count_unbound_infraenvs'] = count_unbounded_infraenvs(infraenvs)
    data['infraenvs_with_static_network_config'] = count_infraenvs_with_static_network_config(infraenvs)
    data['infraenvs_with_static_network_config_bonds'] = count_infraenvs_with_static_network_config_bonds(infraenvs)
    return Dict2Class(data)

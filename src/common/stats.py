

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


def prepare_data(clusters, infraenvs, hosts):
    data = dict()
    data['count_unbound_infraenvs'] = count_unbounded_infraenvs(infraenvs)
    data['infraenvs_with_static_network_config'] = count_infraenvs_with_static_network_config(infraenvs)
    data['infraenvs_with_static_network_config_bonds'] = count_infraenvs_with_static_network_config_bonds(infraenvs)

    return data

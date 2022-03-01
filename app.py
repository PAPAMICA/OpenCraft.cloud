#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack_api as oa
from diagrams import Diagram, Cluster
from diagrams.openstack.compute import Nova
from diagrams.openstack.orchestration import Heat
from diagrams.generic.network import Router
from diagrams.onprem.network import Internet
from diagrams.custom import Custom


cloud = oa.cloud_connection("prout")
instances = oa.get_instances_list(cloud)
networks = oa.list_networks(cloud)

graph_attr = {
    "layout":"dot",
    "concentrate":"true",
    "splines":"spline",
}

print(instances)
with Diagram("\nInfrastructure", show=False, direction="TB", graph_attr=graph_attr,) as diag:

    # Instances
    

    for id, network in networks.items():
        instances_net = []
        for instance in instances:
            # Instance per network
            if (instances[instance]['Network'] == network):
                instance = Custom(f"{instance} \n{instances[instance]['IP']}", "./img/server.png")
                instances_net.append(instance)
        if instances_net:
            network_logo = Custom(f"{network}", "./img/network.png")
            network_logo >> instances_net



diag


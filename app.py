#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack_api as oa
from diagrams import Diagram, Cluster
from diagrams.custom import Custom


cloud = oa.cloud_connection("prout")
instances = oa.get_instances_list(cloud)
networks = oa.list_networks(cloud)
routers = oa.list_router_v2(cloud)

graph_attr = {
    "layout": "dot",
    "concentrate": "true",
    "splines": "spline",
}
with Diagram("\nInfrastructure", show=False, direction="TB", graph_attr=graph_attr,) as diag:
    for router in routers:
        networkwan = routers[router]['network_wan']
        img_router = Custom(
            f"{router}\n WAN : {routers[router]['ipwan']} \n LAN : {routers[router]['iplan']}", "./img/router.png")
        img_network_wan = Custom(f"{networkwan}", "./img/internet.png")
        networklan = routers[router]['network_lan']
        img_network_lan = Custom(f"{networklan}", "./img/network.png")

        instances_net = []
        for instance in instances:
            # Instance per network
            if (instances[instance]['Network'] == networklan):
                instance = Custom(
                    f"{instance} \n{instances[instance]['IP']}", "./img/server.png")
                instances_net.append(instance)
        if instances_net:
            img_network_wan >> img_router >> img_network_lan >> instances_net

    instances_net = []
    for instance in instances:
        # Instance per network
        if (instances[instance]['Network'] == "ext-net1"):
            instance = Custom(
                f"{instance} \n{instances[instance]['IP']}", "./img/server.png")
            instances_net.append(instance)
    if instances_net:
        img_network_wan = Custom(f"ext-net1", "./img/internet.png")
        img_network_wan >> instances_net
diag

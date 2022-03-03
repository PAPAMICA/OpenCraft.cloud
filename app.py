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
tag_attr = {
    "height": "4",
    "width": "4",
}
with Diagram("\nInfrastructure", show=False, direction="TB", graph_attr=graph_attr, outformat=["png"]) as diag:
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
                sc = oa.list_sc_instance(cloud, instances[instance]['ID'])
                for name in sc:
                    sc = name
                    with Cluster(f"{sc}"):
                        with Cluster(f"{instance}", direction="TB"):
                            sc_group = img_instance = Custom(
                                f"{instance} \n{instances[instance]['IP']}", "./img/server.png")

                            for tag in instances[instance]['Tags']:
                                if tag:
                                    with Cluster(f"Tags"):
                                        tags = img_tag = Custom(
                                                f"", f"./img/technos/{tag}.png", height="0.7", width="0.7", imagescale="false")

                    instances_net.append(sc_group)
        if instances_net:
            img_network_wan >> img_router >> img_network_lan >> instances_net

    instances_net = []
    for instance in instances:
        # Instance per network
        if (instances[instance]['Network'] == "ext-net1"):
            sc = oa.list_sc_instance(cloud, instances[instance]['ID'])
            scr = ""
            for name in sc:
                if (scr == ""):
                    scr = name
                else:
                    scr = scr + ", " + name
            with Cluster(f"{scr}"):
                with Cluster(f"{instance}", direction="TB"):
                    sc_group = img_instance = Custom(
                        f"{instance} \n{instances[instance]['IP']}", "./img/server.png")

                    for tag in instances[instance]['Tags']:
                        if tag:
                            with Cluster(f"Tags"):
                                tags = img_tag = Custom(
                                        f"", f"./img/technos/{tag}.png", height="0.7", width="0.7", imagescale="false")

            instances_net.append(sc_group)

            
    if instances_net:
        img_network_wan = Custom(f"ext-net1", "./img/internet.png")
        img_network_wan >> instances_net
diag

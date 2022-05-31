#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack_api as oa
from diagrams import Diagram, Cluster
from diagrams.custom import Custom
import argparse

parser = argparse.ArgumentParser(description='Create a graph of your OpenStack project.')
parser.add_argument("--openrc", required=True, help='Link to your openrc file')
args = parser.parse_args()

cloud = oa.cloud_connection(args.openrc)
instances = oa.get_instances_list(cloud)
networks = oa.list_networks(cloud)
routers = oa.list_router_v2(cloud)

graph_attr = {
    "layout": "dot",
    "concentrate": "true",
    "splines": "spline",
}
cluster_attr = {
    "layout": "fdp",
    "concentrate": "true",
    "splines": "spline",
}
tag_attr = {
    "height": "4",
    "width": "4",
}
with Diagram("\nInfrastructure", show=True, direction="TB") as diag:
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
                scr = ""
                for name in sc:
                    if (scr == ""):
                        scr = name
                    else:
                        scr = scr + ", " + name
                with Custom(f"Security Group : {scr}", "./img/firewall.png") as img_instance:
                    with Custom(f"{instance}\n{instances[instance]['IP']}", "./img/server.png"):
                        for tag in instances[instance]['Tags']:
                            if tag:
                                tags = img_tag = Custom(
                                        f"", f"./img/technos/{tag}.png")

                instances_net.append(img_instance)
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
            with Custom(f"Security Group : {scr}", "./img/firewall.png") as img_instance:
                with Custom(f"{instance}\n{instances[instance]['IP']}", "./img/server.png"):
                    for tag in instances[instance]['Tags']:
                        if tag:
                            tags = img_tag = Custom(
                                    f"", f"./img/technos/{tag}.png")

            instances_net.append(img_instance)

            
    if instances_net:
        img_network_wan = Custom(f"ext-net1", "./img/internet.png")
        img_network_wan >> instances_net
diag

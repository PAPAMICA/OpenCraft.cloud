#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import truediv
import openstack_api as oa
from diagrams import Diagram, Cluster
from diagrams.custom import Custom
import argparse
from os.path import exists

parser = argparse.ArgumentParser(description='Create a graph of your OpenStack project.')
parser.add_argument("--openrc", required=True, help='Link to your openrc file.')
parser.add_argument('--tags', action=argparse.BooleanOptionalAction, help='Show tags as pictures.')
args = parser.parse_args()

cloud = oa.cloud_connection(args.openrc)
instances = oa.get_instances_list(cloud)
networks = oa.list_networks(cloud)
routers = oa.list_router_v2(cloud)

graph_attr = {
    "layout": "dot",
    "concentrate": "true",
}
cluster_attr = {
    "layout": "dot",
}
tag_attr = {
    "height": "1",
    "width": "1",
}
edge_attr = {
    "minlen":"2",
}
with Diagram("\nInfrastructure", show=True, direction="TB", graph_attr=graph_attr, node_attr=tag_attr,edge_attr=edge_attr) as diag:
    for router in routers:
        networkwan = routers[router]['network_wan']
        img_router = Custom(
            f"{router}\n WAN : {routers[router]['ipwan']} \n LAN : {routers[router]['iplan']}", "./img/router.png")
        img_network_wan = Custom(f"{networkwan}", "./img/internet.png")
        networklan = routers[router]['network_lan']

        instances_net = []
        with Custom(f"Network : {networklan}", "./img/network.png") as img_network:
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
                            if args.tags == True:
                                for tag in instances[instance]['Tags']:
                                    if tag:
                                        if exists(f"./img/technos/{tag}.png"):
                                            tags = img_tag = Custom(
                                                    f"", f"./img/technos/{tag}.png")


                instances_net.append(img_instance)
        if instances_net:
            img_network_wan >> img_router >> img_network

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

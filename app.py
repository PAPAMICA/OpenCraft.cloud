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
list = oa.get_instances_list(cloud)


graph_attr = {
    "layout":"dot",
    "concentrate":"true",
    "splines":"spline",
}

print(list)
with Diagram("\nInfrastructure", show=False, direction="TB", graph_attr=graph_attr,) as diag:
    Internet = Internet("Internet")
    with Cluster("Public Cloud Infomaniak"):
        cluster = []
        for instance in list:
            instance = Custom(f"{instance} \n{list[instance]['IP']}", "./img/server.png")
            cluster.append(instance)
            print (cluster)
    Internet >> cluster

diag


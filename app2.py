#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker_api as docker
import argparse
import csv
from diagrams import Diagram, Cluster, Node, Edge
from diagrams.custom import Custom

parser = argparse.ArgumentParser(description='Create a graph of your Docker project.')
parser.add_argument("--container", required=False, help='Create a graph of one container')
parser.add_argument("--network", required=False, help='Create a graph of one network')
args = parser.parse_args()

graph_attr = {
    "layout": "dot",
    "concentrate":"true",
    "splines":"lines",
    "len":"4",
}

cluster_attr = {
    "layout": "fdp",
}
tag_attr = {
    "center": "true",
    "layout": "fdp",
    "imagepos": "mc"
}
edge_attr = {
    "len":"4",
}



def create_diagram():
    with Diagram("\nDocker infrastructure", show=False, direction="TB", graph_attr=graph_attr, node_attr=tag_attr,edge_attr=edge_attr) as diag:
        img_network = Custom(f"{args.network}\nSubnet: {_network[args.network]['Subnet']}", "./img/internet.png")
        with Custom(f"Subnet: {_network[args.network]['Subnet']}", "./img/network.png", direction="LR") as containers_subnet:
            containers = []
            for container in _network[args.network]['Containers']:
                img_container = Custom(
                    f"{container['Container']}\n IP : {container['IPv4']}", "./img/container.png")
                
                containers.append(img_container)

            
        img_network >> containers_subnet

       
    diag

def add_csv_line(file, fields):
    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def list_network(network):
    _network = docker.get_network_informations(network)
    try:
        _network[network]
    except:
        print (f"ERROR: {network} doesn't exist !")
        exit(1)

    file = 'test2.csv'
    fields = list()
    _name = network
    _type = "network"
    _ip = _network[network]['Subnet']
    _fill = "#f8cecc"
    _stroke = "#b85450"
    _refs = "-"
    _image = "https://send.papamica.fr/f.php?h=0f3ZrzyN&p=1"
    fields.extend((_name, _type, _ip, _fill, _stroke, _refs, _image))
    
    add_csv_line(file, fields)

    for container in _network[network]['Containers']:
        _container = docker.get_container_informations(container)
        #print(_container)
        file = 'test2.csv'
        fields = list()
        _name = container['Container']
        _type = "container"
        _ip = container['IPv4']
        _fill = "#dae8fc"
        _stroke = "#6c8ebf"
        _refs = network
        _image = "https://send.papamica.fr/f.php?h=36z5CCnq&p=1"
        fields.extend((_name, _type, _ip, _fill, _stroke, _refs, _image))
        add_csv_line(file, fields)

def list_all():
    _networks = docker.get_networks_list()
    for _network in _networks:
        list_network(_network)

if args.container:
    print(docker.get_container_informations(args.container))
elif args.network:
    list_network(args.network)
else:
    list_all()
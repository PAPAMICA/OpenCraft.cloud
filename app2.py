#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker_api as docker
import argparse
import csv
import pandas as pd
from diagrams import Diagram, Cluster, Node, Edge
from diagrams.custom import Custom

parser = argparse.ArgumentParser(description='Create a graph of your Docker project.')
parser.add_argument("--container", required=False, help='Create a graph of one container')
parser.add_argument("--network", required=False, help='Create a graph of one network')
args = parser.parse_args()

blacklist_networks = ["bridge","host","none"]


def add_csv_line(file, fields):
    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def delete_duplicate_line(file):
    with open(file, 'r') as in_file, open('export.csv', 'w') as out_file:
        seen = set() # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen: continue # skip duplicate

            seen.add(line)
            out_file.write(line)
   

def list_network(network, file):
    _network = docker.get_network_informations(network)
    try:
        _network[network]
    except:
        print (f"ERROR: {network} doesn't exist !")
        exit(1)
    
    fields = list()
    _name = network
    _type = "network"
    _option = ""
    _ip = _network[network]['Subnet']
    _note = "TEST"
    _fill = "#dae8fc"
    _stroke = "#6c8ebf"
    _refs = _network[network]['Driver']
    _image = "https://send.papamica.fr/f.php?h=0f3ZrzyN&p=1"
    fields.extend((_name, _type, _option, _ip, _note, _fill, _stroke, _refs, _image))
    
    add_csv_line(file, fields)
    list_containers(network, file)

def list_containers(network, file):
    if network != "":
        _network = docker.get_network_informations(network)
        containers =  _network[network]['Containers']
    else:
        containers = docker.get_containers_list()
        print(containers)
    for container in containers:
        if network != "":
            _container = docker.get_container_informations(container['Container'])
            _name = container['Container']
            _ip = " ".join(_container[_name]['IP'])
            if _container[_name]['Status'] == "running":
                _fill = "#d5e8d4"
                _stroke = "#82b366"
            else:
                _fill = "#f8cecc"
                _stroke = "#b85450"
            _refs = ",".join(_container[_name]['Network'])
        else:
            _container = docker.get_container_informations(container)
            _name = container
            _ip = " ".join(_container['IP'])
            if _container['Status'] == "running":
                _fill = "#d5e8d4"
                _stroke = "#82b366"
            else:
                _fill = "#f8cecc"
                _stroke = "#b85450"
            _refs = ",".join(_container['Network'])

        fields = list()
        _type = "container"
        _option = "-"
        _note = "Port: 1234/TCP"
        _image = "https://send.papamica.fr/f.php?h=36z5CCnq&p=1"
        fields.extend((_name, _type, _option, _ip, _note, _fill, _stroke, _refs, _image))
        add_csv_line(file, fields)

def list_all(file):
    _networks = docker.get_networks_list()
    for blacklist in blacklist_networks:
        _networks.remove(blacklist)
    for _network in _networks:
        list_network(_network, file)
    list_containers("", file)

if args.container:
    print(docker.get_container_informations(args.container))
elif args.network:
    file = 'test2.csv'
    list_network(args.network, file)
    delete_duplicate_line(file)
else:
    file = 'test2.csv'
    list_all(file)
    delete_duplicate_line(file)
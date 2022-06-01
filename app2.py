#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker_api as docker
import argparse

parser = argparse.ArgumentParser(description='Create a graph of your Docker project.')
parser.add_argument("--container", required=False, help='Create a graph of one container')
args = parser.parse_args()

if args.container:
    print(docker.get_container_informations(args.container))
else:
    print(f"Containers:\n{docker.get_containers_list()}\n\nNetworks:\n{docker.get_networks_list()}")
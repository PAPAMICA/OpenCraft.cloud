#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack
import openstack.exceptions
import os
import re
import json 
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--json", help="Output as json", action="store_true")
parser.add_argument("--dict", help="Output as dict", action="store_true")
args = parser.parse_args()
if args.json:
    arg_json = 1
else:
    arg_json = 0

if args.dict:
    arg_dict = 1
else:
    arg_dict = 0

arg_dict = 1
# Instance
instance_name = "test-name"
instance_image = "Debian 11.2 bullseye"
instance_flavor = "a1-ram2-disk20-perf1"
instance_network= "ext-net1"
instance_securitygroup = "ALLL"
instance_keypair = "Yubikey"

# Others
cloud_name = "Infomaniak"
keypair_name = ""

OS_AUTH_URL = "" 
OS_PROJECT_NAME = ""
OS_USERNAME = ""
OS_PASSWORD = ""
OS_REGION_NAME = ""

# Connect to Openstack
def cloud_connection(cloud_name):
        #file = f'/openrc/{cloud_name}'
        file = '/Users/papamica/kDrive/ProjetsPerso/kubernetes/openrc'
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                line=line.split()
                if len(line) > 1:
                    word=line[1].split('=')
                    globals()[word[0]] = word[1]
        return openstack.connect(
            auth_url=OS_AUTH_URL,
            project_name=OS_PROJECT_NAME,
            username=OS_USERNAME,
            password=OS_PASSWORD,
            region_name=OS_REGION_NAME,
            user_domain_name="default",
            project_domain_name="default",
            app_name='examples',
            app_version='1.0',
        )


# Get all informations of all instances
def get_instances_list(cloud):
    if arg_dict == 1:
        result = {}
    else:
        result = ""
    for server in cloud.compute.servers():
        #print(server)
        secgroup = ""
        for i in server.security_groups:
            if (secgroup == ""):
                secgroup = i['name']
            else:
                secgroup = secgroup + ", " + i['name']
        image = cloud.compute.find_image(server.image.id)
        IPv4 = re.search(r'([0-9]{1,3}\.){3}[0-9]{1,3}', str(server.addresses))
        data = {'instance': server.name}
        data['Cloud'] = cloud_name
        data['Status'] = server.status
        data['IP'] = IPv4.group()
        data['Keypair'] = server.key_name
        data['Image'] = image.name
        data['Flavor'] = server.flavor['original_name']
        data['Network'] = next(iter(server.addresses))
        data['Security_groups'] = secgroup
        if arg_dict == 1:
            result[server.name] = data
        elif arg_json == 1:
            data = json.dumps(data, indent = 4)
            result = result + data
        else:
            result = str(result) + f"{server.name}: \n  Cloud: {cloud_name}\n  Status: {server.status}\n  IP: {IPv4.group()}\n  Keypair: {server.key_name} \n  Image: {image.name}\n  Network: {next(iter(server.addresses))} \n  Flavor: {server.flavor['original_name']} \n  Security_groups: {secgroup} \n "
    return result    

# Find and display information about one instance
def get_instance_information(cloud, server_name):
    try:
        if arg_dict == 1:
            result = {}
        else:
            result = ""
        server = cloud.compute.find_server(server_name)
        server = cloud.compute.get_server(server.id)
        secgroup = ""
        for i in server.security_groups:
            if (secgroup == ""):
                secgroup = i['name']
            else:
                secgroup = secgroup + ", " + i['name']
        image = cloud.compute.find_image(server.image.id)
        IPv4 = re.search(r'([0-9]{1,3}\.){3}[0-9]{1,3}', str(server.addresses))
        data = {'instance': server.name}
        data['Cloud'] = cloud_name
        data['Status'] = server.status
        data['IP'] = IPv4.group()
        data['Keypair'] = server.key_name
        data['Image'] = image.name
        data['Flavor'] = server.flavor['original_name']
        data['Network'] = next(iter(server.addresses))
        data['Security_groups'] = secgroup
        if arg_dict == 1:
            result[server.name] = data
        elif arg_json == 1:
            data = json.dumps(data, indent = 4)
            result = result + data
        else:
            result = str(result) + f"{server.name}: \n  Cloud: {cloud_name}\n  Status: {server.status}\n  IP: {IPv4.group()}\n  Keypair: {server.key_name} \n  Image: {image.name}\n  Network: {next(iter(server.addresses))} \n  Flavor: {server.flavor['original_name']} \n  Security_groups: {secgroup} \n "
        return result
    except:
        return (f"{server_name} not found !")


# List keypairs
def list_keypairs(cloud):
    if arg_dict == 1:
        result = {}
    else:
        result = ""
    for keypair in cloud.compute.keypairs():
        if arg_dict == 1:
            result[keypair.id] = keypair.name
        elif arg_json == 1:
            data = {keypair.id: keypair.name}
            data = json.dumps(data, indent = 4)
            result = result + data
        else:
            if (result == ""):
                result = keypair.name
            else:
                result = result + ", " + keypair.name

    return result

# List networks
def list_networks(cloud):
    if arg_dict == 1:
        result = {}
    else:
        result = ""
    for network in cloud.network.networks():
        if arg_dict == 1:
            result[network.id] = network.name
        elif arg_json == 1:
            data = {network.id: network.name}
            data = json.dumps(data, indent = 4)
            result = result + data
        else:
            if (result == ""):
                result = network.name
            else:
                result = result + ", " + network.name

    return result

# List security groups
def list_security_groups(cloud):
    if arg_dict == 1:
        result = {}
    else:
        result = ""
    for sc in cloud.network.security_groups():
        if arg_dict == 1:
            result[sc.id] = sc.name
        elif arg_json == 1:
            data = {sc.id: sc.name}
            data = json.dumps(data, indent = 4)
            result = result + data
        else:
            if (result == ""):
                result = sc.name
            else:
                result = result + ", " + sc.name

    return result

# List images
def list_images(cloud):
    if arg_dict == 1:
        result = {}
    else:
        result = ""
    for image in cloud.compute.images():
        if arg_dict == 1:
            result[image.id] = image.name
        elif arg_json == 1:
            data = {image.id: image.name}
            data = json.dumps(data, indent = 4)
            result = result + data
        else:
            if (result == ""):
                result = image.name
            else:
                result = result + ", " + image.name

    return result


# List flavors
def list_flavors(cloud):
    if arg_dict == 1:
        result = {}
    else:
        result = ""
    for flavor in cloud.compute.flavors():
        if arg_dict == 1:
            result[flavor.id] = flavor.name
        elif arg_json == 1:
            data = {flavor.id: flavor.name}
            data = json.dumps(data, indent = 4)
            result = result + data
        else:
            if (result == ""):
                result = flavor.name
            else:
                result = result + ", " + flavor.name

    return result


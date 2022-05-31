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

arg_dict = 1

# Connect to Openstack
def cloud_connection(file):
    parameters = {}
    try:
        with open(file) as f:
            for line in f.readlines():
                line=line.split()
                if len(line) > 1:
                    word=line[1].split('=')
                    varname = word[0][3:].lower()
                    parameters[varname]=word[1].strip("\"'")
    except:
        print("Provide a valide openrc file please.")
        exit()
    return openstack.connect(**parameters)


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
        metadata = server.metadata
        servertag = list()
        for tag in server.tags:
            servertag.append(tag)
        for meta in metadata:
            if meta == "tags":
                for tag in metadata["tags"].split(", "):
                    servertag.append(tag)
        image = cloud.compute.find_image(server.image.id)
        IPv4 = re.search(r'([0-9]{1,3}\.){3}[0-9]{1,3}', str(server.addresses))
        data = {'instance': server.name}
        data['ID'] = server.id
        data['Status'] = server.status
        data['IP'] = IPv4.group()
        data['Keypair'] = server.key_name
        data['Image'] = image.name
        data['Tags'] = servertag
        data['Flavor'] = server.flavor['original_name']
        data['Network'] = next(iter(server.addresses))
        data['Security_groups'] = secgroup
        if arg_dict == 1:
            result[server.name] = data
        elif arg_json == 1:
            data = json.dumps(data, indent=4)
            result = result + data
        else:
            result = str(
                result) + f"{server.name}: \n  Cloud: {cloud_name}\n  ID: {server.id}\n  Status: {server.status}\n  IP: {IPv4.group()}\n  Keypair: {server.key_name} \n  Tags: {servertag} \n  Image: {image.name}\n  Network: {next(iter(server.addresses))} \n  Flavor: {server.flavor['original_name']} \n  Security_groups: {secgroup} \n "
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
        metadata = server.metadata
        servertag = list()
        for tag in server.tags:
            servertag.append(tag)
        for meta in metadata:
            if meta == "tags":
                for tag in metadata["tags"].split(", "):
                    servertag.append(tag)
        image = cloud.compute.find_image(server.image.id)
        IPv4 = re.search(r'([0-9]{1,3}\.){3}[0-9]{1,3}', str(server.addresses))
        data = {'instance': server.name}
        data['Status'] = server.status
        data['IP'] = IPv4.group()
        data['Keypair'] = server.key_name
        data['Image'] = image.name
        data['Tags'] = servertag
        data['Flavor'] = server.flavor['original_name']
        data['Network'] = next(iter(server.addresses))
        data['Security_groups'] = secgroup
        if arg_dict == 1:
            result[server.name] = data
        elif arg_json == 1:
            data = json.dumps(data, indent=4)
            result = result + data
        else:
            result = str(
                result) + f"{server.name}: \n  Cloud: {cloud_name}\n  Status: {server.status}\n  IP: {IPv4.group()}\n  Keypair: {server.key_name}\n  Tags: {servertag} \n  Image: {image.name}\n  Network: {next(iter(server.addresses))} \n  Flavor: {server.flavor['original_name']} \n  Security_groups: {secgroup} \n "
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
            data = json.dumps(data, indent=4)
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
            data = json.dumps(data, indent=4)
            result = result + data
        else:
            if (result == ""):
                result = network.name
            else:
                result = result + ", " + network.name

    return result


# List routers
def list_routers(cloud):
    if arg_dict == 1:
        result = {}
    else:
        result = ""
    for router in cloud.network.routers():
        if arg_dict == 1:
            result[router.id] = router.name
        elif arg_json == 1:
            data = {router.id: router.name}
            data = json.dumps(data, indent=4)
            result = result + data
        else:
            if (result == ""):
                result = router.name
            else:
                result = result + ", " + router.name

    return result


def list_router_v2(cloud):
    if arg_dict == 1:
        result = {}
    else:
        result = ""
    for router in cloud.network.routers():
        for info in router.external_gateway_info:
            if info == "external_fixed_ips":
                for data in router.external_gateway_info[info]:
                    router_ipwan = data['ip_address']
            if info == "network_id":
                router_network_wan = router.external_gateway_info[info]
                router_network_wan = cloud.network.get_network(
                    router_network_wan)
                router_network_wan = router_network_wan.name
        for port in list(cloud.network.ports(device_id=router.id)):
            router_network_lan = cloud.network.get_network(port.network_id)
            router_network_lan = router_network_lan.name
            for data in port.fixed_ips:
                router_iplan = data['ip_address']

        if arg_dict == 1:
            result[router.name] = {'id': router.id, 'status': router.status, 'ipwan': router_ipwan,
                                   'network_wan': router_network_wan, 'iplan': router_iplan, 'network_lan': router_network_lan}
        elif arg_json == 1:
            data = {router.id: router.name}
            data = json.dumps(data, indent=4)
            result = result + data
        else:
            if (result == ""):
                result = router.name
            else:
                result = result + ", " + router.name
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
            data = json.dumps(data, indent=4)
            result = result + data
        else:
            if (result == ""):
                result = sc.name
            else:
                result = result + ", " + sc.name

    return result


# List security groups of an instance
def list_sc_instance(cloud, instance):
    if arg_dict == 1:
        result = {}
    else:
        result = ""
    scs = cloud.compute.fetch_server_security_groups(instance)
    for item in scs['security_groups']:
        sc_id = item['id']
        sc_name = item['name']
        if arg_dict == 1:
            result[sc_name] = sc_id
        elif arg_json == 1:
            data = {sc_name: sc_id}
            data = json.dumps(data, indent=4)
            result = result + data
        else:
            if (result == ""):
                result = sc_name
            else:
                result = result + ", " + sc_name
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
            data = json.dumps(data, indent=4)
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
            data = json.dumps(data, indent=4)
            result = result + data
        else:
            if (result == ""):
                result = flavor.name
            else:
                result = result + ", " + flavor.name

    return result

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker_api as docker

containers = docker.get_instances_list()
print(containers)
# -*- coding: utf-8 -*-
###
# ADapted from config_loader.py in HPE iLO and HPE OneView
# Python github repo
# 
# Adaptations
#   Name: ConfigLoader.py
###
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

import json
import os

CUR_MODULE_DIR = os.path.dirname(__file__)
DEFAULT_EXAMPLE_CONFIG_FILE = os.path.join(CUR_MODULE_DIR, 'config.json')


def try_load_from_file(config, file_name=None):
    if not file_name:
        file_name = DEFAULT_EXAMPLE_CONFIG_FILE

    if not os.path.isfile(file_name):
        return config

    with open(file_name) as json_data:
        return json.load(json_data)

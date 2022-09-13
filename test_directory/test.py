#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
import random
import json
import time
import uuid
from collections import OrderedDict


session = None
user_id = 474565
controls = ['DWG', 'PDF', 'NWC']
directory = r'I:\51_UZHNY_TREUGOLNIK\01_PROJECT\III_1_AS\01_RVT'
filenames = ['NewYork', 'LosAngeles', 'Chicago', 'Houston', 'Philadelphia']



# commands[0] = control
# commands[1:] = filenames
##############################
def create_session():
    return str(uuid.uuid1())


##############################
data = OrderedDict()
action = dict()
cmd = list()
##############################


for idx in range(7):
    action = {}
    time.sleep(1)
    commands = list()
    commands.append(random.choice(controls))
    commands.extend([random.choice(filenames) for _ in range(5)])
    data[idx] = action[user_id] = commands
    print(f'action = {action.items()}')
    print("#########")


print(f'data = {data.keys()}')
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
import random
import json
import time
import uuid

#
# directory = 'I:\51_UZHNY_TREUGOLNIK\01_PROJECT\III_1_AS\01_RVT'
# controlId = 'DWG'
#
# dictionary={}

# for i in dictionary:
#     if controlId =='DWG':
#         dictionary[]
#         print(dictionary)


# d = {"A1":"123", "A2":"456"}
# d.update({"A1":"333", "A3":"789"})
# print(d)

# key='I:\51_UZHNY_TREUGOLNIK\01_PROJECT\III_1_AS\01_RVT'
# value='DWG'
# dictionary[key]=value
# print(dictionary)


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
data = {}
action = {}
commands = []
##############################


for _ in range(7):
    action = {}
    time.sleep(1)
    commands = list()
    session = create_session()
    commands.append(random.choice(controls))
    commands.extend([random.choice(filenames) for _ in range(5)])
    data[session] = action[user_id] = commands
    print(f'action = {action.items()}')
    print("#########")


print(f'data = {data.keys()}')
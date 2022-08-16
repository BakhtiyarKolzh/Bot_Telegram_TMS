#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import uuid
import json
import time, random
from collections import OrderedDict
from multiprocessing import Lock


def create_session():
    return str(uuid.uuid1())


def add_item_to_dictionary(data, key, value):
    if isinstance(value, list):
        data[key] = value
        return data


def update_item_to_dictionary(data, key, value):
    if isinstance(value, list):
        data.update({key: value})
        return data


def pop_item_from_dictionary(data):
    global database
    result = data.popitem(last=False)
    if isinstance(data, dict):
        database = data
    return result


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        return json.JSONEncoder.default(self, obj)


def remove_file(path):
    try:
        if os.path.isfile(path):
            os.unlink(path)
    except Exception as e:
        print(e)
    return True


def write_json_data(path, data, rewrite=True):
    if rewrite and os.path.exists(path): remove_file(path)
    if isinstance(data, dict):
        try:
            with open(path, "w") as file:
                json.dump(data, file)
        except Exception as e:
            print(e)
    return True


def deserialize_json_data(path):
    if os.path.isfile(path):
        try:
            with open(path, "r") as file:
                return json.load(file)
        except Exception as e:
            return print("Error: {}".format(e))


def update_json_data(path, data):
    store = deserialize_json_data(path)
    data = (store | data if isinstance(store, dict) else data)
    if isinstance(data, dict):
        write_json_data(path, data, True)
        print("Completed")
    return data


def save_command_data(path, data, filepath, control_id, commands):
    with Lock():
        action = list()
        action.append(filepath)
        action.append(control_id)
        if isinstance(commands, list): action.extend(commands)
        if not isinstance(commands, list): action.append(commands)
        data = add_item_to_dictionary(data, create_session(), action)
        return update_json_data(path, data)


def execute_command(path, data):
    with Lock():
        commands = []
        while len(data):
            time.sleep(5)
            commands = pop_item_from_dictionary(data)
            if write_json_data(path, data, True):
                session, action = commands
                if isinstance(action, list):
                    filepath = action.pop(0)
                    control = action.pop(0)
                    for val in commands:
                        if isinstance(val, int):
                            commands.append(val)
                        elif isinstance(val, str) and val.isdigit():
                            commands.append(int(val))
                    print(commands)
                    print(filepath)
                    print(control)
                    print("\t")
    return len(commands)


database = OrderedDict()
CNTRL = ["DWG", "NWC", "IFC", "PDF"]
mypath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")

for x in range(5):
    time.sleep(5)
    control = random.choice(CNTRL)
    commands = [str(random.randint(0, 10)) for i in range(5)]
    save_command_data(mypath, database, mypath, control, commands)
    execute_command(mypath, database)

print("DATA: " + str(database))

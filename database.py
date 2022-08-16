#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import uuid
import json
import time, random
from collections import OrderedDict
from multiprocessing import Lock

import RevitSortFiles


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
    if len(data): return data.popitem(last=False)


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
        print("Save data count {}\n".format(len(data)))
    return data


def save_command_data(data_path, filepath, control_id, commands):
    with Lock():
        action = list()
        data = OrderedDict()
        action.append(filepath)
        action.append(control_id)
        if isinstance(commands, list): action.extend(commands)
        if not isinstance(commands, list): action.append(commands)
        data = add_item_to_dictionary(data, create_session(), action)

        return update_json_data(data_path, data)


def read_command_data(data_path, data):
    with Lock():
        commands = []
        session, action = pop_item_from_dictionary(data)
        if write_json_data(data_path, data, True):
            if isinstance(action, list):
                filepath = action.pop(0)
                control = action.pop(0)
                for val in action:
                    num = None
                    if isinstance(val, int): num = val
                    if isinstance(val, str) and val.isdigit(): num = int(val)
                    if num is not None and num not in commands: commands.append(num)

                return filepath, control, commands


def execute_commands(data_path, data):
    for _ in range(len(data)):
        result = read_command_data(data_path, data)
        filepath, control, commands = result
        paths = RevitSortFiles.get_result_rvt_path_list(filepath)
        paths = RevitSortFiles.retrieve_paths(paths, commands)
        if "DWG" == control: print("Set DWG")
        if "NWC" == control: print("Set NWC")
        if "IFC" == control: print("Set IFC")
        if "PDF" == control: print("Set PDF")
        [print(path) for path in paths]
        print(commands)

    return print("\n")


database = OrderedDict()
cmd = ["DWG", "NWC", "IFC", "PDF"]
mypath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")

for x in range(7):
    time.sleep(0.25)
    control = random.choice(cmd)
    path = r"I:\48_BTG_3-4\01_PROJECT\III_1_AS\01_RVT"
    commands = [str(random.randint(0, 25)) for i in range(5)]
    save_command_data(mypath, path, control, commands)
    if 5 < x: execute_commands(mypath, database)

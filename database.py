#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import uuid
import json
import time, random
from collections import OrderedDict
from multiprocessing import Lock

database = OrderedDict()
LIST = "qwertyuiopasdfghjklzxcvbnm"
mypath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")


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


complex_json = json.dumps(database, cls=ComplexEncoder)
ComplexEncoder().encode(database)


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


def write_command_data(path, data, control, commands):
    action = list()
    action.append(control)
    action.extend(commands)
    session = create_session()
    data = add_item_to_dictionary(data, session, action)
    return update_json_data(path, data)


def execute_command(path, data):
    while len(data):
        result = pop_item_from_dictionary(data)
        if write_json_data(path, data, True):
            session, action = result
            if isinstance(action, list):
                control = action.pop(0)
                for param in commands:
                    if param.is_integer():
                        value = int(param)
                        time.sleep(0.5)
                        print(value)
    return True



def execute_command_process(path, data, control, commands):
    with Lock():
        data = write_command_data(path, data, control, commands)
        if isinstance(data, OrderedDict) and len(data):
            return execute_command(path, data)
    return


for x in range(5):
    control = str(random.randint(100, 1000))
    commands = [random.choice(LIST) for i in range(5)]
    execute_command_process(mypath, database, control, commands)


print("DATA: " + str(database))
print(type(database))

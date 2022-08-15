#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import json
import os.path

import pytest as pytest

DATA = dict()
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data_file.json")


def add_item_to_dictionary(data, key, value):
    if isinstance(value, list):
        data[key] = value
        return data


def update_item_to_dictionary(data, key, value):
    if isinstance(value, list):
        data.update({key: value})
        return data


def pop_item_from_dictionary(data, key=0):
    if key is not None and key in data.keys():
        return data.pop(key)
    for k in data.keys():
        return data.pop(k)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        return json.JSONEncoder.default(self, obj)


complex_json = json.dumps(DATA, cls=ComplexEncoder)
ComplexEncoder().encode(DATA)


def remove_file(path):
    try:
        if os.path.isfile(path):
            os.unlink(path)
    except Exception as e:
        print(e)
    return True


def write_json_data(path, data):
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
            print(e)
    return True


def pop_item_from_store(path, key):
    data = deserialize_json_data(path)
    if isinstance(data, dict):
        if key in data.keys():
            remove_file(path)
            value = data.pop(key)
            write_json_data(path, data)
            return value


def update_json_data(path, data):
    store = deserialize_json_data(path)
    if store is None: print("store is none")
    data = (store | data if store else data)
    if data is None: print("Is not update")
    if isinstance(data, dict) and remove_file(path):
        if not os.path.exists(path):
            write_json_data(path, data)
    return data


session = uuid.uuid1()
control = str(12345)
commands = ["her", "nan", "python", "add"]

guidValue01 = 1
dictValue01 = ["her", "nan", "python", "add"]

guidValue02 = 2
dictValue02 = ["rev", "sec", "sharp", "pop"]

guidValue03 = 3
dictValue03 = ["ber", "mem", "java", "remove"]

guidValue04 = 4
dictValue04 = ["ser", "sen", "cmd", "update"]

guidValue05 = 5
dictValue05 = ["ser", "sen", "cmd", "update"]


# general_data = add_item_to_dictionary(general_data, guidValue01, dictValue01)
# general_data = add_item_to_dictionary(general_data, guidValue02, dictValue02)
# general_data = add_item_to_dictionary(general_data, guidValue03, dictValue03)
#
# general_data = update_item_to_dictionary(general_data, guidValue03, dictValue02)
# general_data = update_item_to_dictionary(general_data, guidValue02, dictValue01)
# general_data = update_item_to_dictionary(general_data, guidValue01, dictValue03)
# general_data = update_item_to_dictionary(general_data, guidValue04, dictValue04)
# general_data = update_item_to_dictionary(general_data, guidValue05, dictValue05)
# update_json_data(data_path, general_data)

# pop_item_from_dictionary(general_data)
# print(pop_item_from_store(data_path, str(5)))
# pop_item_from_dictionary(general_data)


def set_input_data(data, control, commands):
    session = uuid.uuid1()
    action = add_item_to_dictionary(dict(), control, commands)
    return add_item_to_dictionary(data, session, action)



result = deserialize_json_data(data_path)
print("result store: - " + str(result))
print(type(result))
print(session)

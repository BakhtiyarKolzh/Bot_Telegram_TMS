#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import time
import uuid
from collections import OrderedDict

import path_manager

database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")
rvt_path_list_file = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\revit_path_list_bot.txt")


def create_session():
    return str(uuid.uuid1())


def remove(path):
    if os.path.isfile(path):
        try:
            os.unlink(path)
        except:
            pass
    return


def add_item_to_dictionary(data, key, value):
    if isinstance(value, list):
        data[key] = value
        return data


def pop_item_from_dictionary(data):
    if len(data): return data.popitem(last=False)


def write_json_data(path, data):
    if not isinstance(data, dict): return
    while True:
        try:
            path = os.path.realpath(path)
            with open(path, "w") as file:
                json.dump(data, file)
                return True
        except:
            time.sleep(0.5)


def deserialize_json_data(path):
    while True:
        if not os.path.isfile(path): return
        if os.path.isfile(path):
            try:
                with open(path, "r") as file:
                    return json.load(file)
            except Exception:
                time.sleep(0.5)


def update_json_data(path, data):
    store = deserialize_json_data(path)
    data = (store | data if isinstance(store, dict) else data)
    if isinstance(data, dict):
        write_json_data(path, data)
        print("Save data count {}\n".format(len(data)))
    return data


def save_command_data(data_path, filepath, control_id, commands):
    action = list()
    data = OrderedDict()
    action.append(filepath)
    action.append(control_id)
    if isinstance(commands, list): action.extend(commands)
    if not isinstance(commands, list): action.append(commands)
    data = add_item_to_dictionary(data, create_session(), action)

    return update_json_data(data_path, data)


def read_command_data(data_path, data):
    commands = []
    session, action = pop_item_from_dictionary(data)
    if write_json_data(data_path, data):
        if isinstance(action, list):
            filepath = action.pop(0)
            control = action.pop(0)
            for val in action:
                if isinstance(val, str) and val.isdigit(): val = int(val)
                if isinstance(val, int) and val not in commands: commands.append(val)

            return filepath, control, commands


def run_cmd(control, paths):
    global rvt_path_list_file
    path_manager.write_revit_path_list_to_file(rvt_path_list_file, paths)
    if "DWG" == control:
        bat_file = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToDWG.bat")
        if os.path.exists(bat_file):
            os.startfile(bat_file)
            print("Set DWG")
    if "NWC" == control:
        bat_file = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToNWC.bat")
        if os.path.exists(bat_file):
            os.startfile(bat_file)
            print("Set NWC")
    if "PDF" == control:
        bat_file = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToPDF.bat")
        if os.path.exists(bat_file):
            os.startfile(bat_file)
            print("Set PDF")

    return


def execute_commands(data_path):
    data = deserialize_json_data(data_path)
    if isinstance(data, dict):
        data = OrderedDict(data)
        for _ in range(len(data)):
            result = read_command_data(data_path, data)
            filepath, control, commands = result
            if isinstance(commands, list) and len(commands):
                if isinstance(filepath, str) and isinstance(control, str):
                    commands = [cmd for cmd in commands if isinstance(cmd, int)]
                    paths = path_manager.get_result_rvt_path_list(filepath)
                    paths = path_manager.retrieve_paths(paths, commands)
                    [print(path) for path in paths]
                    run_cmd(control, paths)
                    time.sleep(1000)
    return


def start():
    while True:
        time.sleep(5)
        print('while')
        database_dict = deserialize_json_data(database_path)
        if not isinstance(database_dict, dict): time.sleep(1000)
        if isinstance(database_dict, dict) and not len(database_dict): remove(database_path)
        if isinstance(database_dict, dict) and len(database_dict): execute_commands(database_path)

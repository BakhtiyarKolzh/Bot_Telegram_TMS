#!/usr/bin/env python
# -*- coding: utf-8 -*-

import concurrent.futures
import json
import os
import subprocess
import time
from collections import OrderedDict
from multiprocessing import Lock

import path_manager

mutex = Lock()
database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")
rvt_path_list_file = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\revit_path_list_bot.txt")


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


def write_json_data(path, data):
    if not isinstance(data, dict): return
    with mutex:
        print(data.items())
        try:
            path = os.path.realpath(path)
            with open(path, "w") as file:
                json.dump(data, file)
                return True
        except Exception as exc:
            time.sleep(0.5)
            print(exc)


def deserialize_json_data(path):
    if not os.path.isfile(path): return
    if os.path.isfile(path):
        with mutex:
            try:
                with open(path, "r") as file:
                    return json.load(file)
            except Exception as exc:
                time.sleep(0.5)
                print(exc)


def update_json_data(path, data):
    store = deserialize_json_data(path)
    data = (store | data if isinstance(store, dict) else data)
    if isinstance(data, dict):
        write_json_data(path, data)
        print("Save data count {}\n".format(len(data)))
    return data


def execute_commands(data_path):
    data = deserialize_json_data(data_path)
    if isinstance(data, dict):
        data = OrderedDict(data)
        count, action = data.popitem(last=False)
        write_json_data(data_path, data)
        if isinstance(action, dict):
            print("data is dict")
            for user, commands in action.items():
                if isinstance(commands, list):
                    control = commands.pop(0)
                    directory = commands.pop(0)
                    print(f'Action = {control} {directory} {commands}')
                    commands = [int(cmd) for cmd in commands if cmd.isdigit()]
                    # paths = path_manager.get_result_rvt_path_list(directory)
                    # paths = path_manager.retrieve_paths(paths, commands)
                    # run_cmd(control, paths)
                    ##################


def run_cmd(control, paths):
    global rvt_path_list_file

    def worker(cmd):
        return subprocess.Popen(cmd, shell=True)

    path_manager.write_revit_path_list_to_file(rvt_path_list_file, paths)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:

        if "DWG" == control:
            cmd = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToDWG.bat")
            if os.path.exists(cmd):
                pool.submit(worker, cmd)
                print(f"Set DWG => ")

        if "NWC" == control:
            cmd = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToNWC.bat")
            if os.path.exists(cmd):
                pool.submit(worker, cmd)
                print(f"Set DWG => ")

        if "PDF" == control:
            cmd = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToPDF.bat")
            if os.path.exists(cmd):
                pool.submit(worker, cmd)
                print(f"Set DWG => ")

    return
